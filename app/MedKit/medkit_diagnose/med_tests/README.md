# Medical Tests

This module generates structured descriptions of laboratory or diagnostic tests.

## Files

- `medical_test_info.py`: generation logic.
- `medical_test_info_cli.py`: CLI interface.
- `medical_test_info_models.py`: schemas.
- `medical_test_info_prompts.py`: prompts.

## Why It Matters

Test descriptions often need to combine purpose, specimen, interpretation context, and limitations in a reusable format.

## Limitations

- Reference ranges and interpretation rules vary by lab, method, and patient context.
- Output should be checked against current clinical references.
