# Medical Pathogen Identifier

Identifies whether a given name is a recognized medical pathogen in medical literature.

## Purpose

Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs.

## Usage

```bash
python medical_pathogen_cli.py "example medical_pathogen"
```

## Output

```json
{
  "identification": {
    "name": "Example Medical pathogen",
    "is_well_known": true,
    "recognition_confidence": "high",
    "medical_literature_reference": "Recognized in major medical databases and literature"
  },
  "summary": "Example Medical pathogen is a recognized medical pathogen in medical literature",
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
python test_medical_pathogen_identifier.py
```

## Disclaimer

For identification purposes only. Not a substitute for professional medical advice.
