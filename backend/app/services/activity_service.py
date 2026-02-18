import pandas as pd
import io
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from ..models.models import Activity
from ..core.logger import logger

class ActivityService:
    @staticmethod
    async def process_bulk_upload(file: UploadFile, db: Session, current_user_id: str) -> int:
        """
        Handles the business logic for bulk activity upload.
        Parses CSV, validates data, resolves user IDs, and performs bulk insertion.
        Returns the number of records inserted.
        """
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

        try:
            content = await file.read()
            df = pd.read_csv(io.BytesIO(content))
            
            required_cols = {'activity_type', 'description', 'carbon_estimate'}
            if not required_cols.issubset(df.columns):
                raise HTTPException(status_code=400, detail=f"CSV missing columns: {required_cols - set(df.columns)}")

            activities_to_insert = []
            for _, row in df.iterrows():
                target_uuid = ActivityService._resolve_user_id(row.get('user_id'), current_user_id)
                if not target_uuid:
                    continue

                activities_to_insert.append(Activity(
                    id=uuid.uuid4(),
                    user_id=target_uuid,
                    activity_type=row['activity_type'],
                    description=row['description'],
                    carbon_estimate=float(row['carbon_estimate']),
                    confidence_score=1.0, 
                    raw_data="bulk_import"
                ))

            if not activities_to_insert:
                 raise HTTPException(status_code=400, detail="No valid records found to insert.")

            db.bulk_save_objects(activities_to_insert)
            db.commit()
            
            logger.info(f"Bulk import success: {len(activities_to_insert)} records.")
            return len(activities_to_insert)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Bulk import failed: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Bulk import failed: {str(e)}")

    @staticmethod
    def _resolve_user_id(csv_user_id: Optional[str], current_user_id: str) -> Optional[uuid.UUID]:
        """
        Helper to resolve the target user UUID.
        Prioritizes CSV column, falls back to current authenticated user.
        """
        if not csv_user_id:
            try:
                return uuid.UUID(current_user_id)
            except ValueError:
                # Fallback for dev/test tokens that might not be valid UUIDs
                # In strict prod, this might be handled differently
                return uuid.UUID("00000000-0000-0000-0000-000000000000")
        
        try:
            return uuid.UUID(str(csv_user_id))
        except ValueError:
            return None

    @staticmethod
    def get_activities(db: Session, user_id: str, skip: int = 0, limit: int = 50) -> List[Activity]:
        """
        Retrieves a paginated list of activities for a specific user.
        """
        return db.query(Activity)\
            .filter(Activity.user_id == user_id)\
            .order_by(Activity.timestamp.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
