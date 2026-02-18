import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sklearn.linear_model import LinearRegression
from ..models.models import Activity
from ..core.logger import logger

class AnalyticsService:
    @staticmethod
    def get_time_series_data(db: Session, user_id: str, days: int = 30) -> pd.DataFrame:
        """
        Fetches activity data and resamples it to daily totals.
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        activities = db.query(Activity)\
            .filter(Activity.user_id == user_id, Activity.timestamp >= cutoff_date)\
            .all()
        
        if not activities:
            return pd.DataFrame(columns=['date', 'total_carbon', 'count'])

        data = [{'date': a.timestamp.date(), 'carbon': a.carbon_estimate} for a in activities]
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        
        # Group by date
        daily_df = df.groupby('date')['carbon'].agg(['sum', 'count']).reset_index()
        daily_df.rename(columns={'sum': 'total_carbon'}, inplace=True)
        
        # Fill missing days with 0
        idx = pd.date_range(cutoff_date.date(), datetime.utcnow().date())
        daily_df.set_index('date', inplace=True)
        daily_df = daily_df.reindex(idx, fill_value=0).reset_index().rename(columns={'index': 'date'})
        
        return daily_df

    @staticmethod
    def predict_future_footprint(db: Session, user_id: str, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """
        Predicts future carbon footprint using Linear Regression on past 30 days data.
        """
        df = AnalyticsService.get_time_series_data(db, user_id, days=60) # Use 60 days history for better trend
        
        if df['total_carbon'].sum() == 0:
            return []

        # Prepare features (Days since start)
        df['days_since'] = (df['date'] - df['date'].min()).dt.days
        X = df[['days_since']].values
        y = df['total_carbon'].values

        # Train Model
        model = LinearRegression()
        model.fit(X, y)

        # Predict
        last_day = df['days_since'].max()
        future_days = np.array([[last_day + i] for i in range(1, days_ahead + 1)])
        predictions = model.predict(future_days)
        
        # Format results
        future_dates = [df['date'].max() + timedelta(days=i) for i in range(1, days_ahead + 1)]
        
        result = []
        for date, pred in zip(future_dates, predictions):
            result.append({
                "date": date.strftime("%Y-%m-%d"),
                "predicted_carbon": max(0, round(pred, 2)) # No negative carbon
            })
            
        return result

    @staticmethod
    def detect_anomalies(db: Session, user_id: str) -> List[Dict[str, Any]]:
        """
        Detects activities that are statistical outliers (> 2 standard deviations from mean).
        """
        cutoff_date = datetime.utcnow() - timedelta(days=90)
        activities = db.query(Activity)\
            .filter(Activity.user_id == user_id, Activity.timestamp >= cutoff_date)\
            .all()
            
        if not activities:
            return []

        df = pd.DataFrame([{'id': str(a.id), 'carbon': a.carbon_estimate, 'desc': a.description, 'date': a.timestamp} for a in activities])
        
        mean = df['carbon'].mean()
        std = df['carbon'].std()
        
        if std == 0:
            return []
            
        # Z-Score
        df['z_score'] = (df['carbon'] - mean) / std
        
        # Anomaly = Z-Score > 2 (Top 5% outliers)
        anomalies = df[df['z_score'] > 2].sort_values('carbon', ascending=False).head(5)
        
        return anomalies[['id', 'desc', 'carbon', 'date']].to_dict('records')
