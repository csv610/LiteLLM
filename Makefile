.PHONY: help install install-dev test lint format clean run-cli-text run-cli-vision run-web-text run-web-vision

# Default target
help:
	@echo "LiteLLM - Makefile Commands"
	@echo "=============================="
	@echo ""
	@echo "Installation:"
	@echo "  make install              Install dependencies"
	@echo "  make install-dev          Install with development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test                 Run unit tests"
	@echo "  make lint                 Run code linting (pylint)"
	@echo "  make format               Format code with black"
	@echo ""
	@echo "Running Applications:"
	@echo "  make run-cli-text         Run LiteText CLI"
	@echo "  make run-cli-vision       Run LiteVision CLI"
	@echo "  make run-web-text         Run LiteText web UI (Streamlit)"
	@echo "  make run-web-vision       Run LiteVision web UI (Streamlit)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean                Remove cache and build files"
	@echo ""

# Installation targets
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pylint black pytest-cov

# Testing and linting
test:
	python -m pytest tests/ -v --cov=lite --cov-report=html

test-watch:
	python -m pytest tests/ -v --tb=short -s

lint:
	pylint lite/litellm_tools/ scripts/

format:
	black lite/ scripts/ tests/

# Running applications
run-cli-text:
	python scripts/cli_litetext.py --list-models

run-cli-vision:
	python scripts/cli_litevision.py --help

run-web-text:
	streamlit run scripts/streamlit_litetext.py

run-web-vision:
	streamlit run scripts/streamlit_litevision.py

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	find . -type f -name "temp_*" -delete
	@echo "Cleaned up cache and build files"
