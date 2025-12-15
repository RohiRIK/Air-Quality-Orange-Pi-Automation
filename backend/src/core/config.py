import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App Config
    DEVICE_ID: str = os.getenv("HOSTNAME", "unknown-device")
    READ_INTERVAL: float = 2.0

    # API Security
    API_SECRET: str = "dev-secret-key"

    # N8N Configuration
    N8N_WEBHOOK_URL_TEST: Optional[str] = None
    N8N_WEBHOOK_URL_PROD: Optional[str] = None
    N8N_CALENDAR_WEBHOOK_URL: Optional[str] = None

    # Google Calendar (OAuth)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_CALENDAR_ICS_URL: Optional[str] = None  # Legacy/Backup

    # Hardware Config
    I2C_DEVICE: str = "/dev/i2c-0"
    BLINKA_FORCEBOARD: str = "ORANGE_PI_3_LTS"

    @property
    def n8n_webhook_url(self) -> Optional[str]:
        """Returns the appropriate N8N webhook URL (Test priority)."""
        return self.N8N_WEBHOOK_URL_TEST or self.N8N_WEBHOOK_URL_PROD

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
