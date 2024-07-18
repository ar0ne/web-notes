import logging

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    log_level: int = logging.WARNING
    env: str = "local"
    model_config = SettingsConfigDict(env_file=".env")

    max_connections_count: int = 10
    min_connections_count: int = 10

    mongodb_username: str
    mongodb_password: str
    mongodb_host: str = ""
    mongodb_port: int = 27017
    mongodb_database: str = "app"

    mongodb_note_collection: str = "notes"

    @property
    def mongodb_url(self) -> str:
        return f"mongodb://{self.mongodb_username}:{self.mongodb_password}@{self.mongodb_host}:{self.mongodb_port}/{self.mongodb_database}?retryWrites=true&w=majority&authSource=admin"


@lru_cache
def get_settings():
    return Settings()
