# Surgical Tray Preparation Generator

A command-line tool that generates comprehensive surgical tray lists and preparation instructions using structured language model prompting.

## Overview

The Surgical Tray Preparation Generator retrieves and formats detailed information about the instruments required for specific surgical procedures. It provides quantities, categories, and justifications for each instrument, along with tray-wide sterilization methods and setup instructions for clinical staff.

## Important Medical Disclaimers

**This tool is for informational and educational purposes only.** It is not a substitute for professional medical training, manufacturer guidelines, or clinical expertise. Users should:

- Consult experienced surgeons and clinical staff before preparing any surgical tray
- Verify instrument requirements with institutional preference cards and protocols
- Be aware that LLM-generated content may contain inaccuracies or incomplete information
- Understand that actual tray configurations vary by institution and surgeon preference
- Always follow institutional protocols and regulatory requirements for surgical instrument handling

## Installation

### Requirements

- Python 3.8+
- LiteClient and related dependencies from the parent project
- Rich library for formatted console output

### Setup

```bash
cd surgical_tray
pip install -r requirements.txt
```

## Usage

### Basic Command

Generate a tray list for a specific surgery:

```bash
python surgical_tray_info_cli.py -S "Appendectomy"
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--surgery` | `-S` | **Required.** Name of the surgery | — |
| `--output-dir` | `-d` | Directory for output files | `outputs` |
| `--model` | `-m` | Language model to use | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0-4) | `2` |
| `--structured`| `-s` | Use structured output (JSON) | `False` |

### Examples

Generate structured JSON output:
```bash
python surgical_tray_info_cli.py -S "Total Hip Arthroplasty" -s
```

Use a different model:
```bash
python surgical_tray_info_cli.py -S "Cataract Surgery" -m "ollama/llama2"
```

## Features

- **Tray Documentation**: Generates detailed lists of instruments, quantities, and their specific purpose for a given procedure.
- **Structured Output**: Results can be returned as `SurgicalTrayModel` objects for programmatic use.
- **JSON/Markdown Export**: Save results to files for reference or training.
- **System Prompting**: Uses expert surgical technologist personas to guide accurate information generation.

## Code Architecture

### Core Components

**`SurgicalInfoGenerator`** - Main class for tray generation
- Initializes with language model configuration
- Generates comprehensive surgical tray information
- Handles file output and logging

**Prompt Functions**
- `create_tray_system_prompt()`: Defines the LLM's role as a surgical technologist/OR nurse.
- `create_tray_user_prompt(surgery)`: Creates structured queries for specific surgeries.

**CLI Entry Point**
- `app_cli()`: Handles argument parsing and orchestrates the generation workflow.

## Output Format

When using structured output (`-s`), the tool generates a `SurgicalTrayModel` object:

```json
{
  "surgery_name": "...",
  "specialty": "...",
  "instruments": [
    {
      "name": "...",
      "quantity": 1,
      "category": "...",
      "reason": "..."
    }
  ],
  "sterilization_method": "...",
  "setup_instructions": "..."
}
```

## Logging

Logs are written to `logs/surgical_tool_info.log`.

## Limitations

1. **Model Dependency**: Output quality depends on the underlying language model.
2. **Preference Variation**: Different surgeons and hospitals may use different tray configurations for the same procedure.
3. **No Clinical Validation**: Generated information is not reviewed by clinical experts.