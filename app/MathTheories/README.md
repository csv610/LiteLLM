# Math Theory Explainer

This tool generates comprehensive explanations for mathematical theories tailored to different audience levels, from a general audience (no math background) to specialized researchers.

## Features

- **Multi-Level Explanations**: Provides content for:
  - General (No math background)
  - High School
  - Undergrad (Default)
  - Master
  - PhD
  - Researcher
- **Comprehensive Coverage**: Each explanation includes:
  - Introduction
  - Key concepts (Fundamental building blocks)
  - Historical context (Why it was created)
  - Problems solved or simplified
  - Modern usage and applications
  - Foundational impact on other theories
  - Current research and open questions
  - Solution methods (Analytical and Numerical)
- **Markdown Output**: Generates well-formatted Markdown files for easy reading and documentation.

## Installation

Ensure you have the `lite` library and its dependencies installed.

```bash
# From the project root
pip install -e .
```

## Usage

### Fetch explanation for a specific theory (Undergrad default)

```bash
python math_theory_cli.py --theory "Group theory"
```

### Fetch explanations for a general audience (No math background)

```bash
python math_theory_cli.py --theory "Knot theory" --level general
```

### Fetch explanations for a specific audience level

```bash
python math_theory_cli.py --theory "Chaos theory" --level phd
```

## Code Structure

- `math_theory_cli.py`: Main CLI entry point. Handles arguments and output generation.
- `math_theory_element.py`: Core logic for fetching and processing mathematical theory explanations.
- `math_theory_models.py`: Pydantic data models for structured LLM interaction.
- `assets/theories.txt`: Text file with a list of supported mathematical theories.
- `tests/`: Directory containing test scripts for project validation.

## Supported Theories

A pre-defined list of mathematical theories is maintained in `assets/theories.txt`.
