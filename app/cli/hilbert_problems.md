# Hilbert Problems Reference Guide

## Overview

A Python CLI tool that provides a comprehensive reference guide for Hilbert's 23 Problems. The application dynamically fetches and documents all 23 problems proposed by David Hilbert in 1900 using LiteClient (with support for various models like ollama/gemma3).

## Architecture

### Core Classes

#### `ProblemStatus` (Enum)
Status indicators for Hilbert problems:
- `SOLVED` - Problem has been fully solved
- `UNSOLVED` - Problem remains unsolved
- `PARTIALLY_SOLVED` - Problem has been partially solved

#### `HilbertProblem` (Pydantic Model)
Structured data model for individual problems:
- `number` (int): Problem number (1-23)
- `title` (str): Title of the problem
- `description` (str): Mathematical description
- `status` (ProblemStatus): Current status
- `solved_by` (Optional[str]): Mathematician(s) who solved it
- `solution_year` (Optional[int]): Year the problem was solved
- `solution_method` (str): Detailed explanation of the solution
- `related_fields` (List[str]): Related mathematical fields
- `notes` (str): Additional notes and implications

#### `HilbertProblemsGuide` (Main Class)
Central class managing problem data retrieval and caching:

**Key Methods:**
- `__init__(config)`: Initialize with optional ModelConfig
- `get_problem(problem_number)`: Fetch specific problem from cache or API
- `get_all_problems()`: Fetch all 23 problems with progress bar
- `display_problem(problem)`: Format and display single problem with emojis
- `display_summary()`: Display summary of all problems grouped by status
- `_load_from_file()`: Load cached problems from JSON
- `_save_to_file()`: Persist problems to JSON
- `_validate_problem_number(number)`: Validate problem number is 1-23

**Features:**
- Caches problems in JSON files (format: `hilbert_problems_{model_name}.json`)
- Uses LiteClient for API communication
- Supports custom model configuration
- Comprehensive error handling and logging

## CLI Interface

### Arguments

```
-p, --problem   Problem number (1-23) to display details
                If not specified, shows summary of all problems

-m, --model     Model to use for fetching information
                Default: ollama/gemma3
```

### Usage Examples

```bash
# Show summary of all problems
python hilbert_problems.py

# Show details of problem 1
python hilbert_problems.py -p 1

# Show problem 8 using specific model
python hilbert_problems.py -p 8 -m ollama/gemma3

# Show all problems with custom model
python hilbert_problems.py -m ollama/mistral
```

## Logging

- **Log File**: `hilbert_problems.log`
- **Console Output**: Simultaneous logging to console
- **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Levels**: INFO (default), WARNING, ERROR

## Data Flow

1. **Initialization**: Load cached problems from JSON file if it exists
2. **Fetch Request**: User requests a problem by number
3. **Cache Check**: Check if problem is already cached
4. **API Call**: If not cached, generate prompt and call LiteClient
5. **Validation**: Ensure problem number matches requested number
6. **Cache Update**: Store new problem in cache and save to file
7. **Display**: Format and display problem with emojis and sections

## Display Format

Problems are displayed with:
- Problem title and status emoji (✅/❓/⚠️)
- Mathematical description
- Status information (solver, year)
- Solution method explanation
- Related mathematical fields (bulleted list)
- Additional notes

Summary view displays:
- Overall statistics (solved/unsolved/partially solved counts)
- Grouped lists of problems by status

## Dependencies

- `pydantic`: Data validation using Python type annotations
- `tqdm`: Progress bar for fetching all problems
- `lite.lite_client.LiteClient`: API client for model communication
- `lite.config.ModelConfig, ModelInput`: Configuration models
- Standard library: `sys`, `argparse`, `logging`, `json`, `pathlib`, `typing`, `enum`

## Error Handling

- Validates problem numbers (1-23 range)
- Handles file I/O errors gracefully
- Catches and logs API communication errors
- Handles KeyboardInterrupt for graceful shutdown
- Logs all errors to file and console

## Configuration

Default configuration:
- Model: `ollama/gemma3`
- Temperature: `0.3` (for deterministic responses)

Custom configuration via command-line `-m/--model` flag.
