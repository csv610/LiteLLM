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

## Output Structure
The generated Markdown files (`outputs/theories/<Theory_Name>.md`) follow a structured format:

# Theory Name

## Audience Level: [Level]

### Introduction
...
### Key Concepts
- Concept 1
- Concept 2
...
### Why It Was Created
...
### Problems Solved or Simplified
...
### How It Is Used Today
...
### Foundation for Other Theories
...
### New Research
...
### Solution Methods
**Analytical:** ...
**Numerical:** ...

---

## Supported Theories

A pre-defined list of mathematical theories is maintained in `assets/theories.txt`.
