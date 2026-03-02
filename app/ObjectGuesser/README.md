# Object Guesser Game

An interactive AI-powered guessing game where an LLM (Large Language Model) tries to identify an object you're thinking of by asking strategic yes/no questions.

## 🎮 Overview

In this game, the roles are reversed from the traditional 20 Questions: **the AI is the guesser, and you are the one holding the secret.** Using the `LiteLLM` client, the game connects to powerful models (like Gemma 3) to narrow down possibilities through logical deduction.

## ✨ Features

- **Strategic Deduction**: The AI uses conversation history to avoid redundant questions and narrow down categories (e.g., "Is it living?", "Is it an electronic device?").
- **Dynamic Guessing**: The system detect patterns in the AI's response to identify when it's making a formal guess versus asking a clarifying question.
- **Flexible Backend**: Powered by `LiteLLM`, allowing you to swap between local models (Ollama) or cloud APIs (OpenAI, Anthropic, etc.) with a single flag.
- **Clean Architecture**: Separated logic for game state, prompt engineering, and the command-line interface.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai/) installed and running (for default local model support)

### Installation

1. Clone the repository and navigate to the project:
   ```bash
   cd ObjectGuesser
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Start the game using the CLI:

```bash
# Using the default model (ollama/gemma3)
python object_guessing_cli.py

# Using a specific model and question limit
python object_guessing_cli.py --model ollama/llama3 --max-questions 15 --temperature 0.5
```

### Gameplay

1. Think of a physical object.
2. The AI will ask a question.
3. Respond with `yes`, `no`, or `somewhat`.
4. The game ends when the AI correctly identifies the object or runs out of questions.

## 📁 Project Structure

```text
├── object_guessing_cli.py      # Entry point & CLI argument parsing
├── object_guesser_game.py     # Game engine & guess extraction logic
├── object_guessing_prompts.py # System & User prompt templates
├── tests/                     # Unit tests for core logic
└── README.md                  # Project documentation
```

## 🧪 Testing

Ensure the game logic is functioning correctly by running the test suite:

```bash
python -m unittest discover tests
```

## 🛠️ Configuration

The `object_guessing_cli.py` supports several flags:
- `-m, --model`: The LLM model to use (default: `ollama/gemma3`).
- `--temperature`: Controls randomness (default: `0.7`).
- `--max-questions`: Maximum attempts for the AI (default: `20`).
