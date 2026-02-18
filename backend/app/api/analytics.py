from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..db.session import get_db
from ..services.analytics import AnalyticsService
from .deps import get_current_user

router = APIRouter()

@router.get("/forecast", response_model=List[Dict[str, Any]])
async def get_forecast(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Returns a carbon footprint forecast for the next N days.
    Uses Machine Learning (Linear Regression) on historical data.
    """
    return AnalyticsService.predict_future_footprint(db, current_user, days)

@router.get("/anomalies", response_model=List[Dict[str, Any]])
async def get_anomalies(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Returns a list of anomalous activities (statistical outliers).
    Useful for flagging high-impact events.
    """
    return AnalyticsService.detect_anomalies(db, current_user)
