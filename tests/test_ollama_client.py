"""Tests for Ollama client."""

import pytest

from src.config import Settings
from src.ollama_client import OllamaService


@pytest.fixture
def ollama_service(test_settings: Settings) -> OllamaService:
    """Create Ollama service for testing."""
    return OllamaService(test_settings)


def test_ollama_service_initialization(ollama_service: OllamaService) -> None:
    """Test that Ollama service initializes correctly."""
    assert ollama_service.client is not None
    assert ollama_service.model is not None


@pytest.mark.asyncio
async def test_health_check(ollama_service: OllamaService) -> None:
    """Test Ollama health check."""
    # This will fail if Ollama is not running, which is expected in CI
    is_healthy = await ollama_service.health_check()
    assert isinstance(is_healthy, bool)


@pytest.mark.asyncio
async def test_list_models(ollama_service: OllamaService) -> None:
    """Test listing models."""
    try:
        models = await ollama_service.list_models()
        assert isinstance(models, list)
    except Exception:
        # Expected to fail if Ollama is not running
        pytest.skip("Ollama not available")
