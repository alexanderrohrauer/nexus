from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    evaluation_mode: bool = False
    default_batch_size: int = 20
    openalex_batch_size: int = 20
    db: str = "nexus_dev"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
