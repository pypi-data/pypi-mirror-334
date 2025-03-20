import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    JSON_LOGS: bool = False
    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE_PATH", ".env"),
        extra="allow",
    )


settings = Settings()
