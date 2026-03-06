# Hilbert's 23 Problems Reference Guide

A command-line tool that uses Large Language Models (LLMs) to generate a structured, verifiable reference for the 23 mathematical problems proposed by David Hilbert in 1900.

## Overview

This project provides an automated way to explore the status and history of Hilbert's foundational problems. Instead of manual research, it extracts precise mathematical details and historical context into a structured format, allowing users to quickly understand the trajectory of 20th-century mathematics.

## Information Provided

For each of the 23 problems, the tool retrieves and organizes the following data points:

- **Mathematical Formulation**: A precise and rigorous description of the problem's logic and objectives.
- **Current Resolution Status**: Clear identification of whether the problem is **Solved**, **Unsolved**, or **Partially Solved**.
- **Historical Attribution**: The names of the mathematicians who provided the solution or made significant breakthroughs.
- **Chronology**: The specific year the problem was solved or reached a major milestone.
- **Technical Methodology**: A detailed breakdown of the mathematical techniques and approaches used to address the problem.
- **Cross-Disciplinary Links**: Connections to other branches of mathematics (e.g., Set Theory, Topology, Number Theory, Analysis).
- **Contextual Insights**: Critical notes on the problem's broader impact, historical significance, and ongoing influence on modern research.

## How it Works (Structured Extraction)

The application uses **Structured AI Output** to ensure that every response is complete and accurate. 

1. **Expert Context**: It uses specialized prompts to treat the AI as a mathematical historian, ensuring high-quality, professional-grade information.
2. **Schema Enforcement**: It forces the LLM to provide data in a specific, pre-defined format. This prevents the model from omitting critical details like solution years or the names of solvers.
3. **Data Integrity**: Every piece of information is validated before being displayed, ensuring that you receive consistent and machine-readable data across all 23 problems.

## Why This Matters

- **Centralized Knowledge**: Consolidates fragmented historical and mathematical data into a single, accessible interface.
- **Educational Utility**: Provides a structured roadmap for students and researchers to study the history of mathematics.
- **Comparative Analysis**: Allows users to compare how different LLMs (e.g., `gemma3` vs `mistral`) interpret and summarize complex mathematical breakthroughs.

## Project Structure

- `hilbert_problems_cli.py`: Main CLI for querying and displaying problems.
- `hilbert_problems.py`: Logic for fetching and managing the problem guide.
- `hilbert_problems_models.py`: Defines the structured data schema.
- `hilbert_problems_prompts.py`: Expert-tuned mathematical prompts.

## Usage

### Summary of All Problems
```bash
python hilbert_problems_cli.py
```

### Detailed View (e.g., Riemann Hypothesis)
```bash
python hilbert_problems_cli.py -p 8
```

### Compare with Different Models
```bash
python hilbert_problems_cli.py -p 1 -m ollama/mistral
```

## License
[MIT]
