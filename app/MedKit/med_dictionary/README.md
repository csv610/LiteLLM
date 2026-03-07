# Medical Dictionary

This package contains tools for building, classifying, and reviewing medical terminology datasets.

## Files

- `medical_dictionary_cli.py`: CLI entrypoint.
- `medical_term_classify.py`: term classification logic.
- `dictionary_builder.py`: dictionary construction helper.
- `extract_medical_codes.py`: code extraction helper.
- `review_medical_dictionary.py`: review helper.

## Why It Matters

Medical terminology work often mixes extraction, classification, and review. This package keeps those tasks together.

## Limitations

- Classification quality depends on the model and prompts.
- Terminology resources may require manual curation before external use.
