import logging
from datetime import datetime, timedelta
from bson import ObjectId
from talentwizer_commons.utils.db import mongo_database
from celery.result import AsyncResult
from .template_utils import populate_template_v2
from .core import celery_app
from .test_utils import get_test_delay
from .email_utils import schedule_email, build_gmail_service
from talentwizer_commons.app.api.routers.template import calculate_step_time

logger = logging.getLogger(__name__)

# Initialize MongoDB collections
sequence_collection = mongo_database["email_sequences"]
sequence_audit_collection = mongo_database["email_sequence_audits"]
template_collection = mongo_database["templates"]

async def cancel_sequence_steps(sequence_id: str, reason: str = "Recipient replied to email"):
    """Cancel remaining steps in a sequence."""
    try:
        scheduled_audits = sequence_audit_collection.find({
            "sequence_id": sequence_id,
            "status": "SCHEDULED"
        })

        for audit in scheduled_audits:
            if audit.get("schedule_id"):
                task = AsyncResult(audit["schedule_id"], app=celery_app)
                task.revoke(terminate=True)
                
            sequence_audit_collection.update_one(
                {"_id": audit["_id"]},
                {"$set": {
                    "status": "CANCELLED",
                    "updated_at": datetime.utcnow(),
                    "cancel_reason": reason
                }}
            )
            
        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {"$set": {
                "status": "COMPLETED",
                "completion_reason": reason,
                "updated_at": datetime.utcnow()
            }}
        )
        
    except Exception as e:
        logger.error(f"Error cancelling sequence steps: {str(e)}")
        raise

def update_sequence_status_sync(sequence_id: str):
    """Update sequence status and propagate thread ID."""
    try:
        # Get sequence and its audits
        sequence = sequence_collection.find_one({"_id": ObjectId(sequence_id)})
        if not sequence:
            return

        audits = list(sequence_audit_collection.find(
            {"sequence_id": sequence_id}).sort("step_index", 1))
        if not audits:
            return

        # Get first sent email's thread ID
        first_sent = next((a for a in audits if a["status"] == "SENT"), None)
        if first_sent and first_sent.get("thread_id"):
            thread_id = first_sent["thread_id"]
            
            # Update sequence thread ID
            sequence_collection.update_one(
                {"_id": ObjectId(sequence_id)},
                {"$set": {"thread_id": thread_id}}
            )

            # Propagate thread ID to all remaining steps
            remaining_audits = [a for a in audits if a["status"] == "SCHEDULED"]
            for audit in remaining_audits:
                email_payload = audit.get("email_payload", {})
                email_payload["thread_id"] = thread_id
                sequence_audit_collection.update_one(
                    {"_id": audit["_id"]},
                    {"$set": {
                        "thread_id": thread_id,
                        "email_payload": email_payload
                    }}
                )

        # Calculate status counts
        total = len(audits)
        sent = sum(1 for a in audits if a["status"] == "SENT")
        failed = sum(1 for a in audits if a["status"] == "FAILED")
        cancelled = sum(1 for a in audits if a["status"] == "CANCELLED")
        scheduled = sum(1 for a in audits if a["status"] == "SCHEDULED")

        # Determine sequence status
        status = (
            "COMPLETED" if sent == total
            else "FAILED" if failed > 0
            else "CANCELLED" if cancelled == total
            else "IN_PROGRESS" if sent > 0
            else "PENDING"
        )

        # Update sequence with latest stats
        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {"$set": {
                "status": status,
                "stats": {
                    "total": total,
                    "sent": sent,
                    "failed": failed,
                    "cancelled": cancelled,
                    "scheduled": scheduled
                },
                "updated_at": datetime.utcnow()
            }}
        )

    except Exception as e:
        logger.error(f"Error updating sequence status: {str(e)}", exc_info=True)

async def create_sequence_for_profile(profile: dict, template: dict, token_data: dict, job_title: str, client_info: dict) -> dict:
    """Create and schedule email sequence for a single profile."""
    try:
        sequence = {
            "profile_id": str(profile["_id"]),
            "template_id": str(template["_id"]),
            "public_identifier": profile["public_identifier"],
            "status": "PENDING",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "thread_id": None,  # Will be set after first email
            "sender": token_data["email"],
            "cc": template.get("cc", []),
            "bcc": template.get("bcc", [])
        }
        
        sequence_result = sequence_collection.insert_one(sequence)
        sequence_id = str(sequence_result.inserted_id)
        base_time = datetime.utcnow()
        test_delay = get_test_delay()  # Get test configuration if enabled

        # Process each step with proper scheduling
        for idx, step in enumerate(template["steps"]):
            # Calculate proper scheduled time
            if test_delay:
                # In test mode, space out emails by test delay
                if idx == 0:
                    scheduled_time = base_time
                else:
                    step_delay = test_delay['base_delay'] + (idx * test_delay['step_increment'])
                    scheduled_time = base_time + timedelta(seconds=step_delay)
            else:
                # In production mode, use template's schedule configuration
                scheduled_time = calculate_step_time(step, base_time)

            # Process content and subject
            processed_content = await populate_template_v2(
                step["content"], 
                profile,
                job_title,
                client_info
            )
            
            # Keep original subject for first email, use Re: for follow-ups
            if idx == 0:
                processed_subject = await populate_template_v2(
                    step["subject"],
                    profile,
                    job_title,
                    client_info
                )
                # Store original subject in sequence for follow-ups
                sequence_collection.update_one(
                    {"_id": ObjectId(sequence_id)},
                    {"$set": {"original_subject": processed_subject}}
                )
            else:
                # Get original subject from sequence
                sequence = sequence_collection.find_one({"_id": ObjectId(sequence_id)})
                processed_subject = f"Re: {sequence.get('original_subject', '')}"

            # Create audit record without thread_id
            audit = {
                "sequence_id": sequence_id,
                "step_index": idx,
                "status": "SCHEDULED",
                "scheduled_time": scheduled_time,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_initial": idx == 0,
                "email_payload": {
                    "to_email": profile.get("email", []),
                    "subject": processed_subject,
                    "content": processed_content,
                    "sender": token_data["email"],
                    "sequence_id": sequence_id,
                    "is_initial": idx == 0,
                    "cc": template.get("cc", []),
                    "bcc": template.get("bcc", [])
                }
            }
            
            audit_result = sequence_audit_collection.insert_one(audit)
            audit_id = str(audit_result.inserted_id)

            # Schedule email with audit ID and scheduled_time
            email_payload = {
                **audit["email_payload"],
                "audit_id": audit_id,
                "check_replies": True  # Flag to enable reply checking
            }

            schedule_result = await schedule_email(
                email_payload=email_payload,
                scheduled_time=scheduled_time,
                token_data=token_data
            )

            if schedule_result:
                sequence_audit_collection.update_one(
                    {"_id": audit_result.inserted_id},
                    {"$set": {"schedule_id": schedule_result}}
                )

        return {
            "sequence_id": sequence_id,
            "profile_id": str(profile["_id"]),
            "public_identifier": profile["public_identifier"]
        }
        
    except Exception as e:
        logger.error(f"Error creating sequence: {str(e)}", exc_info=True)
        if 'sequence_id' in locals():
            cleanup_failed_sequence(sequence_id)
        raise

async def get_sequence_status(sequence_id: str) -> dict:
    """Get detailed status of a sequence."""
    try:
        sequence = sequence_collection.find_one({"_id": ObjectId(sequence_id)})
        if not sequence:
            raise ValueError(f"Sequence {sequence_id} not found")

        audits = list(sequence_audit_collection.find({"sequence_id": sequence_id}))
        
        # Get status counts
        status_counts = {
            "scheduled": sum(1 for a in audits if a["status"] == "SCHEDULED"),
            "sent": sum(1 for a in audits if a["status"] == "SENT"),
            "failed": sum(1 for a in audits if a["status"] == "FAILED"),
            "cancelled": sum(1 for a in audits if a["status"] == "CANCELLED")
        }
        
        # Get task statuses
        task_statuses = []
        for audit in audits:
            if audit.get("schedule_id"):
                task = AsyncResult(audit["schedule_id"])
                task_statuses.append({
                    "step_index": audit["step_index"],
                    "celery_status": task.status,
                    "result": str(task.result) if task.result else None
                })

        return {
            "sequence_status": sequence["status"],
            "status_counts": status_counts,
            "task_statuses": task_statuses,
            "updated_at": sequence["updated_at"]
        }

    except Exception as e:
        logger.error(f"Error getting sequence status: {str(e)}")
        raise

def cleanup_test_duplicates():
    """Clean up duplicate test mode entries."""
    try:
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "sequence_id": "$sequence_id",
                        "step_index": "$step_index"
                    },
                    "count": {"$sum": 1},
                    "docs": {"$push": "$$ROOT"}
                }
            },
            {"$match": {"count": {"$gt": 1}}}
        ]

        duplicates = sequence_audit_collection.aggregate(pipeline)

        for duplicate in duplicates:
            docs = sorted(duplicate["docs"], key=lambda x: x["created_at"], reverse=True)
            kept_doc = docs[0]

            for doc in docs[1:]:
                sequence_audit_collection.update_one(
                    {"_id": doc["_id"]},
                    {
                        "$set": {
                            "status": "CANCELLED",
                            "error_message": "Duplicate test mode entry",
                            "updated_at": datetime.utcnow()
                        }
                    }
                )

            if kept_doc.get("sequence_id"):
                update_sequence_status_sync(kept_doc["sequence_id"])

    except Exception as e:
        logger.error(f"Error cleaning up test duplicates: {str(e)}")

def cleanup_failed_sequence(sequence_id: str):
    """Clean up a failed sequence and its associated audits."""
    try:
        # Cancel any scheduled tasks
        audits = sequence_audit_collection.find({"sequence_id": sequence_id})
        for audit in audits:
            if audit.get("schedule_id"):
                task = AsyncResult(audit["schedule_id"])
                task.revoke(terminate=True)
                
            # Update audit status
            sequence_audit_collection.update_one(
                {"_id": audit["_id"]},
                {"$set": {
                    "status": "FAILED",
                    "updated_at": datetime.utcnow(),
                    "error_message": "Sequence creation failed"
                }}
            )
            
        # Update sequence status    
        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {"$set": {
                "status": "FAILED",
                "updated_at": datetime.utcnow(),
                "error": "Sequence creation failed"
            }}
        )
    except Exception as e:
        logger.error(f"Error cleaning up failed sequence: {str(e)}")

def restore_tasks():
    """Restore and reschedule tasks from MongoDB - now synchronous."""
    try:
        logger.info("Starting task restoration process...")
        restored_count = 0

        # Get all sequences with PENDING or IN_PROGRESS status
        active_sequences = sequence_collection.find({
            "status": {"$in": ["PENDING", "IN_PROGRESS"]}
        })

        for sequence in active_sequences:
            # Get all scheduled audits for this sequence
            scheduled_audits = sequence_audit_collection.find({
                "sequence_id": str(sequence["_id"]),
                "status": "SCHEDULED",
                "scheduled_time": {"$lt": datetime.utcnow()}
            }).sort("step_index", 1)

            thread_id = sequence.get("thread_id")
            
            for audit in scheduled_audits:
                try:
                    # Update email payload with sequence thread_id
                    email_payload = audit.get("email_payload", {})
                    email_payload["thread_id"] = thread_id
                    
                    new_task = celery_app.send_task(
                        'send_scheduled_email',
                        kwargs={
                            'email_payload': email_payload,
                            'user_email': email_payload.get('sender')
                        },
                        queue='email_queue',
                        routing_key='email.send'
                    )

                    # Update audit with new task ID
                    sequence_audit_collection.update_one(
                        {"_id": audit["_id"]},
                        {"$set": {
                            "schedule_id": new_task.id,
                            "rescheduled_from": audit.get("schedule_id"),
                            "rescheduled_at": datetime.utcnow()
                        }}
                    )

                    logger.info(f"Restored task {audit['_id']} with new ID {new_task.id}")
                    restored_count += 1

                except Exception as e:
                    logger.error(f"Failed to restore task: {str(e)}")
                    continue

        logger.info(f"Task restoration completed. Restored {restored_count} tasks")
        return restored_count

    except Exception as e:
        logger.error(f"Task restoration failed: {str(e)}")
        return 0

async def check_sequence_replies(thread_id: str, sequence_id: str, token_data: dict, sender_email: str) -> bool:
    """Check for replies in email thread and handle them."""
    try:
        if not thread_id or not token_data.get("scope"):
            return False
            
        if "gmail.send" in token_data["scope"]:
            service = build_gmail_service(token_data)
            thread = service.users().threads().get(
                userId='me',
                id=thread_id,
                format='metadata',
                metadataHeaders=['From', 'Date']
            ).execute()
            
            messages = thread.get('messages', [])
            if len(messages) <= 1:
                return False

            # Sort messages by date to check latest replies
            sorted_messages = sorted(messages, 
                key=lambda x: x['internalDate'] if 'internalDate' in x else 0,
                reverse=True)

            # Check if any recent message is from recipient
            for message in sorted_messages[:-1]:  # Skip the first message (our sent email)
                headers = {h['name']: h['value'] for h in message['payload']['headers']}
                from_email = headers.get('From', '').lower()
                
                if sender_email.lower() not in from_email:
                    # Found a reply from recipient, cancel sequence
                    await cancel_sequence_steps(sequence_id, reason="Recipient replied to email")
                    
                    # Update sequence status
                    sequence_collection.update_one(
                        {"_id": ObjectId(sequence_id)},
                        {"$set": {
                            "status": "COMPLETED",
                            "completion_reason": "Recipient replied to email",
                            "updated_at": datetime.utcnow()
                        }}
                    )
                    return True

        return False

    except Exception as e:
        logger.error(f"Error checking thread replies: {str(e)}")
        return False

async def schedule_email(email_payload: dict, scheduled_time: datetime = None, token_data: dict = None) -> str:
    """Schedule an email to be sent at a specific time."""
    try:
        # Schedule task with correct name
        task = celery_app.send_task(
            'send_scheduled_email',  # Match task name exactly
            kwargs={
                'email_payload': email_payload,
                'user_email': token_data.get('email'),
                'scheduled_time': scheduled_time.isoformat() if scheduled_time else None
            },
            queue='email_queue',
            routing_key='email.send'
        )
        
        return str(task.id)
    except Exception as e:
        logger.error(f"Failed to schedule email: {str(e)}", exc_info=True)
        raise

