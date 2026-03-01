# MedKit Article Tools

A collection of command-line tools for searching, processing, and analyzing medical articles using Large Language Models (LLMs). This project is part of the MedKit ecosystem.

## Unified CLI

The `medkit-article` command provides a single entry point for all article-related tasks.

### General Usage

```bash
medkit-article <subcommand> [args]
```

### Available Subcommands

| Subcommand | Description |
| :--- | :--- |
| **`list`** | List all available article modules and descriptions. |
| **`search`** | Search for medical articles using PubMed (via `biomcp`). |
| **`review`** | Perform structured reviews of medical articles using LLMs. |
| **`compare`** | Side-by-side comparison of two medical articles. |
| **`summarize`** | Generate cohesive summaries for long medical articles. |
| **`keywords`** | Extract precise medical keywords and terminology. |

---

## Project Modules

This repository contains several specialized modules:

### 1. [Article Search](./article_search/)
- **Description:** Search for medical articles using PubMed (via `biomcp`) and visualize results.
- **Key Features:** Disease-based search, citation formatting, JSON output, and Streamlit visualization.
- **CLI Command:** `medkit-article search "Diabetes"`

### 2. [Article Review](./article_review/)
- **Description:** Perform structured reviews of medical articles using LLMs.
- **Key Features:** Evaluates methodology, findings, clinical relevance, and assigns a quality score.
- **CLI Command:** `medkit-article review -f article.md`

### 3. [Article Comparison](./article_comparison/)
- **Description:** Side-by-side comparison of two medical articles.
- **Key Features:** Highlights complementary findings, evaluates relative strengths/weaknesses, and identifies the more comprehensive study.
- **CLI Command:** `medkit-article compare -f1 study1.md -f2 study2.md`

### 4. [Article Summary](./article_summary/)
- **Description:** Generate cohesive summaries for long medical articles.
- **Key Features:** Chunked processing with context-aware overlap to handle documents of any length.
- **CLI Command:** `medkit-article summarize -f large_article.txt`

### 5. [Article Keywords](./article_keywords/)
- **Description:** Extract precise medical keywords and terminology.
- **Key Features:** Categorizes findings into diseases, symptoms, medications, procedures, and anatomical terms.
- **CLI Command:** `medkit-article keywords -f article.md`

## Installation

### Prerequisites
- Python 3.10+
- Access to an LLM provider (e.g., [Ollama](https://ollama.com/) running `gemma3`, or API keys for Gemini/OpenAI).

### Setup
1. Clone the repository.
2. Install the required dependencies (ensure the `lite` package is available in your Python path):
   ```bash
   pip install pydantic litellm tqdm streamlit
   ```
3. Install the package in editable mode to enable the `medkit-article` command:
   ```bash
   pip install -e .
   ```

## Testing

The project includes unit tests for several modules. You can run them using `pytest` from within the respective module directory:

```bash
# Example: Run article_search tests
cd article_search
PYTHONPATH=. pytest tests/
```

## Development

- **Formatting:** The codebase follows `ruff` standards.
- **Logging:** Execution logs are saved in the `logs/` directory within each module.
- **Outputs:** Generated JSON results are saved in the `outputs/` directory within each module.
