# LLM DevTest Template

A production-ready template for building Python web applications and APIs with LLM integration using Ollama. Includes complete dev/test environment setup with CI/CD automation via GitHub Actions.

## Features

- 🤖 **Ollama Integration**: Ready-to-use LLM client with async support
- 🚀 **FastAPI Backend**: Modern, fast API framework with automatic docs
- 🧪 **Complete Testing**: Pytest setup with coverage reporting
- 🔄 **CI/CD Pipeline**: Automated testing and deployment via GitHub Actions
- 🌍 **Multi-Environment**: Separate configurations for dev/test/prod
- 🔐 **GPG Signing**: Commits automatically signed for security
- 📊 **Code Quality**: Black, Ruff, and MyPy configured

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running
- Git with GPG configured (for commit signing)

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd llm-devtest-template
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

### 2. Configure Environment

Copy the appropriate environment file:

```bash
# For development
cp .env.dev.example .env

# For testing
cp .env.test.example .env

# For production
cp .env.prod.example .env
```

Edit `.env` with your specific settings.

### 3. Run the Application

```bash
# Development mode (with auto-reload)
python src/main.py

# Or using uvicorn directly
uvicorn src.main:app --reload
```

API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_main.py -v
```

## Project Structure

```
llm-devtest-template/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
│       ├── ci.yml         # Automated testing
│       ├── deploy-dev.yml # Dev deployment
│       └── deploy-test.yml# Test deployment
├── src/
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   ├── config.py          # Configuration management
│   └── ollama_client.py   # Ollama LLM integration
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures
│   ├── test_config.py
│   ├── test_main.py
│   └── test_ollama_client.py
├── .env.*.example         # Environment templates
├── .gitignore
├── pyproject.toml         # Project configuration
├── requirements.txt       # Production dependencies
└── requirements-dev.txt   # Development dependencies
```

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with service info
- `GET /health` - Health check (includes Ollama status)
- `GET /models` - List available Ollama models

### LLM Endpoints

- `POST /generate` - Generate text from a prompt

**Example Request:**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms",
    "temperature": 0.7,
    "stream": false
  }'
```

## Branch Strategy

- `main` - Production-ready code (protected)
- `dev` - Development branch (auto-deploys to dev environment)
- `test` - Testing branch (auto-deploys to test environment)

### Workflow

1. Create feature branch from `dev`
2. Make changes and commit (will be GPG signed)
3. Push and create PR to `dev`
4. CI runs automatically (tests, linting, type checking)
5. After merge to `dev`, auto-deploy to dev environment
6. Merge to `test` for testing environment
7. Merge to `main` for production

## Environment Variables

### Development (.env.dev)

- `OLLAMA_MODEL=llama3:latest` - Fast, general-purpose model
- `API_DEBUG=true` - Enable debug mode
- `LOG_LEVEL=DEBUG` - Verbose logging

### Test (.env.test)

- `OLLAMA_MODEL=deepseek-coder:latest` - Optimized for testing
- `TEST_MODE=true` - Enable test-specific features
- `LOG_LEVEL=INFO` - Standard logging

### Production (.env.prod)

- `OLLAMA_MODEL=llama3:latest` - Production model
- `API_DEBUG=false` - Disable debug mode
- `LOG_LEVEL=WARNING` - Minimal logging

## Development

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/

# Run all checks
black src/ tests/ && ruff check src/ tests/ && mypy src/
```

### Adding Dependencies

```bash
# Add to requirements.txt for production
echo "package-name>=1.0.0" >> requirements.txt

# Add to requirements-dev.txt for development only
echo "package-name>=1.0.0" >> requirements-dev.txt

# Install
pip install -r requirements-dev.txt
```

## CI/CD

### GitHub Actions Workflows

1. **CI** (`ci.yml`) - Runs on every push/PR
   - Tests across Python 3.10, 3.11, 3.12
   - Linting with Ruff
   - Format checking with Black
   - Type checking with MyPy
   - Coverage reporting

2. **Deploy to Dev** (`deploy-dev.yml`) - Runs on push to `dev`
   - Runs tests
   - Deploys to dev environment

3. **Deploy to Test** (`deploy-test.yml`) - Runs on push to `test`
   - Runs full test suite with coverage
   - Integration tests
   - Deploys to test environment

## Ollama Models

Recommended models for different use cases:

- **Development**: `llama3:latest` (balanced speed/quality)
- **Testing**: `deepseek-coder:latest` (fast, code-focused)
- **Production**: `llama3:latest` or `mistral:latest` (stable)

Pull new models:

```bash
ollama pull llama3:latest
ollama pull deepseek-coder:latest
ollama pull mistral:latest
```

## Troubleshooting

### Ollama Not Connected

```bash
# Check if Ollama is running
ollama list

# Start Ollama (if needed)
ollama serve
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements-dev.txt --force-reinstall
```

### GPG Signing Issues

```bash
# Verify GPG key
git config --global user.signingkey

# Test GPG
echo "test" | gpg --clearsign
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT License - see LICENSE file for details.

## Author

Brian (re3539@outlook.com)

---

**Co-Authored-By: Warp <agent@warp.dev>**
