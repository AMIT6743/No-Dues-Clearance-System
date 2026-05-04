import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./nodues.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-jwt-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    DEFAULT_ADMIN_EMAIL: Optional[str] = None
    DEFAULT_ADMIN_PASSWORD: Optional[str] = None
    DEFAULT_ADMIN_NAME: str = "System Admin"

    class Config:
        env_file = (".env", "backend/.env")

settings = Settings()
