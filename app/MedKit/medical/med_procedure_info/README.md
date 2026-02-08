# Medical Procedure Information Generator

This tool is a command-line interface (CLI) application designed to generate evidence-based documentation for medical procedures using Large Language Models (LLMs). It produces detailed reports covering various aspects of a medical procedure, from preparation to recovery and long-term outcomes.


Difference betwen Medical Procedure and Surgery

A procedure is any defined, structured medical intervention performed to diagnose, treat, or manage a condition.

Key characteristics:

- Can be diagnostic (e.g., biopsy, endoscopy, angiography)
- Can be therapeutic (e.g., wound suturing, catheter insertion)
- May be non-invasive, minimally invasive, or invasive
- Does not necessarily involve cutting the body

Examples:
- Blood transfusion
- Colonoscopy
- Lumbar puncture
- Cardiac catheterization
- Dental filling

So:
**All surgeries are procedures, but not all procedures are surgeries. 




## Features

- **Procedure Reports:** Generates detailed information including:
    - Procedure Purpose & Indications
    - Preparation Requirements (fasting, medications, etc.)
    - Step-by-Step Procedure Details
    - Risks, Discomfort, and Complications
    - Recovery Timeline & Guidelines
    - Outcomes & Effectiveness
    - Follow-up Care
    - Alternatives
    - Cost & Insurance Information
- **Structured Output:** Option to generate output as a structured JSON object (validated by Pydantic) or standard Markdown text.
- **Model Flexibility:** Configurable LLM selection (defaults to `ollama/gemma3`).
- **File Output:** Automatically saves generated reports to a specified output directory.

## Prerequisites

- **Python 3.x**
- **LiteLLM / Lite Client:** This tool relies on a local `lite` package for LLM interaction. Ensure the `lite` module is available in your python path.
- **Pydantic:** Used for data validation and structure definition.

## Installation

Ensure you are in the project root or have the necessary dependencies installed.

```bash
pip install pydantic
# Ensure 'lite' package is accessible
```

## Usage

Run the tool from the command line using `medical_procedure_info_cli.py`.

### Basic Usage

Generate a report for a specific procedure:

```bash
python medical_procedure_info_cli.py -i "appendectomy"
```

### Advanced Usage

Specify an output directory, use a different model, and request structured output:

```bash
python medical_procedure_info_cli.py \
  -i "cardiac catheterization" \
  -d "./my_reports" \
  -m "ollama/gemma3" \
  -s
```

### Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--procedure` | `-i` | **Required.** Name of the medical procedure to research. | N/A |
| `--output-dir` | `-d` | Directory where the report will be saved. | `outputs` |
| `--model` | `-m` | The LLM model to use for generation. | `ollama/gemma3` |
| `--structured` | `-s` | If set, enforces a strict Pydantic schema for the output (JSON). | `False` |
| `--verbosity` | `-v` | Logging level (0=CRITICAL, ..., 4=DEBUG). | `2` (WARNING) |

## File Structure

- **`medical_procedure_info_cli.py`**: Entry point for the CLI. Handles argument parsing and logging setup.
- **`medical_procedure_info.py`**: Core logic. Orchestrates the generation process using `LiteClient`.
- **`medical_procedure_info_models.py`**: Pydantic data models defining the schema for structured procedure reports.
- **`medical_procedure_info_prompts.py`**: Helper class for constructing system and user prompts.
- **`assets/`**: Directory containing sample data.
