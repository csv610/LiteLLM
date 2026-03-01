# Medical Article Search

A command-line and Streamlit-ready tool for searching medical articles using PubMed (via the `biomcp` CLI). It formats results into structured data and provides citation-ready strings.

## Features

- **Search by Disease:** Find relevant articles from PubMed.
- **Structured Output:** Results available in human-readable text or JSON format.
- **Citation Generation:** Automatically formats articles into standard citation strings.
- **Streamlit Integration:** Includes a base for a web-based search interface.

## Project Structure

```text
article_search/
├── articles_search_cli.py     # Main command-line interface
├── biomcp_articles_search.py  # Core search logic using biomcp
├── articles_search_sl.py      # Streamlit interface
└── tests/                     # Unit tests
```

## Prerequisites

- Python 3.10+
- `biomcp` CLI tool installed and configured in your environment.

## Usage

### Command Line Interface

The main entry point is `articles_search_cli.py`.

#### 1. Search for Articles
```bash
python articles_search_cli.py search "diabetes"
```

#### 2. Get JSON Output
```bash
python articles_search_cli.py search "hypertension" --json
```

#### 3. Limit Number of Results
```bash
python articles_search_cli.py search "cancer" -n 5
```

#### 4. Get Formatted Citations
```bash
python articles_search_cli.py cite "alzheimer"
```

### Streamlit Application

To run the Streamlit interface (ensure `streamlit` is installed):

```bash
streamlit run articles_search_sl.py
```

## Testing

The module uses `pytest`. Run tests from the `article_search` directory:

```bash
PYTHONPATH=. pytest tests/
```
