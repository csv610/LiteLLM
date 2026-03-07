# DeepIntuition

`DeepIntuition` generates long-form explanatory narratives about mathematical or technical ideas. Its emphasis is historical framing and intuition-building rather than formal proof.

## What It Does

- Accepts a topic such as a theorem, theory, or foundational idea.
- Produces a structured narrative with sections such as historical struggle, "aha" moment, counterfactual framing, and modern resonance.
- Saves the result to `outputs/story_<topic>.json`.

## Why It Matters

Many technical explanations focus on final results and omit the reasoning path that made the result intelligible. This app is useful when the learning goal is conceptual understanding rather than direct problem solving.

## What Distinguishes It

- Narrative structure rather than terse summary.
- Explicit historical and counterfactual sections.
- Structured JSON output despite the long-form format.

## Files

- `deep_intuition.py`: core generator.
- `deep_intuition_cli.py`: CLI entrypoint.
- `deep_intuition_models.py`: response schema.
- `deep_intuition_prompts.py`: prompt logic.
- `deep_intuition_archive.py`: archive support.

## Usage

```bash
python deep_intuition_cli.py --topic "Galois Theory"
python deep_intuition_cli.py --topic "Lambda Calculus" --model "openai/gpt-4"
```

Default model: `$DEFAULT_LLM_MODEL` or `ollama/gemma3`

## Testing

This folder contains mock tests and a live test file.

## Limitations

- Historical narratives produced by an LLM may compress, omit, or misstate details.
- The app is not designed to provide formal proofs or source citations.
- Users should verify historical claims when accuracy is important.
