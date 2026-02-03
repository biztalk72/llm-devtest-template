# Contributing Guide

Thank you for contributing to the LLM DevTest Template! This guide will help you get started.

## Development Workflow

### 1. Setup Your Environment

```bash
# Clone the repository
git clone <repo-url>
cd llm-devtest-template

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Copy environment file
cp .env.dev.example .env
```

### 2. Create a Feature Branch

Always branch from `dev`:

```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/improvements

### 3. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new features
- Update documentation as needed
- Keep commits focused and atomic

### 4. Test Your Changes

Before committing, run:

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/

# Run tests
pytest -v
```

### 5. Commit Your Changes

Commits are automatically GPG signed. Write clear commit messages:

```bash
git add .
git commit -m "feat: add new LLM generation endpoint"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a PR on GitHub:
- Target branch: `dev`
- Fill out the PR template
- Link any related issues
- Request reviews

## Code Standards

### Python Style

- Line length: 100 characters
- Use type hints
- Write docstrings for functions/classes
- Follow PEP 8 guidelines

Example:

```python
def generate_text(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> str:
    """Generate text from a prompt.
    
    Args:
        prompt: The input prompt
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens to generate
        
    Returns:
        Generated text string
    """
    # Implementation
```

### Testing

- Write tests for all new features
- Aim for >80% code coverage
- Use descriptive test names
- Include edge cases

Example:

```python
def test_generate_with_custom_temperature() -> None:
    """Test text generation with custom temperature setting."""
    # Test implementation
```

### Documentation

- Update README.md for new features
- Add docstrings to all functions/classes
- Include usage examples
- Document environment variables

## Pull Request Process

### PR Checklist

Before submitting your PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts with target branch
- [ ] Commit messages are clear and descriptive

### Review Process

1. CI checks run automatically
   - All tests must pass
   - Code must pass linting
   - Coverage maintained or improved

2. Code review by maintainer
   - Review feedback addressed
   - Changes approved

3. Merge to target branch
   - Squash and merge for feature branches
   - Include PR number in merge commit

## Environment-Specific Guidelines

### Development Environment

- Use `dev` branch
- Test against local Ollama
- Enable debug logging
- Frequent commits encouraged

### Test Environment

- Use `test` branch
- Run full test suite
- Test with production-like data
- Document test scenarios

### Production

- Only merge tested code
- Update version numbers
- Tag releases
- Monitor after deployment

## Getting Help

- Check existing issues and PRs
- Review documentation
- Ask questions in discussions
- Contact maintainers

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow community guidelines

## Recognition

Contributors will be recognized in:
- README.md
- Release notes
- Project documentation

Thank you for contributing! 🚀
