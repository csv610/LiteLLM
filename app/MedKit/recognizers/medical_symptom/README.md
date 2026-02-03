# Medical Symptom Identifier

Identifies whether a given name is a recognized symptom in medical literature.

## Purpose

Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs.

## Usage

```bash
python medical_symptom_cli.py "example symptom"
```

## Output

```json
{
  "identification": {
    "name": "Example Symptom",
    "is_well_known": true,
    "recognition_confidence": "high",
    "medical_literature_reference": "Recognized in major medical databases and literature"
  },
  "summary": "Example Symptom is a recognized symptom in medical literature",
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
python test_medical_symptom_identifier.py
```

## Disclaimer

For identification purposes only. Not a substitute for professional medical advice.
