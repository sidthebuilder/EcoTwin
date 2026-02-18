rom sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Enterprise grade: Use connection pooling
engine = create_engine(
    str(settings.DATABASE_URL),
    pool_pre_ping=True,
    pool_size=40,        # Tuned for high concurrency
    max_overflow=20,     # Allow burst traffic
    pool_recycle=1800    # Recycle connections every 30 mins to prevent stale connections
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
