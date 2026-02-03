# Medical Device Identifier

Identifies whether a given name is a recognized medical device in medical literature.

## Purpose

Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs.

## Usage

```bash
python medical_device_cli.py "example medical_device"
```

## Output

```json
{
  "identification": {
    "name": "Example Medical device",
    "is_well_known": true,
    "recognition_confidence": "high",
    "medical_literature_reference": "Recognized in major medical databases and literature"
  },
  "summary": "Example Medical device is a recognized medical device in medical literature",
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
python test_medical_device_identifier.py
```

## Disclaimer

For identification purposes only. Not a substitute for professional medical advice.
