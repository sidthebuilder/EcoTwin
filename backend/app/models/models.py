import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Efficient access to activities
    activities = relationship("Activity", back_populates="owner", cascade="all, delete-orphan")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    activity_type = Column(String, index=True)  # Indexed for filtering (e.g. "Show only Travel")
    description = Column(String)
    raw_data = Column(Text)  # Store original data for audit
    
    carbon_estimate = Column(Float, nullable=False)
    confidence_score = Column(Float)
    
    timestamp = Column(DateTime(timezone=True), default=func.now(), index=True) # Critical for time-series queries

    owner = relationship("User", back_populates="activities")

    # Composite index for common query pattern: "Get user's activities sorted by time"
    __table_args__ = (
        Index('idx_user_timestamp', 'user_id', 'timestamp'),
    )

class AuditLog(Base):
    """
    Enterprise requirement: Track who accessed what data.
    Partitioning Candidate in Postgres 10+ (Partition by Range on timestamp)
    """
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action = Column(String, nullable=False)
    target_resource = Column(String)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
