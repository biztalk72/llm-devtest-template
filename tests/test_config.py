"""Tests for configuration module."""

from src.config import Settings, get_settings


def test_settings_defaults() -> None:
    """Test that settings have correct defaults."""
    settings = Settings()

    assert settings.environment == "dev"
    assert settings.ollama_host == "http://localhost:11434"
    assert settings.api_port == 8000


def test_get_settings() -> None:
    """Test get_settings function."""
    settings = get_settings()

    assert isinstance(settings, Settings)
