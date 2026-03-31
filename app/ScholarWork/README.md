# ScholarWork

`ScholarWork` generates narrative-driven explanations of major scientific contributions by famous scholars. It follows the pattern established by `MathEquationStory`, focusing on the intellectual journey and historical context rather than dry technical details.

## What It Does

- Accepts the name of a scholar (e.g., "Albert Einstein", "Marie Curie") and optionally a specific contribution (e.g., "General Relativity", "Radioactivity").
- Produces a structured narrative essay with a title, subtitle, flowing story, key terms, impact summary, and discussion questions.
- Offers both a simple one-pass generation (`nonagentic`) and a high-quality 3-agent pipeline (`agentic`).

## Why It Matters

Scientific breakthroughs are often taught as isolated facts. `ScholarWork` brings these discoveries to life by placing them in their human and historical context, making the logic of discovery intuitive and engaging for a general audience.

## Core Pipeline (Agentic)

The `agentic` version uses a specialized 3-agent workflow to ensure high-quality, professional science journalism:

1.  **The Researcher:** Gathers deep historical context, scientific principles, and human-interest anecdotes to build a `ResearchBrief`.
2.  **The Journalist:** Transforms the brief into a beautiful, flowing narrative without headers, capturing the intellectual "Aha!" moment.
3.  **The Editor:** Packages the story with a compelling title, key terms, an impact summary, and thought-provoking discussion questions.

## Directory Structure

- `agentic/`: High-quality 3-agent orchestration engine.
- `nonagentic/`: Simple one-pass structured generation.
- `tests/`: Mock-based unit tests for both versions.

## Usage

Run these commands from the project root (ensure the parent directory is in your `PYTHONPATH`):

### Non-Agentic (Simple)

```bash
python -m nonagentic.scholar_work_cli "Albert Einstein" "General Relativity"
```

### Agentic (High Quality)

```bash
python -m agentic.scholar_work_cli "Marie Curie" "Radioactivity"
```

**Default model:** `ollama/gemma3` (Customizable via `--model` flag).

## Testing

Comprehensive unit tests are included for both pipelines:

```bash
# Run all tests
pytest tests/

# Run specific tests
pytest tests/test_scholar_work_mock.py         # Non-agentic
pytest tests/test_scholar_work_agentic_mock.py # Agentic
```

## Data Models

The project uses Pydantic to ensure structured, reliable outputs:
- `ScholarMajorWork`: The final article structure.
- `ResearchBrief`: intermediate data for the agentic pipeline.

## Limitations

- Emphasizes narrative and intuition over technical rigor.
- Historical details may be dramatized for narrative flow.
- Should be used as an educational supplement, not a primary historical or scientific reference.
