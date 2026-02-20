# Unsolved Problems Explorer

A professional CLI tool and library designed to fetch, analyze, and document famous unsolved problems in various academic and scientific fields using Large Language Models (LLMs).

## Overview

The Unsolved Problems Explorer leverages advanced LLMs to provide structured, academically grounded information about open questions in fields such as Mathematics, Physics, Computer Science, and more. It utilizes a robust Pydantic-based data model to ensure consistency, accuracy, and ease of integration with other tools.

## Key Features

- **Structured Data Extraction**: Returns detailed information including problem title, description, field, difficulty, historical context, prize money, significance, and current status.
- **CLI Interface**: A user-friendly command-line interface for quick generation of reports.
- **Extensible Explorer Class**: A modular `UnsolvedProblemsExplorer` class that can be integrated into larger Python applications.
- **Schema Validation**: Rigorous validation of LLM responses against Pydantic models to ensure data integrity.
- **Automatic Documentation**: Automatically generates and saves reports in JSON format with organized naming conventions.

## Project Structure

- `unsolved_problems_cli.py`: Command-line interface and entry point.
- `unsolved_problems_explorer.py`: Core logic for interacting with LLM clients and managing data flow.
- `unsolved_problems_models.py`: Pydantic models defining the structure of problems and responses.
- `unsolved_problems_prompts.py`: Specialized prompt engineering for generating high-quality academic content.
- `outputs/`: Directory containing generated JSON reports.
- `logs/`: Application logs for debugging and monitoring.

## Prerequisites

- Python 3.10+
- Access to an LLM provider (e.g., Ollama, OpenAI, Anthropic) via the `lite` integration library.
- Environment variable `DEFAULT_LLM_MODEL` (optional, defaults to `ollama/gemma3`).

## Installation

Ensure the `lite` package is available in your Python environment. Install dependencies:

```bash
pip install pydantic
```

## Usage

### CLI

To fetch unsolved problems via the command line:

```bash
python unsolved_problems_cli.py -t "Mathematics" -n 5
```

**Arguments:**
- `-t`, `--topic`: The academic topic (e.g., "Physics", "Number Theory").
- `-n`, `--num-problems`: Number of problems to retrieve (1-50).
- `-m`, `--model`: (Optional) Specific LLM model to use.

### Programmatic Usage

```python
from unsolved_problems_explorer import UnsolvedProblemsExplorer

explorer = UnsolvedProblemsExplorer(model="ollama/gemma3")
problems = explorer.fetch_problems(topic="Cryptography", num_problems=3)

for problem in problems:
    print(f"Title: {problem.title}")
    print(f"Status: {problem.current_status}")
```

## Data Model

Each problem is captured with the following attributes:

| Field | Description |
| :--- | :--- |
| `title` | The name or title of the problem. |
| `description` | Clear explanation of the problem and its importance. |
| `field` | The specific academic subfield. |
| `difficulty` | Estimated level (Elementary, Moderate, Advanced). |
| `first_posed` | Historical context or proposer. |
| `prize_money` | Associated rewards, if any. |
| `significance` | Impact of a potential solution. |
| `current_status` | Latest known results and research progress. |

## License

This project is intended for educational and research purposes.
