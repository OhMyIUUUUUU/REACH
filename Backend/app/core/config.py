import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "../DB/.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "REACH Backend Service"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Server Binding (Default 8080 to match React Vite proxy)
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    # PostgreSQL Connection String
    DATABASE_URL: str = "postgresql://reach_user:reach_password@localhost:5432/reach_db"

    # JWT Authentication
    JWT_SECRET_KEY: str = "reach_super_secret_jwt_key_change_in_production_2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "*"
    ]

settings = Settings()
