# Medical Anatomy Information Generator

A command-line tool for generating anatomical reports. This tool serves clinical reference, educational, and research purposes.

## Features

- **Reports**: Generates information on gross anatomy, microscopic structure, clinical significance, and imaging.
- **Structured Data**: Outputs data in JSON format for programmatic use.
- **Configuration**: Options for AI model selection, output directory, and logging.
- **Standardized Terminology**: Uses system prompts to ensure medical accuracy.

## Components

The report includes the following sections:

- **Overview**: Basic identification, classification, and body system.
- **Anatomical Position**: Location, orientation, and relationships to nearby structures.
- **Gross Morphology**: Shape, dimensions, and external appearance.
- **Microscopic Structure**: Tissue types, cellular components, and histology.
- **Function**: Physiological roles and mechanisms of action.
- **Vascular & Innervation**: Arterial supply, venous drainage, lymphatics, and nerve supply.
- **Clinical Significance**: Medical relevance, pathologies, and injury vulnerability.
- **Imaging Characteristics**: Appearance on X-ray, CT, MRI, and Ultrasound.
- **Developmental Anatomy**: Embryological origin, fetal development, and postnatal growth.
- **Variations & Anomalies**: Normal anatomical variations and congenital anomalies.
- **Landmarks & Approaches**: Surface landmarks and surgical access points.

## Prerequisites

- Python 3.x
- `pydantic`
- `lite` library (internal dependency)

## Usage

Run the tool using `python medical_anatomy_cli.py`.

### Basic Example

Generate a report for the "heart":

```bash
python medical_anatomy_cli.py -i "heart"
```

### Advanced Usage

Generate a structured report for the "femur", save to a specific directory, and set verbosity to INFO:

```bash
python medical_anatomy_cli.py -i "femur" -d outputs/femur -v 3 --structured
```

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--body_part` | `-i` | **Required.** Name of the anatomical structure. | N/A |
| `--output-dir` | `-d` | Directory for output files. | `outputs` |
| `--model` | `-m` | AI model to use. | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG). | `2` |
| `--structured` | `-s` | Enable structured Pydantic output. | `False` |

## Project Structure

- `medical_anatomy_cli.py`: CLI entry point.
- `medical_anatomy.py`: Core logic and API interaction.
- `medical_anatomy_models.py`: Data definitions for structured output.
- `medical_anatomy_prompts.py`: System and user prompt templates.
- `assets/`: Reference materials.
- `logs/`: Application logs.

## Output

Reports are saved to the output directory (default: `outputs`). Filenames use the sanitized body part name (e.g., `heart.txt` or `heart.json`).

---
*Note: This tool uses AI for content generation. Verify information with standard anatomical texts.*
