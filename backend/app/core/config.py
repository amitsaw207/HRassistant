from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HR Policy Assistant"
    app_env: str = "development"
    log_level: str = "INFO"

    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_chat_deployment: str
    azure_openai_embedding_deployment: str

    chroma_persist_directory: str = "../data/chroma"
    upload_directory: str = "../data/uploads"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def chroma_path(self) -> Path:
        return Path(self.chroma_persist_directory)

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_directory)


settings = Settings()