# Nobel Prize Winners Explorer

A sophisticated Python-based tool for fetching, analyzing, and exploring detailed Nobel Prize winner information. This project leverages Large Language Models (LLMs) via the `lite` library to provide structured, objective, and educational data about laureates and their scientific contributions.

## Overview

The Nobel Prize Winners Explorer is designed for researchers, educators, and science enthusiasts who need more than just a list of names. It provides a deep dive into the lives, careers, and scientific impact of Nobel laureates, focusing on factual accuracy and objective analysis.

## Key Features

- **Structured Data Models**: Uses Pydantic to ensure all fetched data adheres to a strict, typed schema.
- **Biographical Depth**: Captures early life, education, mentors, and complete career timelines.
- **Scientific Impact Analysis**:
    - Factual history of discoveries.
    - Measurable impact on scientific understanding.
    - Cross-disciplinary influence and foundational roles.
    - Verified real-world applications.
- **Educational Resources**: Automatically generates glossaries, FAQs, and learning objectives for each discovery.
- **Multi-Model Support**: Compatible with various LLMs (defaulting to Google Gemini) through the `lite` package.
- **Objective Focus**: Prompt engineering specifically designed to eliminate superlatives and subjective language in favor of technical and historical facts.

## Architecture

The codebase is organized into several modular components:

- **`nobel_prize_cli.py`**: The primary command-line interface for the tool.
- **`nobel_prize_info.py`**: A high-level entry point for fetching winner information.
- **`nobel_prize_explorer.py`**: Contains the `NobelPrizeWinnerInfo` class, which handles LLM communication and data validation.
- **`nobel_prize_models.py`**: Defines the `PrizeWinner`, `CareerPosition`, `PersonalBackground`, and other Pydantic models.
- **`nobel_prize_prompts.py`**: Encapsulates the logic for building expert-level prompts for factual data retrieval.

## Installation

### Prerequisites

- Python 3.10 or higher
- Access to an LLM (e.g., Google Gemini API key)
- The `lite` internal library (ensure it is in your `PYTHONPATH`)

### Setup

1. Clone the repository and navigate to the project directory:
   ```bash
   cd NobelPrizeWinners
   ```

2. Install dependencies:
   ```bash
   pip install pydantic
   ```

3. Set up your environment variables:
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   export NOBEL_PRIZE_MODEL="gemini/gemini-2.0-flash" # Optional
   ```

## Usage

Run the CLI to fetch information for a specific category and year:

```bash
python nobel_prize_cli.py -c Physics -y 2023
```

### Options

- `-c`, `--category`: Nobel Prize category (Physics, Chemistry, Medicine, Literature, Peace, Economics).
- `-y`, `--year`: Year of the prize (1901 onwards).
- `-m`, `--model`: (Optional) LLM model to use (e.g., `gemini/gemini-2.0-flash`, `claude-3-opus`).

### Example

```bash
python nobel_prize_cli.py --category Chemistry --year 2022 --model gemini/gemini-2.5-flash
```

## Data Structure

The tool returns a comprehensive JSON-compatible structure (via Pydantic) containing:

- **Personal Background**: Birth details, nationality, family, and education.
- **Career Timeline**: Positions, institutions, and roles.
- **Scientific Work**: Discovery details, impact, foundation, and applications.
- **Educational Content**: Keywords, learning objectives, FAQ, and a glossary.

## License

Objective and educational use encouraged.
