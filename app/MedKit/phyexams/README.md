# Physical Exams

This package contains multiple physical-exam and mental-status exam modules grouped under one CLI.

## Files

- `phyexams_cli.py`: unified CLI used by `medkit-exam`
- numerous `exam_*.py` modules for specific exam domains
- `pydantic_prompt_generator.py`: prompt/schema helper

## Why It Matters

The package organizes many exam-specific generators under one directory rather than dispersing them across unrelated modules.

## Limitations

- Generated exam content is educational and may not match local documentation standards.
- Clinical examination requires trained human performance and interpretation.
