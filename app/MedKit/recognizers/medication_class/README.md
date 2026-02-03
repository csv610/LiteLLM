# Medication Class Identifier

Identifies whether a given name is a recognized medication class in medical literature.

## Purpose

Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs.

## Usage

```bash
python medication_class_cli.py "example medication_class"
```

## Output

```json
{
  "identification": {
    "name": "Example Medication class",
    "is_well_known": true,
    "recognition_confidence": "high",
    "medical_literature_reference": "Recognized in major medical databases and literature"
  },
  "summary": "Example Medication class is a recognized medication class in medical literature",
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
python test_medication_class_identifier.py
```

## Disclaimer

For identification purposes only. Not a substitute for professional medical advice.
