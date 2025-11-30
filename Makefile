.PHONY: help venv venv-activate install install-dev test lint format clean run-cli-text run-cli-vision run-web-text run-web-vision

VENV_DIR := litenv
PYTHON := python3.12
PIP := $(VENV_DIR)/bin/pip
PYTHON_VENV := $(VENV_DIR)/bin/python

# Default target
help:
	@echo "LiteLLM - Makefile Commands"
	@echo "=============================="
	@echo ""
	@echo "Virtual Environment:"
	@echo "  make venv                 Create virtual environment"
	@echo "  make venv-activate        Show activation command"
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
	@echo "  make run-cli-text         Run CLI with list models"
	@echo "  make run-cli-vision       Run CLI help"
	@echo "  make run-web              Run web UI (Streamlit)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean                Remove cache and build files"
	@echo "  make clean-venv           Remove virtual environment"
	@echo "  make clean-all            Full cleanup (cache + venv)"
	@echo ""

# Virtual environment targets
venv:
	@if [ -d $(VENV_DIR) ]; then \
		echo "Virtual environment already exists at $(VENV_DIR)/"; \
	else \
		echo "Creating virtual environment (litenv)..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
		echo "Virtual environment created at $(VENV_DIR)/"; \
		echo "To activate, run: source $(VENV_DIR)/bin/activate (Linux/macOS) or $(VENV_DIR)\Scripts\activate (Windows)"; \
	fi

venv-activate:
	@echo "To activate the virtual environment, run:"
	@echo ""
	@echo "  source $(VENV_DIR)/bin/activate"
	@echo ""

# Installation targets
install: venv
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install --only-binary :all: pyarrow 2>/dev/null || true
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
	@echo "Dependencies installed in virtual environment"

install-dev: venv
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install --only-binary :all: pyarrow 2>/dev/null || true
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
	$(PIP) install pylint black pytest-cov
	@echo "Development dependencies installed in virtual environment"

# Testing and linting
test:
	$(PYTHON_VENV) -m pytest tests/ -v --cov=lite --cov-report=html

test-watch:
	$(PYTHON_VENV) -m pytest tests/ -v --tb=short -s

lint:
	$(VENV_DIR)/bin/pylint lite/ app/ tests/

format:
	$(VENV_DIR)/bin/black lite/ app/ tests/

# Running applications
run-cli-text:
	$(PYTHON_VENV) app/cli/liteclient_cli.py --list-models

run-cli-vision:
	$(PYTHON_VENV) app/cli/liteclient_cli.py --help

run-web:
	$(VENV_DIR)/bin/streamlit run app/web/streamlit_liteclient.py

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

clean-venv:
	rm -rf $(VENV_DIR)
	@echo "Removed virtual environment"

clean-all: clean clean-venv
	@echo "Full cleanup complete"
