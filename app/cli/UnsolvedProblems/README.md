# Unsolved Problems Explorer

A professional command-line interface (CLI) and library for discovering and documenting famous unsolved problems across various academic disciplines. This tool leverages Large Language Models (LLMs) to provide structured, detailed information about open challenges in fields like Mathematics, Physics, Computer Science, and more.

## Overview

The Unsolved Problems Explorer uses the `lite` LLM client to query sophisticated models for a specified number of unsolved problems within a given topic. It returns structured data including the problem's significance, historical context, prize money, and current research status.

## Key Features

- **Topic-Based Exploration**: Fetch unsolved problems for any academic or scientific topic.
- **Structured Data**: Outputs detailed information using Pydantic models for consistency and type safety.
- **LLM Integration**: Flexible model selection (defaults to `ollama/gemma3` or via `DEFAULT_LLM_MODEL` environment variable).
- **Automated Output Management**: Results are automatically saved as JSON files in a dedicated `outputs/` directory.
- **Unicode Support**: Full support for mathematical symbols and non-ASCII characters (e.g., Kähler, Poincaré).
- **Robust Validation**: Input validation for topics and problem counts to ensure high-quality results.

## Project Structure

- `unsolved_problems_cli.py`: The main entry point for the command-line interface.
- `unsolved_problems_explorer.py`: Core logic for interacting with LLM providers and managing requests.
- `unsolved_problems_models.py`: Data schemas (Pydantic) for `UnsolvedProblem` and `UnsolvedProblemsResponse`.
- `unsolved_problems_prompts.py`: Template logic for constructing high-quality LLM prompts.
- `outputs/`: Directory where generated JSON reports are stored.
- `logs/`: Application logs for debugging and auditing.

## Installation

Ensure you have Python 3.10+ installed.

1. Clone the repository.
2. Ensure the `lite` library is installed or available in your Python path.
3. Install the required dependencies:
   ```bash
   pip install pydantic
   ```
4. Set your preferred model (optional):
   ```bash
   export DEFAULT_LLM_MODEL="ollama/gemma3"
   ```

## Usage

### Command Line Interface

Run the CLI using `python unsolved_problems_cli.py` with the following arguments:

```bash
python unsolved_problems_cli.py -t <TOPIC> -n <NUMBER_OF_PROBLEMS> [-m <MODEL>]
```

#### Examples:

- **Mathematics**: Fetch 10 unsolved problems in Mathematics:
  ```bash
  python unsolved_problems_cli.py -t "Mathematics" -n 10
  ```

- **Physics**: Fetch 5 unsolved problems using a specific model:
  ```bash
  python unsolved_problems_cli.py -t "Quantum Mechanics" -n 5 -m "claude-3-opus"
  ```

### Output

Generated files are stored in the `outputs/` directory with a naming convention: `unsolved_<topic>_<count>.json`.

Example JSON structure:
```json
{
    "topic": "Algebraic Topology",
    "num_problems": 1,
    "problems_retrieved": 1,
    "problems": [
        {
            "title": "The Hodge Decomposition Conjecture",
            "description": "...",
            "field": "Algebraic Topology, Complex Geometry",
            "difficulty": "Advanced",
            "first_posed": "...",
            "prize_money": "None",
            "significance": "...",
            "current_status": "..."
        }
    ]
}
```

## Configuration

- **Environment Variables**:
    - `DEFAULT_LLM_MODEL`: Defines the default LLM model to use if not specified via CLI.
- **Logging**: 
    - The application uses `lite.logging_config` to manage logging.
    - Detailed execution logs are automatically stored in `logs/unsolved.log`.
    - Console output is suppressed by default to maintain a clean CLI experience.

## License

[Specify License Here, e.g., MIT]
