# Similar Drugs

This module generates candidates that are similar to a named medicine, typically by therapeutic role or class.

## Files

- `similar_drugs.py`: generator logic.
- `similar_drugs_cli.py`: CLI interface.
- `similar_drugs_models.py`: schemas.
- `similar_drugs_prompts.py`: prompts.

## Why It Matters

Alternative-drug queries are common in educational and exploratory workflows.

## Limitations

- Similarity does not imply interchangeability.
- Switching therapy requires clinical review of indications, contraindications, and dosage.
