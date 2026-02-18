from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..db.session import get_db
from ..core.config import settings
from ..db.neo4j_driver import neo4j_driver
import redis

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive Health Check.
    Verifies connectivity to:
    1. PostgreSQL (Primary DB)
    2. Redis (Cache/Queue)
    3. Neo4j (Graph DB)
    """
    health_status = {
        "status": "healthy",
        "components": {
            "postgres": "unknown",
            "redis": "unknown",
            "neo4j": "unknown"
        }
    }
    has_error = False

    # 1. Check PostgreSQL
    try:
        db.execute(text("SELECT 1"))
        health_status["components"]["postgres"] = "up"
    except Exception as e:
        health_status["components"]["postgres"] = f"down: {str(e)}"
        has_error = True

    # 2. Check Redis
    try:
        r = redis.from_url(settings.REDIS_URL, socket_timeout=1)
        if r.ping():
            health_status["components"]["redis"] = "up"
    except Exception as e:
        health_status["components"]["redis"] = f"down: {str(e)}"
        has_error = True

    # 3. Check Neo4j
    try:
        if neo4j_driver.verify_connectivity():
             health_status["components"]["neo4j"] = "up"
        else:
             health_status["components"]["neo4j"] = "down"
             has_error = True
    except Exception as e:
        health_status["components"]["neo4j"] = f"down: {str(e)}"
        has_error = True

    if has_error:
        health_status["status"] = "degraded"
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=health_status)
    
    return health_status
