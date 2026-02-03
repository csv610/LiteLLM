# Clinical Sign Identifier

Identifies whether a given name is a recognized clinical sign in medical literature.

## Purpose

Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs.

## Usage

```bash
python clinical_sign_cli.py "example clinical_sign"
```

## Output

```json
{
  "identification": {
    "name": "Example Clinical sign",
    "is_well_known": true,
    "recognition_confidence": "high",
    "medical_literature_reference": "Recognized in major medical databases and literature"
  },
  "summary": "Example Clinical sign is a recognized clinical sign in medical literature",
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
python test_clinical_sign_identifier.py
```

## Disclaimer

For identification purposes only. Not a substitute for professional medical advice.
