import asyncio
from typing import Dict, Any
from .worker import celery_app
from .services.inference_engine import InferenceEngine
from .core.logger import logger
from asgiref.sync import async_to_sync

# Instantiate engine once per worker process
inference_engine = InferenceEngine()

@celery_app.task(bind=True, name="analyze_activity_task")
def analyze_activity_task(self, raw_data: str, user_id: str) -> Dict[str, Any]:
    """
    Background task to run AI inference.
    Since Celery is sync by default, we wrap the async inference engine.
    """
    logger.info(f"Task {self.request.id}: Started inference for user {user_id}")
    try:
        # Run async function in sync context
        result = async_to_sync(inference_engine.run_inference)(raw_data)
        
        # Here you would typically save 'result' to the DB associated with 'user_id'
        # For PoC, we return it so it can be retrieved via Redis backend
        logger.info(f"Task {self.request.id}: Completed successfully.")
        return result
    except Exception as e:
        logger.error(f"Task {self.request.id}: Failed - {str(e)}")
        # Retry logic could go here
        raise e
