# Patient Medical History Generator

A CLI tool for generating exam-specific patient medical history questions using AI. This module creates trauma-informed, clinically relevant questions tailored to specific medical examinations, patient demographics, and clinical purposes.

## Features

- **Exam-Specific**: Generates questions relevant to specific medical exams (e.g., cardiac, respiratory).
- **Demographic-Aware**: Tailors questions based on patient age and gender.
- **Purpose-Driven**: Adjusts focus for surgery, medication review, or general physical exams.
- **Structured Output**: Can produce structured JSON data suitable for integration with other systems.
- **Trauma-Informed**: Prompts are designed to be respectful and culturally sensitive.

## File Structure

- **`patient_medical_history_cli.py`**: The command-line entry point for the application.
- **`patient_medical_history.py`**: Contains the core `PatientMedicalHistoryGenerator` class and logic.
- **`patient_medical_history_models.py`**: Defines Pydantic data models for structured input and output.
- **`patient_medical_history_prompts.py`**: Handles the construction of system and user prompts for the LLM.

## Prerequisites

- Python 3.8+
- Access to the internal `lite` library (expected to be in the parent directory structure).
- An appropriate LLM backend (e.g., Ollama, Gemini).

## Usage

Run the tool from the command line using `patient_medical_history_cli.py`.

### Basic Example

```bash
python patient_medical_history_cli.py -e "cardiac" -a 55 -g "male"
```

### Advanced Example

Generate a structured medication review for an 8-year-old female, saving to a specific directory:

```bash
python patient_medical_history_cli.py \
  --exam "general" \
  --age 8 \
  --gender "female" \
  --purpose "medication" \
  --structured \
  --output-dir "./my_medical_reports"
```

### Arguments

| Argument | Flag | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Exam** | `-e`, `--exam` | `str` | Yes | - | Type of medical exam (e.g., cardiac, respiratory). |
| **Age** | `-a`, `--age` | `int` | Yes | - | Patient age in years. |
| **Gender** | `-g`, `--gender` | `str` | Yes | - | Patient gender. |
| **Purpose** | `-p`, `--purpose` | `str` | No | `physical_exam` | Purpose: `physical_exam`, `surgery`, or `medication`. |
| **Output Dir** | `-d`, `--output-dir` | `str` | No | `outputs` | Directory to save the generated output files. |
| **Model** | `-m`, `--model` | `str` | No | `ollama/gemma3` | The LLM model to use for generation. |
| **Structured** | `-s`, `--structured` | `flag` | No | `False` | Use structured JSON output (Pydantic model). |
| **Verbosity** | `-v`, `--verbosity` | `int` | No | `2` | Log level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG. |

## Output

The tool saves the generated questions to the specified output directory.
- **Unstructured**: Plain text questions and clinical rationale.
- **Structured**: JSON file containing categorized questions (Past History, Family History, Lifestyle, etc.) with specific fields for clinical relevance and follow-ups.