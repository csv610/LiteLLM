# MedKit

`MedKit` is a collection of CLI tools for medical information extraction, medical writing support, entity recognition, diagnostics-related reference generation, and privacy-oriented utilities. It is a software toolkit for research and educational workflows, not a medical device.

## What It Does

The package installs the following top-level commands:

- `medkit-medical`: general medical information tools
- `medkit-drug`: pharmacology and interaction tools
- `medkit-diagnose`: diagnostic tests, images, and devices
- `medkit-recognizer`: medical entity recognition
- `medkit-article`: article search, review, comparison, summary, and keyword extraction
- `medkit-graph`: graph-style extraction for medical concepts
- `medkit-privacy`: privacy and compliance utilities
- `medkit-legal`: patient-rights and medical-legal material
- `medkit-exam`: physical examination workflows
- `medkit-agent`: orchestration layer across tools
- `medkit-sane`: SANE interview tooling
- `medkit-dictionary`: medical dictionary tooling
- `medkit-codes`: ICD-11 lookup
- `medkit-mental`: mental-health chat interface
- `medkit-media`: medical media workflow

## Why It Matters

Medical NLP and medical reference tasks tend to split across many narrow scripts. This folder consolidates related workflows into installable command-line tools with typed outputs and shared model configuration.

## What Distinguishes It

- Multiple medical workflows in one package rather than a single-purpose app.
- Includes both generation tasks and recognition/extraction tasks.
- Provides installable console scripts through `pyproject.toml`.

## Notable Subcommand Groups

`medkit-medical` includes modules such as `anatomy`, `disease`, `advise`, `decision`, `faq`, `history`, `ethics`, `procedure`, `eval-procedure`, `quiz`, `refer`, `roles`, `surgery`, `pose`, `tool`, `tray`, `media`, and others.

`medkit-drug` includes `list`, `info`, `interact`, `food`, `disease`, `similar`, `compare`, `symptoms`, `addiction`, `explain`, and `prescription`.

`medkit-recognizer` covers multiple medical entity classes including anatomy, disease, drug, symptoms, procedures, devices, specialties, tests, vaccines, and related categories.

## Installation

From this directory:

```bash
pip install -e .
```

This installs the console scripts declared in `pyproject.toml`.

## Examples

```bash
medkit-agent "70yo on warfarin with a new cough. Check interactions and referral."
medkit-drug interact "Lisinopril" "Ibuprofen"
medkit-medical anatomy "femur"
medkit-recognizer disease "Patient presents with acute bronchitis."
medkit-article search "asthma inhaled corticosteroids"
```

## Outputs

Many subcommands write to an `outputs/` directory by default, though exact behavior varies by module.

## Limitations

- These tools depend on LLM output and may produce incorrect or incomplete medical information.
- Structured output does not make the content clinically validated.
- The package is not suitable for unsupervised diagnosis or treatment decisions.
- Privacy-sensitive workflows should still be reviewed against local legal and institutional requirements.

## Disclaimer

Use for research, prototyping, and education. Do not treat this package as a substitute for licensed clinical judgment.
