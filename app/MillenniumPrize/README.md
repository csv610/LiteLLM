# Millennium Prize Problems Explorer

A CLI tool for exploring and generating detailed information about the seven Millennium Prize Problems in mathematics.

The Millennium Prize Problems are seven problems in mathematics that were stated by the Clay Mathematics Institute in 2000. The problems are Birch and Swinnerton-Dyer conjecture, Hodge conjecture, Navier–Stokes existence and smoothness, P versus NP problem, Poincaré conjecture, Riemann hypothesis, and Yang–Mills existence and mass gap. A correct solution to any of the problems results in a US $1 million prize being awarded by the institute.

## Features

- **CLI Interface**: Easy-to-use command-line interface for querying problem data.
- **Detailed Data**: Includes title, description, field, status, significance, and current progress for each problem.
- **LLM-Powered Explanations**: Generate comprehensive explanations using Large Language Models (LLMs) via `LiteClient`.
- **JSON Export**: Automatically saves problem details and generated explanations to structured JSON files.
- **Type Safety**: Built with Pydantic models for robust data validation and schema management.
- **Comprehensive Logging**: Detailed logging of operations and error handling.

## Project Structure

- `millennium_prize_problems_cli.py`: Main entry point and CLI logic.
- `millennium_prize_models.py`: Pydantic data models for problems and responses.
- `millennium_prize_prompts.py`: Logic for building prompts for LLM explanations.
- `test_millennium_prize.py`: Comprehensive test suite using `unittest`.

## Installation

### Prerequisites

- Python 3.8+
- Pydantic
- Access to an LLM (optional, defaults to `ollama/gemma3`)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd MillenniumPrize
   ```

2. Install dependencies:
   ```bash
   pip install pydantic
   ```
   *(Note: Ensure the `lite` module and its dependencies are available in your python path as this tool depends on it for LLM functionality.)*

## Usage

### List All Problems
To list all Millennium Prize Problems and save them to `millennium_prize_problems.json`:
```bash
python millennium_prize_problems_cli.py
```

### Get Specific Problem Details
To get details for a specific problem (1-7) without LLM explanation:
```bash
python millennium_prize_problems_cli.py -p 1
```

### Generate LLM Explanation
To generate a detailed explanation using a specific LLM:
```bash
python millennium_prize_problems_cli.py -p 3 -m gpt-4
```

### CLI Arguments
- `-p, --problem`: Problem number (1-7). Omit to list all.
- `-m, --model`: LLM model to use (default: `ollama/gemma3`).

## Millennium Prize Problems List

1. **P versus NP** (Computer Science)
2. **Hodge Conjecture** (Algebraic Geometry)
3. **Riemann Hypothesis** (Number Theory)
4. **Yang-Mills Existence and Mass Gap** (Mathematical Physics)
5. **Navier-Stokes Existence and Smoothness** (Fluid Dynamics)
6. **Birch and Swinnerton-Dyer Conjecture** (Number Theory)
7. **Poincaré Conjecture** (Topology) - *Solved by Grigori Perelman (2003)*

## Testing

Run the test suite using `unittest`:
```bash
python test_millennium_prize.py
```

The tests cover model validation, prompt generation, and CLI functionality using mocks for external dependencies.
