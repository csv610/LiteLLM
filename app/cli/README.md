# cli

This folder contains standalone command-line scripts and data-processing helpers that do not fit under a single app-specific package.

## What It Contains

- `liteclient_cli.py`: unified text and image CLI for the local Lite client.
- `llm_judge.py`: judging or comparison utilities.
- `multiple_choice_solver.py`: multiple-choice workflow helper.
- `keyword_extraction.py`: keyword extraction utility.
- `dictionary_builder.py`: medical dictionary-related helper.
- scraping and collection scripts for medical term datasets.

## Why It Matters

This folder acts as a workspace for general-purpose scripts, quick experiments, and data collection utilities used elsewhere in the repository.

## What Distinguishes It

- Mixed utilities rather than one cohesive application.
- Includes both input datasets and processing scripts.
- Useful for development support and local experimentation.

## Limitations

- The folder is heterogeneous by design, so usage patterns vary by script.
- Some scripts depend on local data files or repository-specific imports.
- There is no single installation or execution path for the entire folder.
