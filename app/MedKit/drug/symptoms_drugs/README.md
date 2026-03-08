# Symptom-to-Drug Category Mapper

A specialized triage and pharmacological tool for mapping medical symptom descriptions to relevant drug categories and therapeutic directions.

## Overview

The **Symptom-to-Drug Category Mapper** is designed to facilitate high-level medical exploration and educational triage. It uses advanced language models to identify the drug classes most commonly associated with specific clinical symptoms, helping users navigate the pharmacological landscape based on presenting signs.

## Key Features

- **Symptom Analysis:** Deciphers complex clinical descriptions into standardized medical terms.
- **Therapeutic Classification:** Maps symptoms to relevant drug classes (e.g., NSAIDs, antihistamines, bronchodilators).
- **Clinical Rationale:** Explains the pharmacological basis for why certain drug categories are indicated for a symptom.
- **Urgency Assessment:** Identifies high-risk symptoms that require immediate clinical intervention rather than self-medication.
- **Structured Mapping:** Provides machine-readable outputs using Pydantic models for systematic integration.
- **Confidence Scoring:** Includes an assessment of the reliability of the suggested therapeutic direction.

## Project Structure

- `symptom_drugs.py`: Core logic for mapping and analysis.
- `symptom_drugs_cli.py`: Interactive command-line tool.
- `symptom_drugs_models.py`: Data schemas defining the symptom-to-class mapping model.
- `symptom_drugs_prompts.py`: Prompt templates designed for clinical triage and category identification.
- `logs/`: Diagnostic logs for tracking analysis.
- `contract.md`: Legal and ethical guidelines governing usage.

## Installation

Ensure dependencies are installed:

```bash
pip install pydantic argparse
```

*Note: Depends on the internal `lite` library.*

## Usage

### Command Line Interface

Map a symptom to potential drug categories:

```bash
python symptom_drugs_cli.py "Dry cough and shortness of breath" --structured
```

**Arguments:**
- `symptoms`: A description of the patient's symptoms.
- `--structured`: (Optional) Output as validated JSON.
- `--model`: (Optional) LLM Model ID to use.

### Python API

```python
from symptom_drugs import SymptomDrugsGenerator
from symptom_drugs_prompts import SymptomDrugsInput

generator = SymptomDrugsGenerator()
user_input = SymptomDrugsInput(
    symptoms="Severe nasal congestion and pressure"
)

result = generator.generate_text(user_input=user_input, structured=True)
print(result.data.suggested_drug_categories)
```

## ⚠️ Important Medical Disclaimer

**THIS MODULE IS FOR INFORMATIONAL AND EDUCATIONAL PURPOSES ONLY.**

- **Not for Self-Medication:** This tool suggests drug *categories*, not specific medications or dosing regimens for individual use.
- **Clinical Triage Required:** Symptom-based suggestions are not a substitute for professional diagnosis or the identification of underlying conditions.
- **High-Risk Symptoms:** If you are experiencing chest pain, severe difficulty breathing, or other life-threatening symptoms, contact emergency services immediately.
