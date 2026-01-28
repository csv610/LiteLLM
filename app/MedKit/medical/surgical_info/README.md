# MedKit Surgical Info CLI

## Overview

The **MedKit Surgical Info CLI** is a powerful command-line tool designed to generate comprehensive, evidence-based information about surgical procedures. Utilizing advanced Large Language Models (LLMs) via the `LiteLLM` framework, it produces detailed reports covering indications, risks, procedural steps, recovery timelines, and more.

This tool is part of the **MedKit** suite and is capable of generating both free-form text reports and highly structured JSON data adhering to strict medical schemas.

## Features

*   **Comprehensive Generation**: Generates detailed surgical reports including Anatomy, Indications, Contraindications, Pre-op/Post-op care, Risks, and Recovery.
*   **Dual Output Modes**:
    *   **Text Mode**: Natural language descriptions suitable for reading.
    *   **Structured Mode (`--structured`)**: Returns data strictly validated against Pydantic models, perfect for API integration or database storage.
*   **Customizable Models**: Supports various LLM backends (default: `ollama/gemma3`).
*   **Flexible Output**: Automatically saves results to a specified directory.
*   **Logging Control**: Adjustable verbosity for debugging or quiet operation.

## Prerequisites

*   Python 3.8+
*   Access to an LLM provider (e.g., Ollama running locally, or OpenAI/Anthropic API keys if configured).
*   Internal `lite` library (ensure the parent project structure is intact).

## Installation

Ensure you are in the project root directory and have the necessary dependencies installed.

```bash
# Install required packages (example)
pip install pydantic argparse
```

*Note: This tool relies on an internal `lite` package located four levels up in the directory structure. Ensure you run the script from a location where it can resolve this dependency.*

## Usage

Run the CLI using `python surgery_info_cli.py`.

### Basic Usage
Generate a standard text report for a surgery:

```bash
python surgery_info_cli.py --surgery "appendectomy"
```

### Structured Output
Generate a JSON-structured report validated against medical data models:

```bash
python surgery_info_cli.py --surgery "knee replacement" --structured
```

### Custom Output Directory
Save files to a specific folder:

```bash
python surgery_info_cli.py -i "coronary bypass" -d ./my_reports
```

### Select a Different Model
Use a specific model (must be supported by your configuration):

```bash
python surgery_info_cli.py -i "cataract surgery" -m "gpt-4-turbo"
```

### Debugging
Increase logging verbosity (0=CRITICAL to 4=DEBUG):

```bash
python surgery_info_cli.py -i "hernia repair" -v 4
```

## CLI Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--surgery` | `-i` | **Required.** Name of the surgical procedure. | N/A |
| `--output-dir` | `-d` | Directory for output files. | `outputs` |
| `--model` | `-m` | Model to use for generation. | `ollama/gemma3` |
| `--structured` | `-s` | Enable structured Pydantic output. | `False` |
| `--verbosity` | `-v` | Logging level (0-4). | `2` (WARNING) |

## Data Models

When using the `--structured` flag, the output adheres to the `SurgeryInfoModel` schema defined in `surgery_info_models.py`, containing:

*   **Metadata**: Names, codes (CPT/ICD), categories.
*   **Background**: Definition, anatomy, history, epidemiology.
*   **Indications**: Absolute/relative indications and contraindications.
*   **Preoperative**: Evaluation, labs, imaging, risk stratification.
*   **Operative**: Approaches, anesthesia, steps, duration.
*   **Risks**: Intra/Post-operative complications and rates.
*   **Postoperative**: Immediate care, pain mgmt, hospital stay.
*   **Recovery**: Timeline, rehab, return to work.
*   **Follow-up**: Schedules, warning signs.
*   **Alternatives**: Medical management, less invasive options.
*   **Technical**: Variations, qualifications, technology.
*   **Research**: Innovations, AI applications, trials.
*   **Cost**: Insurance coverage, cost ranges.

## Project Structure

```
surgery_info/
├── surgery_info_cli.py      # Main entry point
├── surgery_info_models.py   # Pydantic data schemas
├── surgery_info_prompts.py  # Prompt engineering logic
├── outputs/                 # Default output directory
│   └── ...
├── assets/                  # Reference materials (PDFs)
└── logs/                    # Application logs
```
