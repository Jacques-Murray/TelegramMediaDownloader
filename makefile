.PHONY: install dev test format lint type-check clean run examples help

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Install with development dependencies"
	@echo "  test        - Run tests"
	@echo "  format      - Format code with black and isort"
	@echo "  lint        - Run flake8 linting"
	@echo "  type-check  - Run mypy type checking"
	@echo "  check       - Run all checks (format, lint, type-check, test)"
	@echo "  clean       - Clean up build artifacts"
	@echo "  run         - Run the main application"
	@echo "  examples    - Run example scripts"
	@echo "  build       - Build package"

# Install dependencies
install:
	uv sync

# Install with development dependencies
dev:
	uv sync --extra dev

# Run tests
test:
	uv run pytest

# Format code
format:
	uv run black src/ tests/ examples/
	uv run isort src/ tests/ examples/

# Lint code
lint:
	uv run flake8 src/ tests/ examples/

# Type checking
type-check:
	uv run mypy src/

# Run all checks
check: format lint type-check test

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .mypy_cache/
	rm -rf htmlcov/ .coverage .coverage.*

# Run the main application
run:
	uv run python -m telegram_media_downloader.main

# Run example scripts
examples:
	@echo "Running basic example..."
	uv run python examples/basic_usage.py
	@echo "Running custom filter example..."
	uv run python examples/custom_filter.py
	@echo "Running custom namer example..."
	uv run python examples/custom_namer.py
	@echo "Running advanced example..."
	uv run python examples/advanced_usage.py

# Build package
build:
	uv build

# Install in development mode
install-dev:
	uv pip install -e .

# Update dependencies
update:
	uv sync --upgrade

# Run with specific log level
run-debug:
	LOG_LEVEL=DEBUG uv run python -m telegram_media_downloader.main

# Run specific example
run-basic:
	uv run python examples/basic_usage.py

run-custom-filter:
	uv run python examples/custom_filter.py

run-custom-namer:
	uv run python examples/custom_namer.py

run-advanced:
	uv run python examples/advanced_usage.py