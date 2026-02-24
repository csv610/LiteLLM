# MedKit API Notes

MedKit is primarily CLI-first, but modules can also be imported directly in Python.

## Common CLI Pattern

```bash
python <module_cli.py> --help
```

Typical options:

- `--model`: LLM model id (for example `ollama/gemma3`)
- `--temperature`: Sampling temperature
- Module-specific input arguments (such as `--disease`, `--drug`, or free text)

## Python Usage Pattern

Many modules expose:

1. Input/output Pydantic models
2. A generation/service class
3. A prompt-builder helper

Import paths vary by module directory under `app/MedKit/`.
