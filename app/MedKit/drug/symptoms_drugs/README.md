# Symptoms to Drug Categories

This module maps a symptom description to possible medication categories or therapeutic directions.

## Files

- `symptom_drugs.py`: generation logic.
- `symptom_drugs_cli.py`: CLI interface.
- `symptom_drugs_models.py`: schemas.
- `symptom_drugs_prompts.py`: prompts.

## Why It Matters

This workflow is useful for educational triage and high-level pharmacology exploration.

## Limitations

- The module suggests categories, not safe self-medication plans.
- Symptom-based suggestions can miss differential diagnoses and contraindications.
