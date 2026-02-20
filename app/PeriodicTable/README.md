# Periodic Table Element Information Fetcher

A CLI tool for fetching detailed, structured information about periodic table elements using Large Language Models (LLMs) via LiteLLM.

## Features

- **Comprehensive Data:** Fetches atomic properties, physical characteristics, chemical properties, isotopes, and more.
- **Structured Output:** Saves information in validated JSON format using Pydantic models.
- **LLM Powered:** Uses advanced models (defaults to `ollama/gemma3:12b`) to gather and structure scientific data.
- **Flexible CLI:** Fetch individual elements or the entire periodic table.

## Prerequisites

- **Python 3.10+**
- **Ollama** (if using the default local model)
- **LiteLLM** and other dependencies:
  ```bash
  pip install pydantic tqdm litellm
  ```

## Usage

### Basic Usage
By default, the script fetches information for **Hydrogen**:
```bash
python periodic_table_cli.py
```

### Fetch a Specific Element
Use the `-e` or `--element` flag:
```bash
python periodic_table_cli.py -e Gold
```

### Fetch All Elements
To fetch data for all 118 elements (this may take over 2 hours):
```bash
python periodic_table_cli.py --all
```

### Configuration Options
- `-m`, `--model`: Specify the model to use (default: `ollama/gemma3:12b`).
- `-t`, `--temperature`: Set the model temperature (default: `0.2`).
- `-o`, `--output-dir`: Specify the directory to save JSON files (default: `.`).

## Data Structure

Each element is saved as a JSON file (e.g., `Hydrogen.json`) with the following structure:

- **Core Identification:** Atomic number, symbol, name, atomic mass.
- **Periodic Table Position:** Period, group, block, category.
- **Electronic Structure:** Electron configuration (full and semantic).
- **Physical Characteristics:** Standard state, density, melting/boiling points, appearance.
- **Atomic Dimensions:** Various radius measurements (atomic, covalent, ionic, van der Waals).
- **Chemical Characteristics:** Oxidation states, reactivity, electronegativity, ionization energy.
- **Scientific Data:** Crystal structure, magnetic properties, thermal conductivity.
- **Occurrence & History:** Natural occurrence, abundance, isotopes, discovery info.
- **Applications & Safety:** Common uses, key properties, toxicity, and safety notes.

## Project Structure

- `periodic_table_cli.py`: The main command-line interface.
- `periodic_table_element.py`: Core logic for interacting with the LLM.
- `periodic_table_models.py`: Pydantic data models for validation and structure.
- `lite/`: Internal package for LLM client configuration (assumed structure).
