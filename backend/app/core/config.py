from typing import List, Union, Optional, Literal
from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class ServerSettings:
    """Settings related to the FastAPI server itself."""
    PROJECT_NAME: str = "EcoTwin"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True  # Default to True for dev; should be False in prod

class SecuritySettings(BaseSettings):
    """Settings related to authentication and cryptography."""
    SECRET_KEY: str  # Must be provided in env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

class DatabaseSettings(BaseSettings):
    """Settings related to database connections."""
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info) -> AnyHttpUrl:
        if isinstance(v, str):
            return v
        
        # Access values from the 'info' context or environment if validation fails
        # In Pydantic v2, cross-field validation is tricky within nested models without a root validator.
        # For simplicity and robustness, we rely on the environ or explicit construction.
        # A simpler pattern for enterprise usage is often just requiring the full DSN.
        return v or PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        )

class AISettings(BaseSettings):
    """Settings related to AI services."""
    GOOGLE_API_KEY: Optional[str] = None
    VECTOR_DB_URL: Optional[str] = None  # Future proofing

class Settings(BaseSettings):
    server: ServerSettings = ServerSettings()
    
    # We flatten these for simpler env var mapping (e.g. POSTGRES_USER maps directly)
    # But keeping them logically grouped in code is cleaner.
    # To make Pydantic settings work seamlessly with flat env vars, we'll keep it simple:
    
    # Core
    PROJECT_NAME: str = "EcoTwin"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    
    # Security
    SECRET_KEY: str = "CHANGEME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[PostgresDsn] = None

    # AI
    GOOGLE_API_KEY: Optional[str] = None
    REDIS_URL: RedisDsn = "redis://cache:6379/0"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info) -> AnyHttpUrl:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        )

    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=True,
        extra="ignore" # Ignore extra env vars
    )

settings = Settings()
