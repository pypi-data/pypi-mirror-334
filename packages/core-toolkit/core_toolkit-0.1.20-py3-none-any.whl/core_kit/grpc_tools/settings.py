import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "core_kit"
    GRPC_SERVICE_PORT: int = 8155

    model_config = SettingsConfigDict(
        env_file=os.environ.get("ENV_FILE_PATH", ".env"),
        extra="allow",
    )


settings = Settings()
