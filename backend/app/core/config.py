
from functools import lru_cache
from typing import Literal

from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    ###########################################################################
    # Environment
    ###########################################################################

    ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    DEBUG: bool = True

    LOG_LEVEL: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    ###########################################################################
    # API
    ###########################################################################

    API_V1_PREFIX: str = "/api/v1"

    PROJECT_NAME: str = "Pronunciation Scoring API"

    VERSION: str = "1.0.0"

    ###########################################################################
    # CORS
    ###########################################################################

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
    ]

    ###########################################################################
    # AI Providers
    ###########################################################################

    GROQ_API_KEY: str = Field(...)

    OPENAI_API_KEY: str | None = None

    ###########################################################################
    # Audio Validation
    ###########################################################################

    MAX_FILE_SIZE_MB: int = 8

    MIN_DURATION_SECONDS: int = 35

    MAX_DURATION_SECONDS: int = 40

    TARGET_SAMPLE_RATE: int = 16000

    TARGET_CHANNELS: int = 1

    ###########################################################################
    # Temporary Storage
    ###########################################################################

    TEMP_DIRECTORY: str = "/tmp"

    ###########################################################################
    # Rate Limiting
    ###########################################################################

    REQUESTS_PER_MINUTE: int = 10

    ###########################################################################
    # HTTP
    ###########################################################################

    HTTP_TIMEOUT_SECONDS: int = 30

    ###########################################################################
    # Validators
    ###########################################################################

    @field_validator("MAX_FILE_SIZE_MB")
    @classmethod
    def validate_file_size(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("MAX_FILE_SIZE_MB must be greater than zero.")
        return value

    @field_validator("MIN_DURATION_SECONDS")
    @classmethod
    def validate_min_duration(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("MIN_DURATION_SECONDS must be greater than zero.")
        return value

    @field_validator("MAX_DURATION_SECONDS")
    @classmethod
    def validate_max_duration(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("MAX_DURATION_SECONDS must be greater than zero.")
        return value

    @field_validator("TARGET_SAMPLE_RATE")
    @classmethod
    def validate_sample_rate(cls, value: int) -> int:
        if value not in (8000, 16000, 22050, 44100, 48000):
            raise ValueError("Unsupported sample rate.")
        return value

    @field_validator("TARGET_CHANNELS")
    @classmethod
    def validate_channels(cls, value: int) -> int:
        if value not in (1, 2):
            raise ValueError("TARGET_CHANNELS must be either mono (1) or stereo (2).")
        return value


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.

    Loaded only once during application lifetime.
    """

    try:
        return Settings()
    except ValidationError as exc:
        raise RuntimeError(
            "Configuration validation failed. "
            "Please check your .env file."
        ) from exc


settings = get_settings()