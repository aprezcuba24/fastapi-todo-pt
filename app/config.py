from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    API_PREFIX: str = "/api/v1"
    SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
