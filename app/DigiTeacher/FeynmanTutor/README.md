# FeynmanTutor

`FeynmanTutor` is an interactive tutor that explains a topic in progressively simpler terms and asks follow-up questions to check understanding.

## What It Does

- Runs a CLI conversation around a user-selected topic.
- Uses prompt templates designed for simplification and iterative clarification.
- Maintains conversational state through the tutoring session.

## Why It Matters

This tutor is useful when the learning goal is explanation and self-checking rather than reference lookup.

## Files

- `feynman_tutor.py`: tutoring logic.
- `feynman_tutor_cli.py`: CLI entrypoint.
- `feynman_tutor_prompts.py`: prompts.

## Usage

```bash
python feynman_tutor_cli.py
```

## Limitations

- Teaching quality depends on the model.
- The tutor does not independently verify correctness.
- Explanations may prioritize accessibility over technical completeness.
