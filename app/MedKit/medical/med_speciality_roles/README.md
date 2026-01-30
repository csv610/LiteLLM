# MedSpecialityRoles CLI

MedSpecialityRoles CLI is a Python-based command-line interface tool designed to provide detailed information about the roles, responsibilities, and common procedures of various medical specialists. Leveraging the power of Large Language Models (LLMs) via `LiteLLM`, it generates comprehensive descriptions for any given medical speciality.

## Features

*   **Role Analysis:** Generates detailed descriptions of a medical specialist's roles.
*   **Responsibility Breakdown:** Lists key responsibilities and common procedures.
*   **Model Flexibility:** Supports various LLMs compatible with `LiteLLM`. Defaults to `ollama/gemma3` but can be configured to use others (e.g., GPT-4, Claude).
*   **Configurable Logging:** features adjustable verbosity levels for debugging and operational monitoring.

## Project Structure

The project is organized into modular components for better maintainability:

*   `med_speciality_roles_cli.py`: The main entry point for the Command Line Interface. Handles argument parsing and application flow.
*   `med_speciality_roles.py`: Contains the `MedSpecialityRoles` core logic class, responsible for interacting with the LLM and processing responses.
*   `med_speciality_roles_prompts.py`: centralized location for prompt engineering and generation logic.
*   `examples.json`: (Optional) Contains example queries or test data.
*   `logs/`: Directory where application logs (`med_speciality_roles.log`) are stored.

## Prerequisites

*   Python 3.8+
*   Access to an LLM provider (e.g., a local Ollama instance or an OpenAI API key).
*   `OPENAI_API_KEY` environment variable set (if using OpenAI models or compatible endpoints).

## Installation

1.  Navigate to the project directory:
    ```bash
    cd /path/to/MedKit/medical/med_speciality_roles
    ```

2.  Ensure dependencies are installed (assuming a parent project environment or local requirements):
    ```bash
    pip install litellm
    # Add other dependencies as required by your specific environment setup
    ```

## Usage

Run the tool from the command line using `med_speciality_roles_cli.py`.

### Basic Usage

Get roles for a specific specialist:

```bash
python med_speciality_roles_cli.py -s "Cardiologist"
```

### Specifying a Model

Use a specific model (e.g., `gpt-3.5-turbo` instead of the default `ollama/gemma3`):

```bash
python med_speciality_roles_cli.py -s "Neurologist" -m "gpt-3.5-turbo"
```

### Adjusting Verbosity

Increase logging output for debugging:

```bash
python med_speciality_roles_cli.py -s "Pediatrician" -v 4
```

### Arguments

| Argument | Short | Description | Default |
| :--- | :--- | :--- | :--- |
| `--speciality` | `-s` | **Required.** The medical speciality to query (e.g., 'Cardiologist'). | N/A |
| `--model` | `-m` | The LLM model to use for generation. | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0=CRITICAL, ..., 3=INFO, 4=DEBUG). | `2` (WARNING) |

## Logging

Logs are automatically written to `logs/med_speciality_roles.log`. The log level matches the verbosity flag provided during execution.
