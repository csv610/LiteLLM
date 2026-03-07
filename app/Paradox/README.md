# Paradox

`Paradox` generates audience-specific explanations of philosophical, logical, or scientific paradoxes and saves them as Markdown.

## What It Does

- Accepts a paradox name and audience level.
- Generates sections such as status, root cause, historical context, contradiction, modern relevance, and resolution.
- Writes the result to `outputs/paradoxes/`.

## Why It Matters

Paradoxes are often discussed informally. This app provides a fixed explanatory template that is easier to compare across audience levels.

## What Distinguishes It

- Audience-specific generation from `general` through `researcher`.
- Includes explicit status and resolution fields.
- Exports Markdown for easy review.

## Files

- `paradox_cli.py`: CLI interface.
- `paradox_element.py`: explanation logic.
- `paradox_models.py`: schemas.
- `tests/`: test files.

## Usage

```bash
python paradox_cli.py --paradox "Zeno's paradox"
python paradox_cli.py --paradox "Fermi paradox" --level researcher
```

Defaults:

- `--paradox`: `Zeno's paradox`
- `--level`: `undergrad`
- `--model`: `ollama/gemma3:12b`
- `--output-dir`: `outputs/paradoxes`

## Testing

This folder contains test files under `tests/`.

## Limitations

- Paradox interpretation can vary across philosophical traditions.
- Resolution fields may present one framing more strongly than alternatives.
- The generated material should be treated as explanatory output, not as a scholarly source.
