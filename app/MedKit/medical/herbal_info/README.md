# Herbal Information Generator

A command-line tool for generating structured, evidence-based reports on medicinal herbs. This system utilizes large language models to aggregate botanical data, therapeutic mechanisms, safety profiles, and clinical evidence.

## Overview

The Herbal Information Generator provides a standardized framework for documenting herbal remedies. It is designed for practitioners, researchers, and educators who require objective data on medicinal plants. The system supports both unstructured narrative reports and strictly validated JSON output using Pydantic models.

## Core Features

- **Comprehensive Data Collection**: Covers botanical nomenclature, active phytochemicals, and traditional medicine systems.
- **Safety Analysis**: Detailed sections for contraindications, drug interactions, and special population considerations (pregnancy, pediatric, etc.).
- **Dosing & Administration**: Age-specific dosage guidelines and preparation methods (teas, tinctures, extracts).
- **Evidence-Based Reporting**: Summarizes clinical evidence, regulatory status, and current research.
- **Structured Output**: Support for JSON schema validation for integration into larger medical databases.

## Project Structure

- `herbal_info.py`: Core logic and `HerbalInfoGenerator` class.
- `herbal_info_cli.py`: Command-line interface for report generation.
- `herbal_info_models.py`: Data schemas and Pydantic validation models.
- `herbal_info_prompts.py`: Standardized prompt templates for medical accuracy.
- `assets/herb_list.txt`: Reference list of supported or common herbs.

## Installation

Ensure you have Python 3.8+ and the required dependencies installed. This tool depends on a local or remote `LiteClient` configuration for LLM access.

```bash
pip install pydantic
```

## Usage

### Basic Report Generation
To generate a standard Markdown report for a specific herb:
```bash
python herbal_info_cli.py -i "Ginger"
```

### Structured Data Export
To generate a validated JSON report:
```bash
python herbal_info_cli.py -i "Turmeric" --structured
```

### Options
- `-i`, `--herb`: (Required) Name of the herb.
- `-d`, `--output-dir`: Directory for saved reports (default: `outputs`).
- `-m`, `--model`: LLM model identifier (default: `ollama/gemma3`).
- `-s`, `--structured`: Enable Pydantic-validated JSON output.
- `-v`, `--verbosity`: Logging level (0-4).

## Data Schema

Reports are organized into the following logical modules:
1.  **Metadata**: Nomenclature and plant family.
2.  **Classification**: Traditional systems and energetics.
3.  **Mechanism**: Biochemical action and targeted body systems.
4.  **Usage**: Preparation, storage, and dosage.
5.  **Safety**: Side effects, interactions, and toxicity.
6.  **Special Populations**: Pregnancy, breastfeeding, and pediatric use.
7.  **Evidence**: Clinical studies and regulatory status.

## Disclaimer

This tool is intended for informational and educational purposes only. The generated reports should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider or certified herbalist before beginning any new herbal regimen.