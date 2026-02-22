#!/bin/bash
set -e

echo "Formatting code..."
ruff format .
ruff check --fix .
echo "Code formatted!"
