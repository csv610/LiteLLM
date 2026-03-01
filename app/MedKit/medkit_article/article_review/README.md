# Medical Article Reviewer

A command-line tool designed to perform structured reviews of medical articles using Large Language Models (LLM). This tool evaluates an article's methodology, findings, and clinical relevance, providing a detailed assessment of its strengths and weaknesses.

## Features

- **Structured Review:** Generates evaluations including title, summary, strengths, weaknesses, clinical implications, and an overall quality score.
- **Multi-format Support:** Accepts articles in `.txt`, `.md`, and `.json` formats.
- **LLM Integration:** Uses `LiteClient` to interface with various models (defaulting to `ollama/gemma3`).
- **Structured Output:** Saves full review results as JSON files for further analysis or integration.

## Project Structure

- `article_review_cli.py`: The command-line interface for running reviews.
- `article_review.py`: The core logic for loading articles and interacting with the LLM.
- `article_review_models.py`: Pydantic models defining the structured output format.
- `article_review_prompts.py`: Logic for building detailed review prompts.

## Usage

### Basic Command

To review an article, run the CLI with the path to your article file:

```bash
python article_review_cli.py -f path/to/article.md
```

### Specifying a Model

You can specify which LLM model to use via the `-m` flag:

```bash
python article_review_cli.py -f path/to/article.md -m gemini/gemini-2.0-flash-exp
```

### Arguments

- `-f`, `--file`: (Required) Path to the medical article file (.txt, .md, .json).
- `-m`, `--model`: (Optional) Model identifier for LiteClient (default: `ollama/gemma3`).

## Output

The tool prints a summary of the review to the console and saves the full structured result in the `./outputs/` directory as a JSON file.

### Example Console Output:

```text
--- Article Review: The Impact of Daily Exercise on Cardiovascular Health ---

Summary:
This study investigates the correlation between daily moderate exercise and cardiovascular health among individuals aged 65 and older...

Strengths:
  - Large sample size (1,000 participants)
  - Longitudinal study design (5 years)

Weaknesses:
  - Potential selection bias in volunteer participants
  - Reliance on self-reported activity levels in some phases

Clinical Implications:
Healthcare providers should encourage daily moderate exercise as it significantly improves cardiovascular markers in elderly patients.

Overall Quality: High
```

## Setup

Ensure you have the necessary dependencies installed and that the `lite` package (part of the broader MedKit ecosystem) is available in your Python path.

```bash
pip install pydantic
```
