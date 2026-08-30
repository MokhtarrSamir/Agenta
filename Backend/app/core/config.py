from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "RAG Agent Backend"
    APP_VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    MONGODB_URI: str
    MONGODB_DB_NAME: str

    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_PORT: int = 6333

    GROQ_API_KEY: str = ""
    TAVILY_API_KEY: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()