# Medical Implant Information Generator

A command-line utility that generates comprehensive medical implant information using large language models (LLMs). This tool leverages the LiteClient framework to produce detailed, structured information about various medical implants.

## Overview

The Medical Implant Generator provides an automated way to retrieve detailed information about medical implants, including specifications, applications, clinical considerations, and related data. Results are structured and validated through Pydantic models, ensuring data consistency and quality.

## Features

- **LLM-Powered Generation**: Uses configurable language models to generate comprehensive implant information
- **Structured Output**: Returns validated Pydantic models for reliable, typed data
- **JSON Export**: Saves results to JSON files for integration with other systems
- **Rich Console Display**: Presents results in formatted, easy-to-read panels
- **Flexible Configuration**: Supports custom model selection and temperature settings
- **Comprehensive Logging**: Multi-level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL) for debugging and monitoring
- **Error Handling**: Robust error handling with detailed error messages and logging

## Installation

1. Ensure you have Python 3.8+ installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your LLM model (default: `ollama/gemma3`)

## Usage

### Basic Command

Generate information for a medical implant:

```bash
python medical_implant_cli.py -i "cardiac pacemaker"
```

### Command-Line Arguments

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `--implant` | `-i` | string | **Required** | Name of the medical implant |
| `--output` | `-o` | string | None | Custom output file path |
| `--output-dir` | `-d` | string | `outputs` | Directory for output files |
| `--model` | `-m` | string | `ollama/gemma3` | LLM model to use for generation |
| `--verbosity` | `-v` | int | 2 | Logging level (0-4) |

### Verbosity Levels

- `0`: CRITICAL - Only critical errors
- `1`: ERROR - Errors and critical messages
- `2`: WARNING - Warnings, errors, and critical messages (default)
- `3`: INFO - Informational messages and above
- `4`: DEBUG - All messages including debug details

### Examples

Generate information with default settings:
```bash
python medical_implant_cli.py -i "hip prosthesis"
```

Generate with custom output file:
```bash
python medical_implant_cli.py -i "cochlear implant" -o my_implant.json
```

Generate with specific model and custom directory:
```bash
python medical_implant_cli.py -i "cardiac pacemaker" -m "openai/gpt-4" -d custom_outputs
```

Generate with detailed debug logging:
```bash
python medical_implant_cli.py -i "stent" -v 4
```

## Output Format

The generator produces structured implant information in the `ImplantInfo` format, exported as JSON:

```json
{
  "implant_name": "Cardiac Pacemaker",
  "description": "...",
  "applications": ["..."],
  "specifications": {...},
  "clinical_considerations": ["..."],
  ...
}
```

Output files are saved in the specified directory (default: `outputs`) with the naming convention:
```
{implant_name_lowercase}.json
```

Example: `cardiac_pacemaker.json`

## Logging

Logs are written to `medical_implant.log` in the working directory. The logging configuration includes:

- **Console Output**: Real-time logging to console based on verbosity level
- **File Output**: All messages written to `medical_implant.log`
- **Structured Logging**: Organized, readable log format with timestamps

### Log File Location
```
medical_implant.log
```

## Configuration

### Model Configuration

The tool uses `ModelConfig` for configuring the LLM:

```python
model_config = ModelConfig(
    model="ollama/gemma3",      # Model identifier
    temperature=0.7              # Creativity/randomness (0.0-1.0)
)
```

Modify the `temperature` parameter in `app_cli()` to adjust response diversity:
- **Lower values (0.0-0.3)**: More focused, deterministic responses
- **Higher values (0.7-1.0)**: More creative, varied responses

## Architecture

### Key Components

**MedicalImplantGenerator**
- Main class responsible for generating implant information
- Manages LiteClient communication
- Handles JSON serialization and file I/O

**Methods**
- `generate_text(implant: str) -> ImplantInfo`: Core generation method
- `ask_llm(model_input: ModelInput) -> ImplantInfo`: LLM query interface
- `save(implant_info: ImplantInfo, output_path: Path) -> Path`: Persistent storage

**Helper Functions**
- `print_result(result: ImplantInfo)`: Formats and displays results
- `get_user_arguments() -> argparse.Namespace`: CLI argument parsing
- `app_cli() -> int`: Main CLI entry point

## Error Handling

The tool provides comprehensive error handling:

- **Invalid Implant Name**: Validates non-empty implant input
- **File I/O Errors**: Catches and logs file operation failures
- **LLM Errors**: Propagates and logs generation failures
- **Configuration Errors**: Validates model configuration

All errors are logged with full exception details for debugging.

## Requirements

- Python 3.8+
- LiteClient framework
- Rich library (for formatted console output)
- Pydantic (for data validation)

## Related Files

- `medical_implant_models.py`: Pydantic models for data validation
- `lite_client.py`: LLM client interface
- `config.py`: Configuration models (ModelConfig, ModelInput)
- `logging_config.py`: Logging setup utilities

## Troubleshooting

### Model Not Found
Ensure the specified model is available in your LLM environment. Verify model configuration with:
```bash
python medical_implant_cli.py -i "test" -m "your/model" -v 4
```

### File Permission Errors
Check directory permissions for the output directory:
```bash
chmod 755 outputs
```

### Empty or Invalid Results
Review logs with increased verbosity to identify LLM issues:
```bash
python medical_implant_cli.py -i "implant" -v 4
```

## License

[Specify license if applicable]

## Support

For issues, questions, or contributions, please refer to the project's issue tracker or documentation.
