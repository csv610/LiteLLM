# HadamardTutor

`HadamardTutor` is an interactive tutor that structures a learning session around preparation, incubation, illumination, and verification.

## What It Does

- Guides the user through staged conceptual exploration.
- Uses prompt templates aligned with a four-stage discovery workflow.
- Runs as a CLI conversation.

## Why It Matters

This tutor is useful when the objective is to work through a difficult idea as a staged discovery process rather than receive a direct summary.

## Files

- `hadamard_tutor.py`: tutoring logic.
- `hadamard_tutor_cli.py`: CLI entrypoint.
- `hadamard_tutor_prompts.py`: prompts.

## Usage

```bash
python hadamard_tutor_cli.py
```

## Limitations

- Stage boundaries are prompt-driven rather than cognitively validated.
- The tool supports guided reflection, not formal assessment.
- Output quality depends on the underlying model.
