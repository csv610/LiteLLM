# MedKit Drug

This package groups the pharmacology-related MedKit modules.

## What It Includes

- `info`: medicine information
- `interact`: drug-drug interaction analysis
- `food`: drug-food interaction analysis
- `disease`: drug-disease interaction analysis
- `similar`: similar or alternative medicines
- `compare`: side-by-side medicine comparison
- `symptoms`: symptom-to-drug-category suggestions
- `addiction`: addiction-related information
- `explain`: plain-language medicine explanation
- `prescription`: prescription-image analysis

## Entry Point

- `drug_cli.py`: unified CLI used by `medkit-drug`

## Why It Matters

These modules cover several common medication-reference tasks through one CLI rather than separate unrelated scripts.

## Limitations

- The outputs are informational and model-dependent.
- Drug safety decisions should not rely on generated output alone.
