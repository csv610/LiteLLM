# SocratesTutor

`SocratesTutor` is an interactive tutor that uses question-led dialogue to examine a concept, claim, or problem.

## What It Does

- Runs a CLI conversation using a Socratic questioning style.
- Encourages clarification, justification, and refinement of the user's reasoning.
- Stores the tutoring logic separately from the prompt templates.

## Why It Matters

This tutor is useful when the primary goal is reflective reasoning rather than direct instruction.

## Files

- `socrates_tutor.py`: tutoring logic.
- `socrates_tutor_cli.py`: CLI entrypoint.
- `socrates_tutor_prompts.py`: prompts.

## Usage

```bash
python socrates_tutor_cli.py
```

## Limitations

- The tutor can ask productive questions without ensuring the final conclusion is correct.
- It is better suited to exploration than to factual verification.
- Conversation quality depends on the model and user responses.
