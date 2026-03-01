# Medical Article Keyword Extraction

A command-line tool designed to extract precise medical terminology and keywords from text using Large Language Models (LLMs). This tool identifies and categorizes findings into structured medical domains.

## Features

- **Precise Extraction:** Identifies diseases, symptoms, medications, procedures, and anatomical terms.
- **Categorization:** Results are structured into logical medical categories.
- **Structured Output:** Uses Pydantic models to ensure consistent JSON results.
- **Bulk Processing:** Supports JSON arrays to process multiple items at once.
- **Flexible Input:** Supports plain text (.txt), Markdown (.md), and JSON (.json).

## Project Structure

```text
article_keywords/
├── cli.py                    # Command-line interface
├── keyword_extraction.py     # Core extraction logic
├── models.py                 # Pydantic data models
├── prompts.py                # LLM prompt templates
├── logs/                     # Execution logs
└── outputs/                  # Generated keyword JSON files
```

## Prerequisites

- Python 3.10+
- Access to an LLM provider (e.g., Ollama running `gemma3`, or an OpenAI/Gemini API key).

## Installation

1. Navigate to the project directory.
2. Ensure required dependencies are present:
   ```bash
   pip install pydantic tqdm
   ```

## Usage

### Basic Usage (Text Input)
```bash
python cli.py -t "Patient has hypertension, diabetes, and is prescribed Metformin."
```

### From a File
```bash
python cli.py -f article.md
```

### Specifying a Model
```bash
python cli.py -f notes.txt -m gemini/gemini-2.0-flash-exp
```

### Output

The full structured results are saved to the `outputs/` directory as JSON files, named based on the input file and the model used. For example, `article_keywords_ollama_gemma3.json`.
