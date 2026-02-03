"""Configuration management for different environments."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Environment
    environment: str = "dev"

    # Ollama Configuration
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3:latest"
    ollama_timeout: int = 300

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = True
    api_reload: bool = True

    # Database
    database_url: str = "sqlite:///./dev.db"

    # Logging
    log_level: str = "INFO"
    log_format: str = "detailed"

    # Feature Flags
    enable_cache: bool = False
    enable_metrics: bool = True

    # Testing
    test_mode: bool = False
    mock_ollama: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
