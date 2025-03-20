import os
import json
from celery import Celery, signals
from celery.states import PENDING, SUCCESS, FAILURE
from kombu import Queue, Exchange
from datetime import datetime
import logging
from bson import ObjectId
from typing import Dict, Any
from talentwizer_commons.utils.db import mongo_database
from .core import redis_client, get_redis_url
from .email_utils import send_email_from_user_email_sync, build_gmail_service
from .token_utils import get_valid_token

logger = logging.getLogger(__name__)

# Initialize Celery with proper name 
celery_app = Celery('talentwizer_commons.utils.celery_init')

# Configure Celery
celery_app.conf.update(
    broker_url=get_redis_url(),
    result_backend=get_redis_url(),
    broker_connection_retry_on_startup=True,
    imports=['talentwizer_commons.utils.celery_init'],
    task_track_started=True,
    task_ignore_result=False,
    task_routes={
        'send_scheduled_email': {
            'queue': 'email_queue',
            'exchange': 'email'
        }
    }
)

# Define queues
default_exchange = Exchange('default', type='direct')
email_exchange = Exchange('email', type='direct')

celery_app.conf.task_queues = (
    Queue('celery', default_exchange, routing_key='celery'),
    Queue('email_queue', email_exchange, routing_key='email.#'),
)

# MongoDB collections
sequence_collection = mongo_database["email_sequences"]
sequence_audit_collection = mongo_database["email_sequence_audits"]

@celery_app.task(
    name='send_scheduled_email',
    queue='email_queue',
    autoretry_for=(Exception,),
    max_retries=3
)
def send_scheduled_email(email_payload: Dict[str, Any], user_email: str, **kwargs):
    """Send scheduled email task."""
    try:
        logger.info(f"Starting scheduled email task at {datetime.utcnow()}")
        scheduled_time = kwargs.get('scheduled_time')
        
        # Honor scheduled time
        if scheduled_time:
            scheduled_dt = datetime.fromisoformat(scheduled_time)
            now = datetime.utcnow()
            if scheduled_dt > now:
                logger.info(f"Task scheduled for {scheduled_dt}, current time {now}")
                celery_app.send_task(
                    'send_scheduled_email',
                    kwargs={
                        'email_payload': email_payload,
                        'user_email': user_email,
                        'scheduled_time': scheduled_time
                    },
                    eta=scheduled_dt,
                    queue='email_queue'
                )
                return {'status': 'deferred', 'scheduled_time': scheduled_time}

        sequence_id = email_payload.get("sequence_id")
        if sequence_id:
            sequence = sequence_collection.find_one({"_id": ObjectId(sequence_id)})
            if sequence:
                if not email_payload.get("is_initial"):
                    thread_id = sequence.get("thread_id")
                    if thread_id:
                        try:
                            token_data = get_valid_token(user_email)
                            service = build_gmail_service(token_data)
                            thread = service.users().threads().get(
                                userId='me',
                                id=thread_id,
                                format='metadata',
                                metadataHeaders=['From']
                            ).execute()
                            
                            messages = thread.get('messages', [])
                            if len(messages) > 1:  # Has replies
                                for msg in messages[1:]:  # Skip first message
                                    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
                                    from_email = headers.get('From', '').lower()
                                    if email_payload.get('sender', '').lower() not in from_email:
                                        # Found reply, cancel sequence
                                        sequence_collection.update_one(
                                            {"_id": ObjectId(sequence_id)},
                                            {"$set": {
                                                "status": "COMPLETED",
                                                "completion_reason": "Recipient replied",
                                                "updated_at": datetime.utcnow()
                                            }}
                                        )

                                        # Update audit status
                                        if email_payload.get("audit_id"):
                                            sequence_audit_collection.update_one(
                                                {"_id": ObjectId(email_payload["audit_id"])},
                                                {"$set": {
                                                    "status": "CANCELLED",
                                                    "cancel_reason": "Recipient replied",
                                                    "updated_at": datetime.utcnow()
                                                }}
                                            )
                                        return {"status": "cancelled", "reason": "Recipient replied"}
                        except Exception as e:
                            logger.error(f"Error checking replies: {str(e)}")

                email_payload["thread_id"] = sequence.get("thread_id")

        # Send email
        token_data = get_valid_token(user_email, lookup_type="integration")
        result = send_email_from_user_email_sync(token_data, email_payload)

        # Update sequence and audit status
        if sequence_id:
            # Update thread ID if initial email
            if email_payload.get("is_initial") and result.get("threadId"):
                sequence_collection.update_one(
                    {"_id": ObjectId(sequence_id)},
                    {"$set": {
                        "thread_id": result["threadId"],
                        "status": "IN_PROGRESS",
                        "updated_at": datetime.utcnow()
                    }}
                )

            # Update audit status
            if email_payload.get("audit_id"):
                sequence_audit_collection.update_one(
                    {"_id": ObjectId(email_payload["audit_id"])},
                    {"$set": {
                        "status": "SENT",
                        "sent_time": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    }}
                )

            # Update sequence overall status
            from .sequence_utils import update_sequence_status_sync
            update_sequence_status_sync(sequence_id)

        return {"status": "sent", "result": result}

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}", exc_info=True)
        
        # Update audit status on failure
        if email_payload.get("audit_id"):
            sequence_audit_collection.update_one(
                {"_id": ObjectId(email_payload["audit_id"])},
                {"$set": {
                    "status": "FAILED",
                    "error_message": str(e),
                    "updated_at": datetime.utcnow()
                }}
            )
        raise

# Use a simpler singleton pattern
_task_restore_complete = False

@celery_app.task(bind=True, name='restore_persisted_tasks')
def restore_persisted_tasks(self):
    """Task to restore persisted tasks on worker startup."""
    global _task_restore_complete
    
    if (_task_restore_complete):
        logger.info("Tasks already restored, skipping...")
        return 0

    try:
        from .sequence_utils import restore_tasks  # Import here to avoid circular imports
        result = restore_tasks()
        _task_restore_complete = True
        return result
    except Exception as e:
        logger.error(f"Task restoration failed: {str(e)}")
        return 0

@signals.worker_ready.connect
def on_worker_ready(sender, **kwargs):
    """Run task restoration exactly once when worker is ready."""
    global _task_restore_complete
    if not _task_restore_complete:
        restore_persisted_tasks.apply_async(countdown=5)

@signals.task_sent.connect
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    """Handle task sent event."""
    task_id = headers.get('id') if headers else None
    if task_id:
        try:
            task_data = {
                'status': PENDING,
                'sent': datetime.utcnow().isoformat()
            }
            redis_client.set(
                f'flower:task:{task_id}',
                json.dumps(task_data),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_sent_handler: {str(e)}")

@signals.task_received.connect
def task_received_handler(sender=None, request=None, **kwargs):
    """Handle task received event."""
    if request and request.id:
        try:
            task_data = {
                'status': PENDING,
                'received': datetime.utcnow().isoformat()
            }
            redis_client.set(  # Now redis_client is properly imported
                f'flower:task:{request.id}',
                json.dumps(task_data),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_received_handler: {str(e)}")

@signals.task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    """Handle task success event."""
    if sender and sender.request.id:
        try:
            task_data = {
                'status': SUCCESS,
                'result': str(result),
                'completed': datetime.utcnow().isoformat()
            }
            redis_client.set(
                f'flower:task:{sender.request.id}',
                json.dumps(task_data),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_success_handler: {str(e)}")

@signals.task_failure.connect
def task_failure_handler(sender=None, exception=None, **kwargs):
    """Handle task failure event."""
    if sender and sender.request.id:
        try:
            task_data = {
                'status': FAILURE,
                'error': str(exception),
                'failed': datetime.utcnow().isoformat()
            }
            redis_client.set(
                f'flower:task:{sender.request.id}',
                json.dumps(task_data),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_failure_handler: {str(e)}")

# Export key components
__all__ = [
    'celery_app',
    'send_scheduled_email',
    'restore_persisted_tasks'
]