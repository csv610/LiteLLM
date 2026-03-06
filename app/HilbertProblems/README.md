# Hilbert's 23 Problems Reference Guide

A dynamic, AI-powered reference tool designed to fetch, document, and explore the 23 mathematical problems proposed by David Hilbert in 1900. 

## What This Project Does

This tool provides a structured, command-line interface for exploring Hilbert's 23 problems. It leverages Large Language Models (LLMs) via the `LiteClient` (specifically optimized for `ollama/gemma3`) to retrieve comprehensive details, historical context, and current status for each problem. 

Key functionality includes:
- **On-Demand Retrieval**: Fetches detailed information for any of Hilbert's 23 problems using advanced AI.
- **Structured Documentation**: Organizes complex mathematical data into a consistent format (status, solver, year, solution method, etc.).
- **Summary Views**: Provides a high-level overview of all problems for quick reference.
- **Model Flexibility**: Supports multiple LLM backends to compare different perspectives on these mathematical challenges.

## Why It Matters

Hilbert's problems are more than just a list of questions; they served as a roadmap for 20th-century mathematics. Many of these problems have been solved, leading to significant breakthroughs, while others remain open challenges that continue to inspire researchers.

This project matters because it:
- **Bridges the Gap**: Makes dense mathematical history accessible through a modern, interactive interface.
- **Demonstrates AI Utility**: Shows how structured LLM outputs can be used to build reliable educational and research tools.
- **Centralizes Knowledge**: Instead of searching through fragmented resources, it provides a single, consistent source for exploring these foundational problems.

## Structured Output: The Core Engine

A defining feature of this project is its use of **Structured AI Output**. Unlike typical chatbots that return free-form text, this tool enforces a strict data schema for every response.

### How it Works:
1. **Pydantic Models**: We define the "shape" of a Hilbert Problem using Pydantic (see `hilbert_problems_models.py`). This includes specific types for problem numbers, titles, and even an enumeration for status (`SOLVED`, `UNSOLVED`, `PARTIALLY_SOLVED`).
2. **Schema Enforcement**: The `LiteClient` transmits this schema to the LLM (optimized for `ollama/gemma3`), instructing it to return data that fits the model exactly.
3. **Validation**: Before the data ever reaches the CLI, it is validated against the model. If the AI returns malformed data or missing fields, the system catches it, ensuring the application remains stable and the information remains reliable.

### Benefits:
- **Consistency**: Every problem, regardless of which model generated it, follows the exact same format.
- **Programmatic Use**: Because the output is structured (JSON-compatible), the data can be easily saved, searched, or integrated into other systems without complex parsing.
- **Reliability**: It eliminates "AI hallucinations" where the model might otherwise omit critical details like the solution year or the mathematician involved.

## Target Audience

- **Mathematics Students & Educators**: A structured way to learn about the history and status of some of the most famous problems in math.
- **Researchers & Enthusiasts**: A quick reference tool for checking the status and solution details of specific problems.
- **AI Developers**: An example of how to use structured LLM outputs (Pydantic models) to build robust applications.

---

## Features

- **Dynamic Retrieval**: Fetches detailed information, status, and historical context.
- **Persistent Logging**: Comprehensive logging for tracking operations and debugging.
- **Command-Line Interface**: Intuitive CLI to browse summaries or dive into specific details.
- **Structured Data**: Uses robust data models (Pydantic) to ensure consistency.

## Project Structure

- `hilbert_problems_cli.py`: The main entry point for the command-line interface.
- `hilbert_problems.py`: Core logic for fetching, parsing, and managing the problem guide.
- `hilbert_problems_models.py`: Data models defining the structure of a Hilbert Problem.
- `hilbert_problems_prompts.py`: Logic for building LLM prompts.
- `logs/`: Directory containing application and CLI logs.

## Prerequisites

- Python 3.x
- Access to an LLM provider (e.g., Ollama running `gemma3`)
- `lite` package (internal dependency for LLM communication)
- `tqdm` for progress tracking

## Installation

```bash
pip install tqdm
# Ensure the 'lite' package is available in your Python path
```

## Usage

The guide can be accessed via the CLI script:

### Display All Problems Summary
```bash
python hilbert_problems_cli.py
```

### Display Details for a Specific Problem (e.g., Problem 1)
```bash
python hilbert_problems_cli.py -p 1
```

### Specify a Custom Model
```bash
python hilbert_problems_cli.py -m ollama/mistral
```

## License

[Specify License, e.g., MIT]
