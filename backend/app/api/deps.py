from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..auth.jwt_handler import JWTHandler
from ..core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
     reusable dependency to validate JWT and return the user ID.
    """
    payload = JWTHandler.decode_jwt(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload["user_id"]
