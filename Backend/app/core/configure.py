
### Meaning:
"""
- Imports caching utility.
- `lru_cache` stores function results in memory.

### Why it is used:
- Prevents reloading settings multiple times.
- Configuration is expensive to rebuild repeatedly.

---
"""
"""
Application Configuration

This module centralizes all application settings.

Responsibilities:
- Load environment variables
- Validate configuration
- Provide a single settings object
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.

    Values are loaded automatically from the .env file.
    """

    APP_NAME: str = Field(
        default="Enterprise Hybrid RAG + Text-to-SQL AI Chatbot",
        description="Application name",
    )
    
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Expiration time"
    )
    
    JWT_SECRET_KEY: str=Field(
        default="Demokeypresented",
        description="Jwt secret key_Demo",
    )

    
    JWT_ALGORITHM: str=Field(
        default="HS256",
        description="Algorithm",
    )
    DATABASE_URL:str=Field(
        default="jashka",
        description="DATABASE_URL "
    )


    APP_VERSION: str = Field(
        default="1.0.0",
        description="Application version",
    )

    DEBUG: bool = Field(
        default=True,
        description="Enable debug mode",
    )

    HOST: str = Field(
        default="127.0.0.1",
        description="Application host",
    )

    PORT: int = Field(
        default=8000,
        description="Application port",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    Using lru_cache ensures the configuration is loaded only once.
    """
    return Settings()


settings = get_settings()