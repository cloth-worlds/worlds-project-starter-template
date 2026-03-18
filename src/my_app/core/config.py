"""Configuration models using Pydantic."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIConfig(BaseSettings):
    """Configuration for API authentication."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="API_",
    )

    bearer_token: str = Field(..., description="Bearer token for API authentication")


class AppConfig(BaseSettings):
    """Configuration for My Project Name service.

    Env vars are prefixed with MY_APP_ (e.g. MY_APP_HTTP_ENDPOINT).
    Rename this class and update env_prefix for your project.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="MY_APP_",
    )

    # GraphQL API Configuration
    http_endpoint: str = Field(..., description="GraphQL HTTP endpoint URL")
    ws_endpoint: str = Field(..., description="GraphQL WebSocket endpoint URL")
    token_id: str = Field(..., description="Authentication token ID")
    token_value: str = Field(..., description="Authentication token value")

    # Environment Mode
    env: str = Field(default="development", description="Environment mode (development/production)")


class UvicornConfig(BaseSettings):
    """Configuration for Uvicorn server."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    HOT_RELOAD: bool = Field(default=False, description="Enable/disable hot-reloading for Uvicorn")
