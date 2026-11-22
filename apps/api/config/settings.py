from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "GitVerse Core Engine"
    ENVIRONMENT: str = "development"
    GITHUB_TOKEN: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    CACHE_TTL_SECONDS: int = 3600  # 1 hour cache TTL

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()