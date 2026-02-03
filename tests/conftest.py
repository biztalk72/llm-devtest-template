"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from src.config import Settings
from src.main import app


@pytest.fixture
def test_settings() -> Settings:
    """Create test settings."""
    return Settings(
        environment="test",
        test_mode=True,
        ollama_model="deepseek-coder:latest",
    )


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    return TestClient(app)
