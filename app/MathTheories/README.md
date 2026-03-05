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
python math_theory_cli.py --theory "Knot theory" --levels general
```

### Fetch explanations for multiple audience levels

```bash
python math_theory_cli.py --theory "Chaos theory" --levels general high-school phd
```

## Code Structure

- `math_theory_cli.py`: Main CLI entry point. Handles arguments and output generation.
- `math_theory_element.py`: Core logic for fetching and processing mathematical theory explanations.
- `math_theory_models.py`: Pydantic data models for structured LLM interaction.
- `assets/theories.txt`: Text file with a list of supported mathematical theories.
- `tests/`: Directory containing test scripts for project validation.

## Output Structure

The tool saves each explanation as a Markdown file in `outputs/theories/<Theory_Name>.md`. If multiple audience levels are requested, they are appended in the same file, separated by a horizontal rule (`---`).

The structure follows this template:

# Theory Name

## Audience Level: [e.g., General, Undergrad, etc.]

### Introduction
A high-level overview of the theory tailored to the specific audience.

### Key Concepts
- **Concept 1**: Brief description.
- **Concept 2**: Brief description.
...

### Why It Was Created
Historical context and the core motivation behind the theory's development.

### Problems Solved or Simplified
What was difficult before this theory, and how it made things easier.

### How It Is Used Today
Modern applications in science, technology, and industry.

### Foundation for Other Theories
How this theory serves as a building block for more advanced mathematical or scientific fields.

### New Research
Current open questions, recent breakthroughs, and active areas of study.

### Solution Methods
- **Analytical**: Mathematical proofs and exact calculation methods.
- **Numerical**: Computational approaches, simulations, and algorithms.

---

*(Additional audience levels repeat the structure above)*

## Supported Theories

A pre-defined list of mathematical theories is maintained in `assets/theories.txt`.
