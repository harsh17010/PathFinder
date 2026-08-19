from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://pathfinder:pathfinder@localhost:5432/pathfinder"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
