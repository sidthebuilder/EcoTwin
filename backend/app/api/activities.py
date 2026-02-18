@router.get("/", response_model=List[ActivityResponse])
async def list_activities(
    skip: int = 0, 
    limit: int = 50, 
    activity_type: Optional[str] = None,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get activities with enterprise-grade pagination.
    Default limit is 50 to prevent memory overruns on large datasets.
    """
    query = db.query(Activity).filter(Activity.user_id == current_user)
    
    if activity_type:
        query = query.filter(Activity.activity_type == activity_type)
    
    # High-performance sorted paging
    activities = query.order_by(Activity.timestamp.desc()).offset(skip).limit(limit).all()
    
    return activities

router = APIRouter()
from .deps import get_current_user

@router.post("/infer", status_code=202)
async def infer_activity(request: ActivityInferenceRequest, current_user: str = Depends(get_current_user)):
    """
    Async Inference: Submits data to the queue and returns a Task ID.
    Clients should poll /infer/{task_id} for results.
    """
    task = analyze_activity_task.delay(request.raw_data, current_user)
    return {"task_id": task.id, "status": "processing"}

@router.get("/infer/{task_id}")
async def get_inference_result(task_id: str, current_user: str = Depends(get_current_user)):
    task_result = AsyncResult(task_id)
    
    if task_result.state == 'PENDING':
        return {"task_id": task_id, "status": "processing"}
    elif task_result.state == 'SUCCESS':
        return {"task_id": task_id, "status": "completed", "result": task_result.result}
    elif task_result.state == 'FAILURE':
        return {"task_id": task_id, "status": "failed", "error": str(task_result.info)}
    
    return {"task_id": task_id, "status": task_result.state}
