# ObjectGuesser

`ObjectGuesser` is an interactive CLI game in which the model asks questions and tries to infer the object chosen by the user.

## What It Does

- Runs a question-and-answer loop in the terminal.
- Tracks conversation history.
- Attempts to detect when the model is making a guess rather than asking another question.

## Why It Matters

Within this repository, this app is primarily useful as a compact example of stateful interactive prompting.

## What Distinguishes It

- Interactive loop rather than one-shot generation.
- Simple guess extraction logic over model responses.
- Minimal project structure suitable for experimentation.

## Files

- `object_guessing_cli.py`: CLI entrypoint.
- `object_guesser_game.py`: game state and guess extraction.
- `object_guessing_prompts.py`: prompts.
- `tests/mock_test_object_guesser.py`: tests.

## Usage

```bash
python object_guessing_cli.py
python object_guessing_cli.py --model ollama/llama3 --max-questions 15 --temperature 0.5
```

Defaults:

- `--model`: `ollama/gemma3`
- `--temperature`: `0.7`
- `--max-questions`: `20`

## Testing

```bash
python -m unittest tests/mock_test_object_guesser.py
```

## Limitations

- Gameplay quality depends heavily on the model.
- Guess extraction uses simple text heuristics and can miss or misread guesses.
- There is no ranking or scoring system beyond the terminal interaction.
