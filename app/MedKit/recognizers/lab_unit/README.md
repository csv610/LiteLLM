# Lab Unit Identifier

Identifies whether a given name is a recognized laboratory unit in medical literature.

## Purpose

Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs.

## Usage

```bash
python lab_unit_cli.py "example laboratory_unit"
```

## Output

```json
{
  "identification": {
    "name": "Example Laboratory unit",
    "is_well_known": true,
    "recognition_confidence": "high",
    "medical_literature_reference": "Recognized in major medical databases and literature"
  },
  "summary": "Example Laboratory unit is a recognized laboratory unit in medical literature",
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
python test_lab_unit_identifier.py
```

## Disclaimer

For identification purposes only. Not a substitute for professional medical advice.
