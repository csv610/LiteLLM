# UnsolvedProblems

`UnsolvedProblems` generates structured lists of open problems for a topic such as mathematics, physics, or computer science.

## What It Does

- Accepts a topic and number of problems.
- Generates a list of structured problem records.
- Saves the result to `outputs/unsolved_<topic>_<count>.json`.

## Why It Matters

Open-problem lists are useful for study planning and topic exploration, but they are often scattered across multiple sources. This app produces a consistent JSON representation.

## What Distinguishes It

- Topic-based generation rather than a fixed built-in dataset.
- Typed output with fields such as title, description, significance, and status.
- Automatic output archiving.

## Files

- `unsolved_problems_cli.py`: CLI interface.
- `unsolved_problems_explorer.py`: generation logic.
- `unsolved_problems_models.py`: schemas.
- `unsolved_problems_prompts.py`: prompt builder.

## Usage

```bash
python unsolved_problems_cli.py --topic "Mathematics" --num-problems 5
python unsolved_problems_cli.py --topic "Cryptography" --num-problems 3 --model ollama/gemma3
```

Defaults:

- `--model`: `$DEFAULT_LLM_MODEL` or `ollama/gemma3`

## Limitations

- The app does not verify whether a listed problem is still open.
- Topic coverage depends on model knowledge rather than a maintained problem database.
- Results should be checked against current field-specific references.
