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
- **JSON Output**: Saves results in structured JSON format.

## Installation

Ensure you have the `lite` library and its dependencies installed.

```bash
pip install -e .
```

## Usage

### Fetch explanation for a specific theory

```bash
python math_theory_cli.py --theory "Game theory"
```

### Fetch explanations for specific audience levels

```bash
python math_theory_cli.py --theory "Chaos theory" --levels high-school phd
```

## Data Structure
The generated Markdown files follow the structure:

# Theory Name
## Audience Level: Level Name
### Introduction
...
### Key Concepts
...

## Supported Theories

The list of theories is maintained in `assets/theories.txt`.
