import sys
from pydantic import SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from ..error import CustomError

class AppSettings(BaseSettings):
    ENVIRONMENT: str
    DATABASE_URL: str
    API_SECRET_KEY: SecretStr 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
        extra="ignore"
    )

try:
    settings = AppSettings()
except Exception as e:
    print(CustomError(__file__, e))
    sys.exit(1)

