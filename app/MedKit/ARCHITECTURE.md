# MedKit Architecture

MedKit is organized into domain-focused modules:

- `recognizers/`: Entity recognition (disease, symptom, drug, device, etc.).
- `drug/`: Drug metadata, interactions, and safety checks.
- `medical/`: Medical knowledge and education helpers.
- `phyexams/`: Physical examination guidance workflows.
- `mental_health/`: Mental health and screening workflows.
- `diagnostics/`: Medical tests and medical device support.
- `utils/`: Shared utilities used by MedKit modules.

## Integration Pattern

Most modules follow the same structure:

1. Prompt builder
2. Data model (Pydantic)
3. CLI wrapper
4. Optional contract and tests

## Runtime Dependencies

- Python 3.8+
- `litellm` client stack
- A configured LLM provider (`ollama/*`, `openai/*`, `anthropic/*`, etc.)
