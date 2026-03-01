# Medical Article Comparison Tool

A command-line tool designed to compare two medical articles side-by-side using Large Language Models (LLMs) and structured output. It evaluates the strengths, weaknesses, and overall quality of each article, providing a summary of how they compare and complement each other.

## Features

- **Side-by-Side Evaluation**: Detailed assessment of research findings, methodology, and clinical implications.
- **Structured Output**: Uses Pydantic models to ensure consistent JSON results.
- **Flexible Input**: Supports `.txt`, `.md`, and `.json` file formats.
- **Model Agnostic**: Leverages `LiteClient` to support various models (default: `ollama/gemma3`).
- **Comprehensive Results**: Saves full evaluation details to a JSON file for further analysis.

## Project Structure

```text
article_comparison/
├── article_comparison.py        # Core logic for article comparison
├── article_comparison_cli.py    # Command-line interface
├── article_comparison_models.py # Pydantic data models
├── article_comparison_prompts.py # LLM prompt templates
├── logs/                        # Execution logs
├── outputs/                     # Generated comparison JSON files
└── tests/                       # Unit tests
```

## Prerequisites

- Python 3.10+
- Access to an LLM provider (e.g., Ollama running `gemma3`, or an OpenAI/Gemini API key configured in your environment).

## Installation

1. Navigate to the project directory.
2. Ensure the parent `lite` package and other dependencies are available in your Python environment.
3. Install required packages (if not already present):
   ```bash
   pip install pydantic
   ```

## Usage

Run the tool via the CLI by providing two article files:

```bash
python article_comparison_cli.py -f1 article1.md -f2 article2.md -m ollama/gemma3
```

### Arguments

- `-f1`, `--file1`: Path to the first article file (Required).
- `-f2`, `--file2`: Path to the second article file (Required).
- `-m`, `--model`: Model identifier for LiteClient (Default: `ollama/gemma3`).

### Output

- A summary of the comparison is printed to the console.
- Detailed results are saved in the `outputs/` directory as a JSON file, e.g., `comparison_article1_article2_ollama_gemma3.json`.

## Testing

The project uses `pytest` for unit testing. The tests mock the LLM client to ensure fast and reliable verification of the logic.

Run the tests with:

```bash
pytest tests/test_article_comparison.py
```

## Code Quality

The codebase is maintained using `ruff` for linting and formatting.

```bash
# Check for linting issues
ruff check .

# Format the code
ruff format .
```
