# MathTheories

`MathTheories` generates level-specific explanations for mathematical theories and saves them as Markdown.

## What It Does

- Accepts a theory name and an audience level.
- Generates an explanation covering introduction, key concepts, motivation, applications, and current research.
- Writes the result to `outputs/theories/`.

## Why It Matters

The same topic often needs different explanations for different audiences. This app provides one interface for that adaptation.

## What Distinguishes It

- Audience-aware generation from `general` through `researcher`.
- Markdown export suitable for notes or documentation.
- Uses typed models for the generated structure.

## Files

- `math_theory_cli.py`: CLI interface.
- `math_theory_element.py`: theory explanation logic.
- `math_theory_models.py`: schemas and enums.
- `assets/theories.txt`: list of supported theories.
- `tests/`: test files.

## Usage

```bash
python math_theory_cli.py --theory "Group theory"
python math_theory_cli.py --theory "Knot theory" --level general
python math_theory_cli.py --theory "Chaos theory" --level phd
```

Defaults:

- `--theory`: `Group theory`
- `--level`: `undergrad`
- `--model`: `ollama/gemma3:12b`
- `--output-dir`: `outputs/theories`

## Testing

This folder contains test files under `tests/`.

## Limitations

- Audience adaptation is prompt-based and may still be uneven across topics.
- The generated text is explanatory rather than source-cited.
- Formal accuracy should be reviewed for advanced mathematical use.
