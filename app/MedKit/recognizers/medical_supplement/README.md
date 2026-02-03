# Medical Supplement Identifier

Identifies whether a given name is a recognized medical supplement in medical literature.

## Purpose

Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs.

## Usage

```bash
python medical_supplement_cli.py "example medical_supplement"
```

## Output

```json
{
  "identification": {
    "name": "Example Medical supplement",
    "is_well_known": true,
    "recognition_confidence": "high",
    "medical_literature_reference": "Recognized in major medical databases and literature"
  },
  "summary": "Example Medical supplement is a recognized medical supplement in medical literature",
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
python test_medical_supplement_identifier.py
```

## Disclaimer

For identification purposes only. Not a substitute for professional medical advice.
