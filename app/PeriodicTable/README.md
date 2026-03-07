# PeriodicTable

`PeriodicTable` generates structured element information for one element or for all elements in the built-in list.

## What It Does

- Accepts a single element name or the `--all` flag.
- Produces JSON output for individual elements.
- When `--all` is used, also writes a consolidated `all_elements.json`.

## Why It Matters

This app provides a uniform JSON representation for element descriptions, which is useful for downstream processing or educational datasets.

## What Distinguishes It

- Supports both single-element lookup and batch generation.
- Uses typed models for element structure.
- Writes one file per element plus an optional aggregate file.

## Files

- `periodic_table_cli.py`: CLI interface.
- `periodic_table_element.py`: generation logic and element list.
- `periodic_table_models.py`: schemas.
- `tests/`: test files.

## Usage

```bash
python periodic_table_cli.py
python periodic_table_cli.py --element Gold
python periodic_table_cli.py --all
```

Defaults:

- `--element`: `Hydrogen`
- `--model`: `ollama/gemma3:12b`
- `--temperature`: `0.2`
- `--output-dir`: `outputs`

## Limitations

- Generated element data may omit or misstate values.
- `--all` can take substantial time and cost depending on the model backend.
- Scientific facts should be verified before reuse in reference material.
