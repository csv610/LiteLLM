# Medical Article Summary Tool

A command-line tool designed to process long medical articles and generate comprehensive, cohesive summaries using Large Language Models (LLMs). It uses a chunked processing strategy to handle documents of any length without losing context.

## Features

- **Cohesive Summarization:** Synthesizes a unified summary from multiple article sections.
- **Chunked Processing:** Splitting large documents into overlapping segments to maintain context.
- **Configurable Strategy:** Allows control over chunk size and overlap for different article types.
- **Structured Output:** Uses Pydantic models to ensure consistent JSON results.
- **Multi-format Support:** Processes plain text (.txt), Markdown (.md), and JSON (.json) files.

## Project Structure

```text
article_summary/
├── article_summary_cli.py      # Command-line interface
├── article_summary.py          # Core summarization logic with chunking
├── article_summary_models.py   # Pydantic data models
├── article_summary_prompts.py  # LLM prompt templates
├── logs/                       # Execution logs
└── outputs/                    # Generated summary JSON files
```

## Prerequisites

- Python 3.10+
- Access to an LLM provider (e.g., Ollama running `gemma3`, or an OpenAI/Gemini API key).

## Installation

1. Navigate to the project directory.
2. Ensure required dependencies are present:
   ```bash
   pip install pydantic tqdm litellm
   ```

## Usage

The main entry point is `article_summary_cli.py`.

### Basic Summarization
To summarize a medical article with default settings (100k chunk size):
```bash
python article_summary_cli.py -f article.md
```

### Advanced Summarization
You can control the chunking behavior for extremely large documents or specific context requirements:
```bash
python article_summary_cli.py -f large_document.txt --chunk-size 5000 --overlap 0.2
```

### Specify a Model
The tool defaults to `ollama/gemma3`, but you can specify any model supported by the `LiteClient`:
```bash
python article_summary_cli.py -f article.md -m gemini/gemini-2.0-flash-exp
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-f`, `--file` | Path to the input file (.txt, .md, .json) | Required (if no -t) |
| `-t`, `--text` | Direct text input | Required (if no -f) |
| `-m`, `--model` | LLM model identifier | `ollama/gemma3` |
| `--chunk-size` | Max characters per chunk | `100,000` |
| `--overlap` | Ratio of overlap between chunks (0.0 to 1.0) | `0.1` |

## Output

Results are saved to the `outputs/` directory as JSON files, named based on the input file and the model used. For example, `article_summary_ollama_gemma3.json`. Each result contains:
- `id`: Unique identifier for the item.
- `summary`: The generated cohesive summary.
