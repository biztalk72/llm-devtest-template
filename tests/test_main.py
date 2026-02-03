"""Tests for main API endpoints."""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """Test root endpoint returns correct response."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "environment" in data
    assert "model" in data


def test_health_endpoint(client: TestClient) -> None:
    """Test health endpoint."""
    response = client.get("/health")

    # May fail if Ollama is not running, but should return valid response
    assert response.status_code in [200, 503]


def test_models_endpoint(client: TestClient) -> None:
    """Test models listing endpoint."""
    response = client.get("/models")

    # May fail if Ollama is not running
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "models" in data
        assert "current" in data
