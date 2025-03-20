import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False
    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 10
    PREPARED_STATEMENT_CACHE_SIZE: int = 100
    STATEMENT_CACHE_SIZE: int = 100

    DATABASE_URL: str = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/core'
    TEST_DATABASE_URL: str = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/core_test'
    DATABASE_ECHO_MODE: bool = 0

    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE_PATH", ".env"),
        extra="allow",
    )


settings = Settings()
