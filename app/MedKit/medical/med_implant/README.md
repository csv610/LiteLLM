# Medical Implant Information Generator

A powerful CLI tool that leverages Large Language Models (LLMs) to generate comprehensive, evidence-based reports on medical implants. This tool can produce both free-text descriptions and highly structured data suitable for clinical databases or educational resources.

## Features

*   **Comprehensive Generation:** Generates detailed information covering purpose, indications, materials, surgical procedure, recovery, complications, and more.
*   **Structured Data:** Optional support for Pydantic-based structured output (JSON) ensures consistent and machine-readable data formats.
*   **Customizable Models:** Supports various LLM backends (default: `ollama/gemma3`) via the `lite` client configuration.
*   **Extensive Schema:** Utilizes a rich data model covering over 15 categories of implant information, from "Metadata" to "Insurance & Cost".
*   **Flexible Output:** Save reports to a specified directory with automatic naming.

## Prerequisites

*   Python 3.8+
*   Access to the local `lite` library (shared utility for LLM interaction).
*   An operational LLM backend (e.g., Ollama) if using the default configuration.

## Installation

1.  Navigate to the project directory:
    ```bash
    cd medical/med_implant
    ```

2.  Ensure you have the necessary dependencies installed (including `pydantic` and the internal `lite` package).

## Usage

The primary entry point is `medical_implant_cli.py`.

### Basic Usage
Generate a report for a specific implant:

```bash
python medical_implant_cli.py -i "cardiac pacemaker"
```

### Structured Output
Generate a structured JSON report adhering to the strict data schema:

```bash
python medical_implant_cli.py -i "total hip replacement" --structured
```

### Custom Output Directory
Specify where to save the generated files:

```bash
python medical_implant_cli.py -i "cochlear implant" -d ./my_reports
```

### Select a Different Model
Use a specific LLM model for generation:

```bash
python medical_implant_cli.py -i "dental implant" -m "ollama/llama3"
```

### Verbose Logging
Increase verbosity for debugging:

```bash
python medical_implant_cli.py -i "stent" -v 4
```

## CLI Arguments

| Argument | Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| **Implant** | `-i`, `--implant` | Name of the medical implant (Required) | N/A |
| **Output Dir** | `-d`, `--output-dir` | Directory for output files | `outputs` |
| **Model** | `-m`, `--model` | LLM model to use | `ollama/gemma3` |
| **Structured** | `-s`, `--structured` | Use Pydantic model for JSON output | `False` |
| **Quick** | `--quick` | Skip structured enforcement for faster text | `False` |
| **Verbosity** | `-v`, `--verbosity` | Logging level (0-4) | `2` (WARNING) |

## Data Structure

When using `--structured`, the output follows the `MedicalImplantInfoModel` schema, which includes:

*   **Metadata:** Name, type, manufacturers.
*   **Purpose & Indications:** Therapeutic uses, conditions treated.
*   **Materials:** Biocompatibility, material properties.
*   **Installation:** Surgical steps, anesthesia, duration.
*   **Functionality:** Mechanism of action, lifespan.
*   **Recovery:** Healing timeline, pain management.
*   **Risks:** Complications, infection risks.
*   **Maintenance:** Long-term care, replacement needs.
*   **Cost & Insurance:** Financial considerations.
*   **Patient Education:** Layman explanations and tips.

## Project Structure

*   `medical_implant_cli.py`: CLI entry point and argument parsing.
*   `medical_implant.py`: Core logic for coordinating the LLM request and saving results.
*   `medical_implant_models.py`: Pydantic data definitions for structured output.
*   `medical_implant_prompts.py`: System and user prompt construction.
*   `assets/medical_implants.json`: Reference list of common medical implants.