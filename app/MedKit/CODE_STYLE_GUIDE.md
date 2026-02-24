# MedKit Code Style Guide

## Python

- Follow PEP 8 conventions.
- Prefer explicit naming over abbreviations.
- Keep functions single-purpose and testable.

## Models and Prompts

- Keep Pydantic models close to module logic.
- Version prompt behavior carefully; avoid breaking output schemas.
- Preserve backward-compatible field names unless migration is documented.

## CLI Design

- Provide clear `--help` text.
- Validate inputs early with actionable error messages.
- Include one short and one realistic example in README.
