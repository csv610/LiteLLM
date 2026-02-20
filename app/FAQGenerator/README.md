# FAQGenerator

A production-grade, LLM-powered utility designed to generate academically rigorous and semantically diverse Frequently Asked Questions (FAQs) from either topical strings or existing document content.

## Overview

FAQGenerator leverages Advanced Large Language Models (via the `lite` client) to transform complex subjects into structured, verifiable Q&A pairs. Unlike naive prompt wrappers, this system implements rigorous quality constraints, multi-stage validation, and production-ready safety mechanisms.

## Key Features

- **Multi-Source Generation**: Generate FAQs from a simple topic (e.g., "Quantum Computing") or by analyzing local files (`.txt`, `.md`).
- **Academic Standard Prompting**: Implements strict requirements for objectivity, interrogative structure, and peer-reviewed verifiability.
- **Configurable Difficulty**: Supports four distinct cognitive levels: `simple`, `medium`, `hard`, and `research`.
- **Production Reliability**: 
    - **Transient Failure Recovery**: Automatic retry logic with exponential backoff for API flakiness.
    - **Security-First Design**: Path sanitization to prevent directory traversal and strict file size limits (5MB) to prevent resource exhaustion.
    - **Structured Data Integrity**: Uses Pydantic for schema validation of LLM outputs.
- **Comprehensive Observability**: Integrated with `lite.logging_config` for detailed execution tracing and error diagnostics.

## Architecture

- `faq_generator.py`: Core engine implementing generation logic, retry mechanisms, and file I/O.
- `faq_generator_cli.py`: Robust command-line interface with proactive argument validation.
- `faq_generator_models.py`: Centralized Pydantic schemas and shared constants.
- `faq_generator_prompts.py`: Component-based prompt engineering system.

## Installation

Ensure you have a Python 3.10+ environment and the `lite` package installed.

```bash
pip install -r requirements.txt # If available, otherwise ensure 'lite' is in path
```

## Usage

### Command Line Interface

```bash
# Generate 10 research-level FAQs from a topic
python faq_generator_cli.py --input "Distributed Systems" --num-faqs 10 --difficulty research

# Generate simple FAQs from a content file
python faq_generator_cli.py --input documentation.md --num-faqs 5 --difficulty simple --output ./results
```

### Argument Reference

| Argument | Shorthand | Description | Default |
| :--- | :--- | :--- | :--- |
| `--input` | `-i` | Topic string or path to content file | (Required) |
| `--num-faqs` | `-n` | Number of pairs to generate (1-100) | 5 |
| `--difficulty` | `-d` | Level: simple, medium, hard, research | medium |
| `--model` | `-m` | LLM identifier (e.g., `ollama/gemma3`) | `ollama/gemma3` |
| `--output` | `-o` | Target directory for JSON results | `.` |

## Security & Reliability

- **File Safety**: The system resolves absolute paths and enforces a 5MB limit to prevent Denial of Service (DoS) via large file inputs.
- **Output Sanitization**: Filenames are sanitized using regex to prevent path injection during the archive process.
- **Quality Assurance**: Implements a semantic check on generated content length to ensure the model does not return truncated or low-quality placeholders.

## Development & Testing

The project maintains a high-coverage test suite focusing on boundary conditions and failure recovery.

```bash
python -m unittest test_faq_generator.py
```

## License

Standard project licensing applies. See `LICENSE` for details.
