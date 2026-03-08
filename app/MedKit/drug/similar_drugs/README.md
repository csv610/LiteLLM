# Therapeutic Alternative & Similar Drug Finder

A clinical reference module for identifying medications that are pharmacologically or therapeutically similar to a specified drug.

## Overview

The **Therapeutic Alternative Finder** identifies medicines with comparable indications, mechanisms of action, or therapeutic classes. It is designed to assist healthcare professionals in exploring drug alternatives and to help patients understand the therapeutic landscape of their medications.

## Key Features

- **Similarity Analysis:** Evaluates drugs based on therapeutic class, clinical indication, and pharmacological effect.
- **Alternative Candidates:** Suggests a list of potential substitutes or similar treatments.
- **Interchangeability Assessment:** Briefly discusses the clinical considerations for switching medications (e.g., potency, side-effect profile).
- **Clinical Rationale:** Explains *why* two drugs are considered similar.
- **Structured Outputs:** Uses Pydantic models for validated, machine-readable data delivery.
- **Confidence Scoring:** Assesses the clinical reliability of the suggested alternatives.

## Project Structure

- `similar_drugs.py`: Core logic for similarity identification and analysis.
- `similar_drugs_cli.py`: Command-line tool for drug comparison.
- `similar_drugs_models.py`: Data schemas defining the similarity model.
- `similar_drugs_prompts.py`: Optimized prompt templates for therapeutic alternative identification.

## Installation

Ensure dependencies are installed:

```bash
pip install pydantic argparse
```

*Note: Depends on the internal `lite` library.*

## Usage

### Command Line Interface

Find similar drugs to a specified medication:

```bash
python similar_drugs_cli.py "Ibuprofen" --structured
```

**Arguments:**
- `medicine`: The name of the medication to find alternatives for.
- `--structured`: (Optional) Output as validated JSON.
- `--model`: (Optional) LLM Model ID to use.

### Python API

```python
from similar_drugs import SimilarDrugsGenerator
from similar_drugs_prompts import SimilarDrugsInput

generator = SimilarDrugsGenerator()
user_input = SimilarDrugsInput(
    medicine_name="Lisinopril"
)

result = generator.generate_text(user_input=user_input, structured=True)
print(result.data.similar_drugs_list)
```

## ⚠️ Important Medical Disclaimer

**THIS MODULE IS FOR INFORMATIONAL PURPOSES ONLY.**

- **No Implicit Interchangeability:** Similarity in class or mechanism does **not** mean two medications are interchangeable or bioequivalent.
- **Clinical Review Mandatory:** Switching medications requires a thorough review of the patient's history, contraindications, and potential interactions by a qualified physician.
- **Dosage Variability:** Therapeutic alternatives often require different dosing regimens and monitoring.
