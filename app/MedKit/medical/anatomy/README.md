# Medical Anatomy Information Generator

A powerful CLI tool that generates comprehensive, evidence-based anatomical information reports using AI models. This tool is designed for clinical reference, educational purposes, and anatomical research.

## Features

- **Comprehensive Reports**: Generates detailed information including gross anatomy, microscopic structure, clinical significance, imaging characteristics, and more.
- **Structured Data**: Option to output data in a structured JSON format (Pydantic models) for programmatic use.
- **Customizable**: Configure the AI model, output directory, and logging verbosity.
- **Evidence-Based Prompts**: Uses expert-level system prompts to ensure accurate and clinically relevant terminology.

## Components

The report covers the following anatomical aspects:
- **Overview**: Classification, body system, and embryological origin.
- **Position**: Location, landmarks, and anatomical relationships.
- **Morphology**: Shape, dimensions, and surface features.
- **Microscopic Structure**: Histology and cellular components.
- **Function**: Primary/secondary functions and mechanisms.
- **Vascular & Innervation**: Blood supply, lymphatics, and nerve supply.
- **Clinical Significance**: Pathologies, surgical considerations, and injury vulnerability.
- **Imaging**: Appearance on X-ray, CT, MRI, and Ultrasound.
- **Development**: Embryology and growth patterns.

## Prerequisites

- Python 3.x
- `pydantic`
- `lite` library (internal dependency)

## Usage

Run the CLI tool using `python medical_anatomy_cli.py`.

### Basic Example

Generate a report for the "heart":

```bash
python medical_anatomy_cli.py -i "heart"
```

### Advanced Usage

Generate a structured report for the "femur", save it to a specific folder, and set verbosity to INFO:

```bash
python medical_anatomy_cli.py -i "femur" -d outputs/femur -v 3 --structured
```

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--body_part` | `-i` | **Required.** The name of the anatomical structure. | N/A |
| `--output-dir` | `-d` | Directory for output files. | `outputs` |
| `--model` | `-m` | AI model to use. | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG). | `2` |
| `--structured` | `-s` | Enable structured Pydantic output. | `False` |

## Project Structure

- `medical_anatomy_cli.py`: CLI entry point and argument parsing.
- `medical_anatomy.py`: Core generator logic and API interaction.
- `medical_anatomy_models.py`: Pydantic data definitions for structured output.
- `medical_anatomy_prompts.py`: System and user prompt templates.
- `assets/`: Reference materials (PDFs and text).
- `logs/`: Application logs.

## Output

Generated reports are saved to the specified output directory (default: `outputs`). The filenames are sanitized versions of the body part name (e.g., `heart.txt` or `heart.json` depending on the output format).

---
*Note: This tool uses LLMs for content generation. While designed for accuracy, always verify critical medical information with standard anatomical texts.*
