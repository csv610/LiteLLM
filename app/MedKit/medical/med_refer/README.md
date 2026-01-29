# MedRefer CLI

MedRefer CLI is a Python-based command-line interface tool designed to assist in identifying appropriate medical specialists based on reported symptoms or medical questions. Leveraging the power of Large Language Models (LLMs) via `LiteLLM`, it analyzes user input and provides a list of recommended specialists, filtering results against a verified list of medical disciplines.

## ⚠️ Disclaimer

**This tool is for informational and educational purposes only.** It is **not** a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## Features

*   **Symptom Analysis:** Analyzes natural language queries describing symptoms or medical conditions.
*   **Specialist Recommendation:** Suggests relevant medical specialists (e.g., Cardiologist, Neurologist) based on the analysis.
*   **Validation:** Filters AI-generated recommendations against a strict whitelist of recognized medical specialties to ensure relevance.
*   **Model Flexibility:** Supports various LLMs compatible with `LiteLLM`. Defaults to `ollama/gemma3` but can be configured to use others (e.g., GPT-4, Claude).
*   **Configurable Logging:** features adjustable verbosity levels for debugging and operational monitoring.

## Project Structure

The project is organized into modular components for better maintainability:

*   `medrefer_cli.py`: The main entry point for the Command Line Interface. Handles argument parsing and application flow.
*   `med_referral.py`: Contains the `MedReferral` core logic class, responsible for interacting with the LLM and processing responses.
*   `prompts.py`: centralized location for prompt engineering and generation logic.
*   `examples.json`: (Optional) Contains example queries or test data.
*   `logs/`: Directory where application logs (`med_refer.log`) are stored.

## Prerequisites

*   Python 3.8+
*   Access to an LLM provider (e.g., a local Ollama instance or an OpenAI API key).
*   `OPENAI_API_KEY` environment variable set (if using OpenAI models or compatible endpoints).

## Installation

1.  Navigate to the project directory:
    ```bash
    cd /path/to/MedKit/medical/med_refer
    ```

2.  Ensure dependencies are installed (assuming a parent project environment or local requirements):
    ```bash
    pip install litellm
    # Add other dependencies as required by your specific environment setup
    ```

## Usage

Run the tool from the command line using `medrefer_cli.py`.

### Basic Usage

Ask a medical question to get a specialist recommendation:

```bash
python medrefer_cli.py -q "I have a severe headache and blurry vision."
```

### Specifying a Model

Use a specific model (e.g., `gpt-3.5-turbo` instead of the default `ollama/gemma3`):

```bash
python medrefer_cli.py -q "Joint pain in my knees" -m "gpt-3.5-turbo"
```

### Adjusting Verbosity

Increase logging output for debugging:

```bash
python medrefer_cli.py -q "Stomach pain after eating" -v 4
```

### Arguments

| Argument | Short | Description | Default |
| :--- | :--- | :--- | :--- |
| `--question` | `-q` | **Required.** The medical question or symptoms to analyze. | N/A |
| `--model` | `-m` | The LLM model to use for generation. | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0=CRITICAL, ..., 3=INFO, 4=DEBUG). | `2` (WARNING) |

## Logging

Logs are automatically written to `logs/med_refer.log`. The log level matches the verbosity flag provided during execution.
