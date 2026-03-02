# Socrates AI Tutor

A Python-based AI tutor that helps you find the truth through dialogue using the Socratic Method. It leverages questioning to help you reach deep intuitive breakthroughs.

## Features

- **Socratic Inquiry:** Guided dialogue to help you discover truths through reason.
- **Core Engine:** `SocratesTutor` class handles the inquiry logic and state.
- **CLI Interface:** Interactive command-line interface for the inquiry loop.
- **LiteClient Integration:** Compatible with multiple LLMs via `LiteClient` (defaults to `ollama/gemma3`).

## Project Structure

- `socrates_tutor_cli.py`: The entry point for the interactive CLI application.
- `socrates_tutor.py`: Contains the `SocratesTutor` class that manages the inquiry.
- `socrates_tutor_prompts.py`: Contains the `PromptBuilder` class that stores all system and inquiry prompts.
- `tests/`: Directory containing unit tests.

## Setup

1. **Install Dependencies:**
   Ensure the `lite` package is installed.

2. **Configure Model:**
   The default model is set to `ollama/gemma3`. Ensure you have Ollama running or change the `MODEL` variable in `socrates_tutor.py` to your preferred provider.

## Usage

Run the CLI application:
```bash
python socrates_tutor_cli.py
```

Follow the dialogue:
1. **Begin Inquiry**: State the concept or problem you want to explore.
2. **Respond**: Answer the questions posed by Socrates to refine your understanding.
3. **Conclusion**: Reach a clear understanding through guided reason.

## Development

### Running Tests
```bash
python -m unittest discover tests
```
