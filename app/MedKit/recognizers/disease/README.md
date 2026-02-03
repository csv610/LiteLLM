# Disease Identifier

Identifies whether a given name is a recognized disease in medical literature.

## Purpose

Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs.

## Usage

```bash
python disease_identifier_cli.py "diabetes mellitus"
```

## Output

```json
{
  "identification": {
    "disease_name": "Diabetes Mellitus",
    "is_well_known": true,
    "recognition_confidence": "high",
    "medical_literature_reference": "Recognized in ICD-10 and major medical databases"
  },
  "summary": "Diabetes Mellitus is a recognized disease in medical literature",
  "data_available": true
}
```

## Installation

```bash
cd /Users/csv610/Projects/LiteLLM
pip install -r requirements.txt
```

## Testing

```bash
python test_disease_identifier.py
```

## Disclaimer

For identification purposes only. Not a substitute for professional medical advice.
