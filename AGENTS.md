# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python template for building web applications and APIs with LLM integration using Ollama. The architecture follows a multi-environment pattern (dev/test/prod) with FastAPI for the web layer and async Ollama client for LLM interactions.

### Core Architecture

**Configuration Layer** (`src/config.py`):
- Pydantic-based settings management using `pydantic_settings`
- Environment-specific configuration loaded from `.env` files
- All settings are type-safe with defaults
- Settings singleton accessed via `get_settings()`

**API Layer** (`src/main.py`):
- FastAPI application with async endpoints
- Global `ollama_service` instance initialized at module level
- Pydantic models for request/response validation
- Supports both streaming and non-streaming responses

**LLM Integration** (`src/ollama_client.py`):
- `OllamaService` class wraps Ollama's `AsyncClient`
- All methods are async
- Health checks validate Ollama connectivity before operations
- Model selection controlled via settings

### Environment Strategy

The codebase uses three environments with distinct configurations:
- **dev** (`.env.dev.example`): Uses `kimi2.5:latest` (main LLM), debug enabled, verbose logging
- **test** (`.env.test.example`): Uses `deepseek-coder:latest`, test mode enabled
- **prod** (`.env.prod.example`): Uses `kimi2.5:latest` (main LLM), production settings with minimal logging

Always copy the appropriate `.env.*.example` to `.env` before running.

### Branch Workflow

- `main`: Production-ready code (protected)
- `dev`: Primary development branch (auto-deploys to dev environment)
- `test`: Testing branch (auto-deploys to test environment)
- Feature branches: Always branch from `dev`, PR back to `dev`

All commits are GPG-signed automatically via git config.

## Common Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies (including dev)
pip install -r requirements-dev.txt

# Set up dev environment
cp .env.dev.example .env
```

### Running the Application
```bash
# Development mode (auto-reload enabled)
python src/main.py

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Custom environment
ENVIRONMENT=test uvicorn src.main:app
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_main.py -v

# Run single test function
pytest tests/test_main.py::test_root_endpoint -v

# Run with coverage report
pytest --cov=src --cov-report=html

# Run tests with specific environment
ENVIRONMENT=test pytest
```

### Code Quality
```bash
# Format code (modifies files)
black src/ tests/

# Lint code (read-only check)
ruff check src/ tests/

# Type check (mypy may show errors due to missing type stubs)
mypy src/

# Run all quality checks
black src/ tests/ && ruff check src/ tests/ && mypy src/

# Auto-fix linting issues
ruff check --fix src/ tests/
```

### Ollama Management
```bash
# Verify Ollama is running
ollama list

# Pull required models
ollama pull kimi2.5:latest
ollama pull deepseek-coder:latest

# Test Ollama connectivity
curl http://localhost:11434/api/tags
```

## Code Patterns

### Adding New API Endpoints

When adding endpoints to `src/main.py`:
1. Define Pydantic request/response models as classes
2. Use type hints for all parameters and return types
3. Add docstrings to endpoint functions
4. Handle Ollama errors with try/except, raise HTTPException with appropriate status codes
5. For async Ollama calls, use `await ollama_service.method()`

### Configuration Changes

When adding new settings to `src/config.py`:
1. Add field to `Settings` class with type hint and default value
2. Update all three `.env.*.example` files with the new variable
3. Settings are automatically loaded from `.env` (no restart needed for Pydantic)

### Testing Patterns

- Use pytest fixtures from `tests/conftest.py`
- `client` fixture provides FastAPI TestClient
- `test_settings` fixture provides test-specific settings
- Ollama-dependent tests should gracefully handle Ollama being unavailable (pytest.skip)
- Async tests require `@pytest.mark.asyncio` decorator

### Import Patterns

Always use absolute imports from `src`:
```python
from src.config import get_settings
from src.ollama_client import OllamaService
```

Never use relative imports outside the `src` package.

## Style Guidelines

- **Line length**: 100 characters (configured in pyproject.toml)
- **Type hints**: Required for all function parameters and returns (mypy enforces `disallow_untyped_defs`)
- **Docstrings**: Required for all public functions and classes
- **Formatting**: Black with default config
- **Import order**: Enforced by ruff (stdlib, third-party, local)

## CI/CD Behavior

GitHub Actions workflows:
- **ci.yml**: Runs on all pushes/PRs to main/dev/test - tests, linting, type checking across Python 3.10, 3.11, 3.12
- **deploy-dev.yml**: Triggers on push to `dev` branch
- **deploy-test.yml**: Triggers on push to `test` branch

All workflows run pytest but actual deployment steps are placeholders (see workflow files for where to add deployment logic).

## Dependencies Management

- `requirements.txt`: Production dependencies only (FastAPI, Ollama, Pydantic, etc.)
- `requirements-dev.txt`: Includes production deps + testing/quality tools

When adding dependencies:
1. Add to appropriate file with version constraint (e.g., `package>=1.0.0`)
2. Run `pip install -r requirements-dev.txt`
3. Update pyproject.toml `requires-python` if minimum Python version changes

## Common Pitfalls

- **Ollama must be running**: The app won't start if Ollama isn't accessible at `OLLAMA_HOST`
- **Virtual environment**: Always activate venv before installing packages or running commands
- **Environment files**: Don't commit `.env` files (only `.env.*.example` files)
- **GPG signing**: Commits will fail if GPG isn't properly configured (see README troubleshooting)
- **Type checking**: mypy is strict (`disallow_untyped_defs=true`) - all functions need type hints
- **Async/await**: All Ollama client methods are async - must use `await`
