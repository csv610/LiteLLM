# Quadrails

`Quadrails` analyzes text or images for safety-related categories and returns a structured assessment.

## What It Does

- Accepts either text or an image path.
- Runs asynchronous analysis through `GuardrailAnalyzer`.
- Covers multiple safety categories defined in the prompt and model schema.
- Supports optional in-memory caching.

## Why It Matters

Applications that call LLMs often need a reusable moderation layer before or after generation. This app packages that step as a separate CLI and Python module.

## What Distinguishes It

- Handles both text and images.
- Uses typed result schemas and a custom exception hierarchy.
- Supports caching and length limits in the CLI layer.

## Files

- `guardrail.py`: core analyzer.
- `guardrail_cli.py`: CLI interface.
- `guardrail_models.py`: schemas and custom errors.
- `guardrail_prompts.py`: moderation prompts.
- `test_guardrail_mock.py`, `test_guardrail_cli_mock.py`: tests.

## Usage

```bash
python guardrail_cli.py --text "Check this text for safety"
python guardrail_cli.py --image ./sample.jpg
```

Defaults:

- `--model`: `$GUARDRAIL_MODEL` or `ollama/gemma3`
- `--max-length`: `4000`

## Testing

```bash
pytest test_guardrail_mock.py test_guardrail_cli_mock.py
```

## Limitations

- Safety classification depends on model behavior and prompt coverage.
- The results are useful as a screening layer, not as a legal or policy determination.
- Categories and thresholds should be validated against the deployment context.
