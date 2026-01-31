# Medical FAQ Generator

A CLI tool for generating patient-friendly medical FAQs using AI models. This tool leverages the `LiteClient` to produce structured or plain-text FAQ content for various medical topics.

## Features

- **FAQ Generation:** Creates detailed FAQs including patient-friendly answers, common misconceptions, and guidance on when to seek care.
- **Structured Output:** Option to generate output as structured JSON data (using Pydantic models) or plain text.
- **Customizable Models:** Support for different LLM backends (default: `ollama/gemma3`).
- **Flexible Logging:** Adjustable verbosity levels for debugging and monitoring.

## Installation

Ensure you have Python 3.x installed. This tool is part of the `MedKit` suite and relies on the `lite` library found in the parent directory.

1. Navigate to the tool directory:
   ```bash
   cd path/to/MedKit/medical/med_faqs
   ```

2. Ensure dependencies are installed (typically part of the main project setup).

## Usage

Run the CLI tool using `python medical_faq_cli.py`.

### Basic Example

Generate FAQs for a specific topic:

```bash
python medical_faq_cli.py -i "diabetes"
```

### Advanced Usage

Generate structured JSON output, specify a model, and set a custom output directory:

```bash
python medical_faq_cli.py -i "heart disease" --structured --output-dir ./my_faqs --model ollama/llama3
```

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--topic` | `-i` | **Required.** The medical topic to generate FAQs for. | N/A |
| `--output-dir` | `-d` | Directory to save the output files. | `outputs` |
| `--model` | `-m` | The AI model to use for generation. | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0=CRITICAL to 4=DEBUG). | `2` (WARNING) |
| `--structured` | `-s` | Enable structured JSON output using Pydantic models. | `False` |

## Project Structure

- `medical_faq_cli.py`: Entry point for the command-line interface.
- `medical_faq.py`: Core generator logic integrating with `LiteClient`.
- `medical_faq_models.py`: Pydantic data models for structured FAQ responses.
- `medical_faq_prompts.py`: System and user prompt definitions.

## Output

Generated files are saved to the specified output directory (default: `outputs`). Filenames are automatically generated based on the topic name (e.g., `diabetes_faq.json` or `diabetes_faq.txt`).