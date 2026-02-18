from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..services.activity_service import ActivityService

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def bulk_upload_activities(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Mass Ingestion Endpoint.
    Delegates logic to ActivityService.
    """
    try:
        count = await ActivityService.process_bulk_upload(file, db, current_user)
        return {"message": f"Successfully imported {count} activities."}

    except Exception as e:
        logger.error(f"Bulk import failed: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Bulk import failed: {str(e)}")
