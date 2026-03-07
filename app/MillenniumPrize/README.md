# MillenniumPrize

`MillenniumPrize` provides a CLI for the seven Clay Mathematics Institute Millennium Prize Problems.

## What It Does

- Lists the seven problems from the built-in dataset.
- Can generate an additional model-produced explanation for a selected problem.
- Saves JSON output to the current working directory.

## Why It Matters

The Millennium Prize Problems are a compact set of high-impact open problems. This app provides a simple way to retrieve them in a consistent format.

## What Distinguishes It

- Uses a built-in data table for the seven problems.
- Optionally augments that data with a generated explanation.
- Keeps the scope narrow and fixed.

## Files

- `millennium_prize_problems_cli.py`: CLI entrypoint.
- `millennium_prize_models.py`: schemas.
- `millennium_prize_prompts.py`: prompt builder.
- `mock_test_millennium_prize.py`: tests.

## Usage

```bash
python millennium_prize_problems_cli.py
python millennium_prize_problems_cli.py --problem 1
python millennium_prize_problems_cli.py --problem 3 --model gpt-4
```

Default model for generated explanations: `ollama/gemma3`

Note: when a specific problem is requested, the current CLI attempts to generate an explanation unless the code is changed.

## Testing

```bash
python -m unittest mock_test_millennium_prize.py
```

## Limitations

- The built-in problem metadata is static.
- Generated explanations are not authoritative mathematical references.
- The CLI behavior currently couples single-problem lookup with model-based explanation generation.
