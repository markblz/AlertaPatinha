from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Process env only, no env_file: tests must never inherit a developer's .env.
    model_config = SettingsConfigDict(extra="ignore")

    env: str = "dev"
    database_url: str = "postgresql+asyncpg://alertapatinha:changeme@localhost:5440/alertapatinha"
    cors_origins: str = "http://localhost:3100"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
