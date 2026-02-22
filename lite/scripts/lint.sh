#!/bin/bash
set -e

echo "Running lint checks..."
ruff check .
echo "Checking formatting..."
ruff format --check .
echo "Linting complete!"
