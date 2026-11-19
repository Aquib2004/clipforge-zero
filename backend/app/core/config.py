"""Application configuration using Pydantic Settings.

Values are read from environment variables and an optional `.env` file.
Secrets (API keys, OAuth tokens) are intentionally NOT stored here — they
are managed through the UI Vault backed by the OS keychain.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Server — bound to loopback only by default
    host: str = Field("127.0.0.1", validation_alias="CLIPFORGE_HOST")
    port: int = Field(8765, validation_alias="CLIPFORGE_PORT")

    # Data directory — all user data stays local
    data_dir: str = Field("./data", validation_alias="CLIPFORGE_DATA_DIR")

    # Publishing safety
    default_visibility: str = Field("private", validation_alias="CLIPFORGE_DEFAULT_VISIBILITY")
    autopilot: bool = Field(False, validation_alias="CLIPFORGE_AUTOPILOT")


settings = Settings()
