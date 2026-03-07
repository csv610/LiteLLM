# Medical Recognizers

This package groups multiple entity-recognition modules used by `medkit-recognizer`.

## What It Includes

- clinical signs, diseases, symptoms, tests, procedures, devices, pathogens, vaccines
- anatomy, medical conditions, specialties, abbreviations, coding, medication classes
- supplements, imaging findings, lab units, and genetic variants

## Entry Point

- `medical_recognizer_cli.py`: unified CLI

## Why It Matters

These recognizers expose a consistent pattern for extracting different classes of medical entities.

## Limitations

- Recognition quality depends on prompt design and model quality.
- Entity extraction should be validated before downstream use.
