# Medical Ethics Analysis Generator

This tool generates professional medical ethics analysis for various questions or scenarios. It uses an AI model to provide structured or markdown-based analysis based on clinical ethics principles.

## Features

- **Professional Analysis**: Evaluates scenarios using core ethical principles (Autonomy, Beneficence, Non-maleficence, Justice).
- **Structured Output**: Can generate structured Pydantic-validated data or formatted markdown.
- **Batch Processing**: Supports analyzing multiple scenarios from a file.
- **Customizable**: Works with various LLMs (default: `ollama/gemma3`).

## Usage

### Individual Analysis
```bash
python -m medkit.medical.med_ethics.med_ethics_cli "Is it ethical to use AI for diagnostic purposes without informing the patient?"
```

### Batch Analysis
```bash
python -m medkit.medical.med_ethics.med_ethics_cli assets/medical_ethics_questions.txt
```

### Options
- `-s`, `--structured`: Generate structured JSON output.
- `-m`, `--model`: Specify the LLM model to use.
- `-d`, `--output-dir`: Specify where to save the reports.

## Structure
- `med_ethics.py`: Core generation logic.
- `med_ethics_cli.py`: Command-line interface.
- `med_ethics_models.py`: Pydantic data models for structured output.
- `med_ethics_prompts.py`: Prompt templates for the AI.
- `test_med_ethics.py`: Unit tests.
