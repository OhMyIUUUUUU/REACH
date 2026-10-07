import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "REACH NLP Service"
    APP_VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", "5000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")

    # ML & Model Config
    DEFAULT_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    DEVICE: str = "cpu"  # AMD Ryzen 5 5600G CPU inference

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
