from typing import Optional
from celery import Celery
from pymongo.database import Database
from redis import Redis

class Dependencies:
    """Dependency container for major components."""
    _instance = None
    
    def __init__(self):
        self.celery_app: Optional[Celery] = None
        self.mongo_db: Optional[Database] = None
        self.redis_client: Optional[Redis] = None
        
        # Collections
        self.sequence_collection = None
        self.sequence_audit_collection = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Dependencies()
        return cls._instance
    
    def initialize(self, celery_app, mongo_db, redis_client):
        """Initialize all dependencies."""
        self.celery_app = celery_app
        self.mongo_db = mongo_db
        self.redis_client = redis_client
        
        # Initialize collections
        self.sequence_collection = self.mongo_db["email_sequences"]
        self.sequence_audit_collection = self.mongo_db["email_sequence_audits"]

# Create singleton instance
dependencies = Dependencies.get_instance()
