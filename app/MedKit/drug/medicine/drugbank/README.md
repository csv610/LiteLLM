# DrugBank Medicine Information Fetcher

This project provides a Python-based tool to fetch comprehensive and detailed information about medicines. It utilizes Large Language Models (LLMs) via the `LiteClient` to generate extensive reports on pharmacology, safety, interactions, regulatory data, and more.

## Features

*   **Comprehensive Data Retrieval**: Fetches detailed information including chemical properties, taxonomy, pharmacology, interactions, safety, and regulations.
*   **Flexible Output**: Supports both free-text (Markdown) reports and structured data (JSON) using Pydantic models.
*   **CLI Interface**: Easy-to-use command-line interface for quick lookups.
*   **Model Agnostic**: Compatible with various LLM backends (e.g., Ollama, Anthropic, etc.) via the `LiteClient` abstraction.

## Project Structure

*   `drugbank_medicine_cli.py`: The main entry point for the command-line interface. Handles argument parsing and output file management.
*   `drugbank_medicine.py`: Contains the `DrugBankMedicine` class, which manages the interaction with the LLM client.
*   `drugbank_medicine_models.py`: Defines the Pydantic data models used for structured output, ensuring type safety and consistent data schemas.

## Usage

You can run the tool directly from the command line.

### Basic Usage

Fetch a report for a specific medicine (defaults to `ollama/gemma3`):

```bash
python drugbank_medicine_cli.py "Aspirin"
```

### Specifying a Model

Use a different LLM model:

```bash
python drugbank_medicine_cli.py "Metformin" -m "anthropic/claude-3-5-sonnet"
```

### Structured Output

Request structured data (validated against Pydantic models) instead of a plain text report:

```bash
python drugbank_medicine_cli.py "Ibuprofen" --structured
```

### Adjusting Parameters

Control the temperature (creativity) and verbosity:

```bash
python drugbank_medicine_cli.py "Paracetamol" -t 0.1 -v 3
```

## Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `medicine` | | The name of the medicine to look up (e.g., 'Aspirin'). | Required |
| `--model` | `-m` | The LLM model to use. | `ollama/gemma3` |
| `--temperature` | `-t` | Sampling temperature (0.0 - 1.0). | `0.2` |
| `--verbosity` | `-v` | Logging verbosity level (0-4). | `2` |
| `--structured` | `-s` | Enforce structured output using Pydantic models. | `False` |
| `--json-output` | | Output results as JSON to stdout (flag only). | `False` |

## Output

Results are automatically saved to the `outputs/` directory:
*   **Markdown (.md)**: Standard text reports.
*   **JSON (.json)**: Structured data reports.

## Dependencies

*   Python 3.x
*   `pydantic`
*   `lite` (Internal library for LLM client handling)
