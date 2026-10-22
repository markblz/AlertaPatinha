from functools import lru_cache
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Process env only, no env_file: tests must never inherit a developer's .env.
    model_config = SettingsConfigDict(extra="ignore")

    env: str = "dev"
    database_url: str = "postgresql+asyncpg://alertapatinha:changeme@localhost:5440/alertapatinha"
    cors_origins: str = "http://localhost:3100"
    # Pilot city's zone. Brazil spans 4 zones: per-relato tz arrives with multi-city.
    default_tz: str = "America/Sao_Paulo"
    session_cookie_name: str = "ap_session"
    session_cookie_max_age_days: int = 400  # browsers cap cookie lifetime at ~400 days

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def tz(self) -> ZoneInfo:
        return ZoneInfo(self.default_tz)

    @property
    def secure_cookies(self) -> bool:
        return self.env not in ("dev", "test")


@lru_cache
def get_settings() -> Settings:
    return Settings()
