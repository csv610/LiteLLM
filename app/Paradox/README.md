# Paradox Explainer

This tool generates high-rigor, academically-focused explanations for paradoxes tailored to different audience levels, from a general audience to specialized researchers.

## Features

- **Multi-Level Explanations**: Provides tailored content for:
  - **General**: Uses analogies, avoids jargon.
  - **High School**: Introduces basic logic and mathematical concepts.
  - **Undergrad**: Focuses on formal definitions (e.g., limits, convergence).
  - **Master**: Discusses philosophical implications (e.g., "At-At" theory).
  - **PhD**: Explores supertasks, non-standard analysis, and set theory.
  - **Researcher**: Connects to cutting-edge physics (e.g., Planck scale, Loop Quantum Gravity).
- **Academic Rigor Mandate**: Every explanation must include:
  - **Status**: Current scientific/philosophical standing (Solved, Unsolved, Debated).
  - **Root Cause**: The exact hidden assumptions or theoretical flaws causing the contradiction.
  - **Resolution Details**: 
    - **Who Solved It**: Primary figures (e.g., Aristotle, Newton, Russell).
    - **How It Was Solved**: The specific breakthrough or methodology.
    - **Logical & Mathematical Details**: Deep dives into the resolution's mechanics.
- **Comprehensive Coverage**: Includes historical context, key concepts, modern relevance, and current debates.
- **Markdown Output**: Generates well-formatted Markdown files automatically.

## Installation

Ensure you have the `lite` library and its dependencies installed.

```bash
# From the project root
pip install -e .
```

## Usage

### Fetch explanation for a specific paradox (Undergrad default)

```bash
python paradox_cli.py --paradox "Zeno's Dichotomy Paradox"
```

### Fetch explanations for a researcher level

```bash
python paradox_cli.py --paradox "Fermi paradox" --level researcher
```

## Testing

The project includes a comprehensive test suite using `pytest`, covering all 6 audience levels and ensuring structural integrity of the explanations.

```bash
# Run all tests
export PYTHONPATH=$PYTHONPATH:.
pytest tests/
```

## Code Structure

- `paradox_cli.py`: Main CLI entry point. Handles arguments and Markdown output.
- `paradox_element.py`: Core logic with a high-rigor academic prompt.
- `paradox_models.py`: Pydantic data models enforcing field requirements.
- `assets/paradox.txt`: JSON-formatted list of supported paradoxes by category.
- `tests/`: Test suite for data models, logic, and CLI.

## Supported Paradoxes

A curated list of paradoxes is maintained in `assets/paradox.txt`.
