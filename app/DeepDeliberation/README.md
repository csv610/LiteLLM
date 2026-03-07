# DeepDeliberation

`DeepDeliberation` is a topic exploration tool that iterates through generated probes and synthesizes a structured research summary. It is intended for exploratory study, not for authoritative literature review.

## What It Does

- Accepts a topic, number of rounds, and number of initial probes.
- Runs repeated analysis rounds over the topic.
- Produces a final structured synthesis with an executive summary, hidden connections, and research frontiers.
- Saves the result to `outputs/discovery_<topic>.json`.

## Why It Matters

For exploratory work, a single prompt often produces a broad but shallow answer. This app adds iteration and synthesis so users can inspect how a topic evolves across multiple rounds.

## What Distinguishes It

- Multi-round exploration rather than one-pass prompting.
- Explicit separation between probe generation, iterative analysis, and final synthesis.
- Structured archival of the final result.

## Files

- `deep_deliberation.py`: core engine.
- `deep_deliberation_cli.py`: CLI entrypoint.
- `deep_deliberation_models.py`: response schemas.
- `deep_deliberation_prompts.py`: prompt logic.
- `deep_deliberation_agents.py`: auxiliary agent logic.
- `deep_deliberation_archive.py`: archive support.

## Usage

```bash
python deep_deliberation_cli.py --topic "The Origin of Consciousness"
python deep_deliberation_cli.py --topic "Category Theory" --num-rounds 5 --num-faqs 7
```

Defaults:

- `--num-rounds`: `3`
- `--num-faqs`: `5`
- `--model`: `$DEFAULT_LLM_MODEL` or `ollama/gemma3`

## Testing

This folder contains both mock tests and live tests.

## Limitations

- Output quality depends on model quality and prompt adherence.
- The generated synthesis is not a substitute for primary literature review.
- The tool does not verify claims against external sources on its own.
