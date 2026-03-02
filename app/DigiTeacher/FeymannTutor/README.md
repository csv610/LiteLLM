# Feynman Style AI Tutor

A Python-based AI tutor that helps you learn complex topics using the Feynman Technique. It leverages Richard Feynman’s approach of breaking down ideas into simple, intuitive truths through analogy, questioning, and iterative refinement.

## Features

- **Prompt Management:** Centralized `PromptBuilder` class for easy prompt maintenance.
- **Core Engine:** `FeynmanTutor` class handles the conversation logic and state.
- **CLI Interface:** Interactive command-line interface for the learning loop.
- **LiteLLM Integration:** Compatible with multiple LLMs (defaults to `ollama/gemma3`).

## Project Structure

- `cli.py`: The entry point for the interactive CLI application.
- `feymann_tutor.py`: Contains the `FeynmanTutor` class that manages the learning logic.
- `prompt_builder.py`: Contains the `PromptBuilder` class that stores all system and user prompts.
- `tests/`: Directory containing unit tests.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install litellm
   ```

2. **Configure Model:**
   The default model is set to `ollama/gemma3`. Ensure you have Ollama running or change the `MODEL` variable in `feymann_tutor.py` to your preferred provider (e.g., `gpt-4`, `claude-3-opus`).

## Usage

Run the CLI application:
```bash
python cli.py
```

Follow the prompts to:
1. Enter a topic you want to learn.
2. State your current understanding level.
3. Review the initial explanation and analogies.
4. Provide feedback on what's unclear.
5. Take the "Understanding Challenge."
6. Receive your final "Teaching Snapshot."

## Development

### Running Tests
```bash
python -m unittest discover tests
```
