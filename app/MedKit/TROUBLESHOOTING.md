# MedKit Troubleshooting

## `ModuleNotFoundError` when running module CLIs

- Run commands from repository root: `LiteLLM/`
- Install package in editable mode:
  - `pip install -e .`

## Model/provider authentication errors

- Ensure API keys are set for hosted providers.
- For Ollama, verify the daemon is running and the model is pulled.

## Empty or low-quality outputs

- Use a better-suited model for the task.
- Lower temperature for deterministic extraction tasks.
- Validate that required CLI arguments are provided.

## Import path issues in subdirectories

Prefer execution from repo root using full relative paths:

```bash
python app/MedKit/<module>/<cli_file>.py ...
```
