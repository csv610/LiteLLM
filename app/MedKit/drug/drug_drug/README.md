# Drug-Drug Interaction

This module analyzes a pair of medicines and generates a structured interaction summary.

## Files

- `drug_drug_interaction.py`: interaction logic.
- `drug_drug_interaction_cli.py`: CLI interface.
- `drug_drug_interaction_models.py`: schemas.
- `drug_drug_interaction_prompts.py`: prompts.

## Why It Matters

Drug-drug interaction screening is a common medication-reference task and benefits from a focused output format.

## Limitations

- Interaction severity can depend on dose, route, timing, and patient-specific factors.
- Generated output should be reviewed against authoritative drug references.
