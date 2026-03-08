# Drug-Disease Interaction Analyzer

A clinical decision support module for identifying potential risks, contraindications, and precautions when specific medications are prescribed for patients with pre-existing medical conditions.

## Overview

The **Drug-Disease Interaction Analyzer** evaluates the safety profile of medicines relative to specific diseases or conditions. By combining standardized pharmacological insights with advanced AI analysis, it provides healthcare professionals and patients with structured reports on how a medication might adversely affect or be affected by a concurrent health condition.

## Key Features

- **Contraindication Identification:** Clearly identifies when a medication is strictly discouraged for a specific condition.
- **Precautions and Warnings:** Flags necessary monitoring or dosage adjustments for patients with relevant comorbidities.
- **Pathophysiological Explanation:** Explains *why* an interaction occurs (e.g., impact on organ function, exacerbation of symptoms).
- **Clinical Severity Assessment:** Categorizes risks into severity levels (e.g., NONE, CAUTION, CONTRAINDICATED).
- **Patient-Friendly Warnings:** Translates complex clinical interactions into clear advice and warning signs for patients.
- **Structured Data:** Delivers results via Pydantic models for seamless integration into electronic health records (EHR) or other health systems.

## Project Structure

- `drug_disease_interaction.py`: Core logic for interaction analysis and model orchestration.
- `drug_disease_interaction_cli.py`: Feature-rich command-line interface.
- `drug_disease_interaction_models.py`: Robust Pydantic data schemas.
- `drug_disease_interaction_prompts.py`: Specialized prompt engineering for clinical accuracy.
- `assets/`: Reference data (e.g., lists of known harmful drug-disease pairs).
- `tests/`: Comprehensive test suite (live and mock).

## Installation

Ensure dependencies are installed:

```bash
pip install pydantic argparse
```

*Note: Depends on the internal `lite` library.*

## Usage

### Command Line Interface

Check the interaction between a medicine and a disease:

```bash
python drug_disease_interaction_cli.py "Naproxen" "Peptic Ulcer" --structured
```

**Arguments:**
- `medicine`: The name of the medication.
- `disease`: The medical condition or disease name.
- `--structured`: (Optional) Output as validated JSON.
- `--model`: (Optional) LLM Model ID to use.

### Python API

```python
from drug_disease_interaction import DrugDiseaseInteractionGenerator
from drug_disease_interaction_prompts import DrugDiseaseInput

generator = DrugDiseaseInteractionGenerator()
user_input = DrugDiseaseInput(
    medicine="Metformin",
    disease="Severe Renal Impairment"
)

result = generator.generate_text(user_input=user_input, structured=True)
print(result.data.overall_severity)
```

## ⚠️ Important Medical Disclaimer

**THIS MODULE IS FOR INFORMATIONAL AND REFERENCE PURPOSES ONLY.**

- **Professional Consultation Required:** Never change or stop a medication based on this tool without consulting a physician.
- **Incomplete Context:** The analyzer may not account for the full spectrum of patient history, dosage levels, or concurrent therapies.
- **AI Limitations:** Clinical data must be verified against authoritative medical textbooks and FDA-approved labeling.
