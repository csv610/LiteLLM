#!/bin/bash
set -e

echo "Running tests..."
# Add parent directory to PYTHONPATH to ensure local package is found
PYTHONPATH=. pytest tests/
echo "Tests passed!"
