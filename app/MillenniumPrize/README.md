# MillenniumPrize

`MillenniumPrize` provides a CLI for the seven Clay Mathematics Institute Millennium Prize Problems.
It now uses a lightweight two-agent workflow for single-problem requests.

## What It Does

- Lists the seven problems from the built-in dataset.
- Uses a selection agent to prepare the requested problem.
- Uses an explanation agent to optionally generate a model-produced explanation.
- Saves JSON output to the current working directory.

## Why It Matters

The Millennium Prize Problems are a compact set of high-impact open problems. This app provides a simple way to retrieve them in a consistent format.

## What Distinguishes It

- Uses a built-in data table for the seven problems.
- Splits problem selection and explanation generation into separate agents.
- Keeps the scope narrow and fixed.

## Files

- `millennium_prize_problems_cli.py`: CLI entrypoint.
- `millennium_prize_agents.py`: two-agent workflow.
- `millennium_prize_models.py`: schemas.
- `millennium_prize_prompts.py`: prompt builder.
- `test_millennium_prize_mock.py`: tests.

## Usage

```bash
python millennium_prize_problems_cli.py
python millennium_prize_problems_cli.py --problem 1
python millennium_prize_problems_cli.py --problem 3 --model gpt-4
python millennium_prize_problems_cli.py --problem 3 --no-explanation
```

Default model for generated explanations: `ollama/gemma3`

Note: when a specific problem is requested, the CLI runs the explanation agent by default unless `--no-explanation` is passed.

## Testing

```bash
python -m unittest test_millennium_prize_mock.py
```

## Limitations

- The built-in problem metadata is static.
- Generated explanations are not authoritative mathematical references.
- The app uses a lightweight sequential two-agent workflow rather than concurrent or autonomous agents.
