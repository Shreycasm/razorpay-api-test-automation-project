"""
Application configuration and environment variable management.

Configuration values are loaded from environment variables and validated
using Pydantic Settings.
"""

from typing import Literal

from pydantic import Field, HttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Define and validate application configuration.

    Configuration values are loaded from environment variables and validated
    using Pydantic Settings.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        env_file_encoding="utf-8"
    )

    base_url: HttpUrl = Field(...,alias="BASE_URL",)
    api_key: str = Field(...,alias="RAZORPAY_API_KEY",)
    api_key_secret: SecretStr = Field(...,alias="RAZORPAY_API_KEY_SECRET",)

    request_timeout_seconds: int = Field(
        default=30,
        gt=0,
        alias="REQUEST_TIMEOUT_SECONDS",
    )

    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = Field(
        ...,
        alias="LOG_LEVEL",
    )

    integration_post_delay_seconds: float = Field(
        default=0,
        ge=0,
        alias="INTEGRATION_POST_DELAY_SECONDS"
    )

    @field_validator("log_level", mode="before")
    @classmethod
    def __uppercase_log_level(cls, value: str) -> str:
        """Normalize the log level to uppercase before validation."""
        return value.upper()


settings = Settings()
