# MedKit Diagnose

This package groups diagnostic-reference and medical-image modules.

## What It Includes

- `test`: medical test information
- `device`: diagnostic device information
- `classify_image`: image classification

## Entry Point

- `diagnose_cli.py`: unified CLI used by `medkit-diagnose`

## Why It Matters

Diagnostic tests, devices, and images are related but operationally different tasks. This package keeps them under one command namespace.

## Limitations

- Outputs are reference-oriented and model-dependent.
- Image classification results should not be used as clinical diagnosis.
