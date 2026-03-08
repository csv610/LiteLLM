# Drug-Drug Interaction Analyzer

A specialized clinical decision support tool for analyzing potential interactions between medications. This module leverages large language models (LLMs) to provide structured, evidence-based insights into drug-drug interactions (DDIs), covering pharmacological mechanisms, clinical effects, and management recommendations.

## Overview

The Drug-Drug Interaction Analyzer evaluates pairs of medicines to identify contraindications, synergistic effects, or adverse interactions. It provides two layers of analysis:
1.  **Clinical/Technical:** Detailed pharmacological mechanisms and management strategies for healthcare professionals.
2.  **Patient-Centric:** Simplified explanations and actionable advice for patients.

## Key Features

-   **Structured Analysis:** Generates data in machine-readable JSON format (via Pydantic) or human-readable Markdown.
-   **Severity Scoring:** Categorizes interactions from `NONE` to `CONTRAINDICATED`.
-   **Clinical Context:** Supports patient-specific factors such as age, dosages, and existing medical conditions.
-   **Evidence-Based:** Includes confidence levels and references for identified interactions.
-   **Flexible Prompting:** Multiple styles (`detailed`, `concise`, `balanced`) to suit different use cases.

## Project Structure

-   `drug_drug_interaction.py`: Core logic for interaction generation and LLM integration.
-   `drug_drug_interaction_cli.py`: Command-line interface for interactive use.
-   `drug_drug_interaction_models.py`: Pydantic schemas for structured data validation.
-   `drug_drug_interaction_prompts.py`: Template management for LLM instructions.
-   `assets/`: Supplementary data (e.g., common harmful drug lists).
-   `tests/`: Comprehensive test suite including mock and live integration tests.

## Installation

Ensure you have the core `MedKit` environment configured. This module typically requires:

```bash
pip install -r requirements.txt  # From project root
```

*Note: This module depends on the `lite` library for LLM communication.*

## Usage

### Command Line Interface

Analyze the interaction between two drugs:

```bash
python drug_drug_interaction_cli.py "Warfarin" "Aspirin" --age 65 --style detailed --structured
```

**Arguments:**
-   `medicine1`, `medicine2`: Names of the drugs to analyze.
-   `--age`: Patient age for tailored risk assessment.
-   `--dosage1`, `--dosage2`: Specific dosage information.
-   `--conditions`: Comorbidities (comma-separated).
-   `--structured`: Output as validated JSON.
-   `--style`: Output detail level (`detailed`, `concise`, `balanced`).

### Python API

```python
from drug_drug_interaction import DrugDrugInteractionGenerator
from drug_drug_interaction_prompts import DrugDrugInput

generator = DrugDrugInteractionGenerator()
user_input = DrugDrugInput(
    medicine1="Simvastatin",
    medicine2="Clarithromycin",
    age=50
)

result = generator.generate_text(user_input=user_input, structured=True)
print(result.data.interaction_details.severity_level)
```

## Data Models

The analyzer uses a strict schema (`DrugInteractionModel`) which includes:
-   `severity_level`: (MINOR, MODERATE, SIGNIFICANT, CONTRAINDICATED, etc.)
-   `mechanism_of_interaction`: Pharmacokinetic or pharmacodynamic explanation.
-   `management_recommendations`: Actionable clinical steps.
-   `patient_friendly_summary`: Simple language explanation and warning signs.

## Testing

Run the test suite to verify functionality:

```bash
# Mock tests (No LLM calls)
pytest tests/test_mock_drug_drug.py

# Live tests (Requires API configuration)
pytest tests/test_live_drug_drug.py
```

## Important Medical Disclaimer

**This tool is for informational and educational purposes only.** 
- It is **not** a substitute for professional medical advice, diagnosis, or treatment. 
- Always seek the advice of a physician or other qualified health provider with any questions regarding a medical condition or drug interactions.
- AI-generated content may contain inaccuracies; all outputs must be verified against authoritative clinical references (e.g., Lexicomp, Micromedex, or FDA labels).
