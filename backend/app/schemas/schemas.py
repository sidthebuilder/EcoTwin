from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ActivityBase(BaseModel):
    user_id: str
    activity_type: str
    description: str
    timestamp: datetime
    raw_data_source: str

class ActivityInferenceRequest(BaseModel):
    raw_data: str  # Example: "Booking Confirmation for John, Location: JFK Airport, Time: 8:00 AM"

class ActivityResponse(ActivityBase):
    id: str
    carbon_estimate: float  # In kg CO2e
    confidence_score: float

class RecommendedAction(BaseModel):
    action: str
    potential_savings: float
    difficulty: str
