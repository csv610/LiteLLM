# Organ Disease Information Generator

A professional command-line interface (CLI) tool designed to generate comprehensive, evidence-based lists of diseases associated with specific human organs using Large Language Models (LLMs).

> **⚠️ Medical Disclaimer**
>
> This tool is for **informational and educational purposes only**. The content generated is produced by an AI model and **must not be used as a substitute for professional medical advice, diagnosis, or treatment**. Always seek the advice of a qualified healthcare provider with any questions regarding a medical condition.

## Overview

The **Organ Disease Information Generator** leverages the power of the `LiteClient` library to interface with advanced LLMs (defaulting to `ollama/gemma3`). It assists medical professionals, researchers, and students by rapidly compiling exhaustive lists of pathologies—ranging from common conditions to rare genetic disorders—linked to a specified organ.

## Features

- **Comprehensive Disease Mapping:** Generates exhaustive lists covering infectious, inflammatory, neoplastic, congenital, metabolic, vascular, traumatic, and autoimmune disorders.
- **Categorized Output:** Automatically classifies diseases into **"Common"** and **"Rare"** categories for better readability and prioritization.
- **Flexible Output Formats:**
  - **Markdown Report (Default):** A detailed, readable text report.
  - **Structured JSON (`-s`):** Machine-parsable output validated against strict Pydantic models (`OrganDiseasesModel`), ideal for data integration.
- **Customizable Backend:** Supports various LLM backends via the `LiteClient` configuration.
- **Robust Logging:** Configurable verbosity levels for debugging and monitoring.

## Installation

### Prerequisites

- **Python 3.8+**
- Access to the `lite` package (internal library)
- An LLM provider (e.g., Ollama, OpenAI) configured in your environment.

### Setup

1.  Ensure all dependencies are installed (including `pydantic` and `lite`).
2.  Verify your LLM configuration (e.g., `ollama` running locally or API keys set).

## Usage

The tool is executed via the command line using `organ_disease_info_cli.py`.

### Basic Command

Generate a comprehensive Markdown report for a specific organ:

```bash
python organ_disease_info_cli.py -i "Kidney"
```

*Output:* A file named `kidney_diseases.md` will be created in the `outputs/` directory.

### Advanced Usage

Generate a structured JSON dataset for the Liver, using a specific model, and save to a custom directory:

```bash
python organ_disease_info_cli.py -i "Liver" -s -d "./data/medical_reports" -m "ollama/llama3"
```

### CLI Arguments

| Argument | Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| **Organ Name** | `-i`, `--organ` | **Required.** The name of the organ to investigate. | N/A |
| **Structured Output** | `-s`, `--structured` | Output as structured JSON (validates against Pydantic schema). | `False` |
| **Output Directory** | `-d`, `--output-dir` | Directory to save the generated report. | `outputs` |
| **Model** | `-m`, `--model` | LLM model identifier to use. | `ollama/gemma3` |
| **Verbosity** | `-v`, `--verbosity` | Logging level (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG). | `2` |

## Output Structure

### Markdown Report (Default)
A formatted document listing diseases categorized by prevalence (Common vs. Rare), often including brief descriptions of etiology and pathophysiology.

### Structured JSON (`-s`)
A JSON file adhering to the `OrganDiseasesModel` schema:

```json
{
  "organ": "Heart",
  "common_diseases": [
    "Coronary Artery Disease",
    "Atrial Fibrillation",
    ...
  ],
  "rare_diseases": [
    "Hypertrophic Cardiomyopathy",
    "Arrhythmogenic Right Ventricular Cardiomyopathy",
    ...
  ]
}
```

## Project Structure

- `organ_disease_info_cli.py`: Main CLI entry point. Handles arguments and orchestration.
- `organ_disease_info.py`: Core generator logic (`DiseaseInfoGenerator` class).
- `organ_disease_info_models.py`: Pydantic data models for input/output validation.
- `organ_disease_info_prompts.py`: Prompt engineering logic for LLM interaction.