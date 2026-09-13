from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    API_SECRET_KEY: SecretStr 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
        extra="ignore"
    )

settings = AppSettings()
