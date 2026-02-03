# Genetic Variant Identifier

Identifies whether a given name is a recognized genetic variant in medical literature.

## Purpose

Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs.

## Usage

```bash
python genetic_variant_cli.py "example genetic_variant"
```

## Output

```json
{
  "identification": {
    "name": "Example Genetic variant",
    "is_well_known": true,
    "recognition_confidence": "high",
    "medical_literature_reference": "Recognized in major medical databases and literature"
  },
  "summary": "Example Genetic variant is a recognized genetic variant in medical literature",
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
python test_genetic_variant_identifier.py
```

## Disclaimer

For identification purposes only. Not a substitute for professional medical advice.
