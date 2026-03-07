# Drug-Disease Interaction

This module generates structured information about whether a medicine may be unsuitable, risky, or noteworthy for a named disease or condition.

## Files

- `drug_disease_interaction.py`: generation logic.
- `drug_disease_interaction_cli.py`: CLI interface.
- `drug_disease_interaction_models.py`: schemas.
- `drug_disease_interaction_prompts.py`: prompts.

## Why It Matters

Drug-disease interactions are a distinct class of safety question and should not be conflated with drug-drug interactions.

## Limitations

- Generated contraindication summaries may omit context such as severity, dose, or comorbidities.
- The output is not a substitute for clinical prescribing guidance.
