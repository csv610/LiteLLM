# Hadamard Discovery AI Tutor

A Python-based AI tutor that guides you through the process of mathematical and conceptual discovery using Jacques Hadamard’s technique. It leverages Hadamard’s approach of Preparation, Incubation, Illumination, and Verification to help you reach deep intuitive breakthroughs.

## Features

- **Hadamard Prompting:** Guided stages based on "The Psychology of Invention in the Mathematical Field."
- **Core Engine:** `HadamardTutorQuestionGenerator` class handles the discovery logic and state.
- **CLI Interface:** Interactive command-line interface for the discovery loop.
- **LiteClient Integration:** Compatible with multiple LLMs via `LiteClient` (defaults to `ollama/gemma3`).

## Project Structure

- `hadamard_tutor_cli.py`: The entry point for the interactive CLI application.
- `hadamard_tutor.py`: Contains the `HadamardTutorQuestionGenerator` class that manages the discovery stages.
- `prompt_builder.py`: Contains the `PromptBuilder` class that stores all system and stage prompts.
- `tests/`: Directory containing unit tests.

## Setup

1. **Install Dependencies:**
   Ensure the `lite` package is installed.

2. **Configure Model:**
   The default model is set to `ollama/gemma3`. Ensure you have Ollama running or change the `MODEL` variable in `hadamard_tutor.py` to your preferred provider.

## Usage

Run the CLI application:
```bash
python hadamard_tutor_cli.py
```

Follow the stages:
1. **Preparation**: Explore fundamentals and identify core struggles.
2. **Incubation**: Abstract away from jargon into mental imagery.
3. **Illumination**: Receive a conceptual spark and find your "Aha!" moment.
4. **Verification**: Formalize and test your new insight.

## Development

### Running Tests
```bash
python -m unittest discover tests
```
