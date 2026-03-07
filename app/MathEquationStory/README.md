# MathEquationStory

`MathEquationStory` generates narrative explanations of well-known equations. It is aimed at conceptual communication rather than symbolic derivation.

## What It Does

- Accepts the name of an equation.
- Produces a structured response with title, subtitle, main story, vocabulary notes, and discussion questions.
- Includes an equation asset library under `assets/`.

## Why It Matters

Equation summaries are often technically correct but pedagogically thin. This app is useful when the goal is to explain context and intuition to a non-specialist audience.

## What Distinguishes It

- Narrative format instead of short reference entries.
- Additional teaching material such as vocabulary notes and discussion questions.
- Local equation datasets for common examples.

## Files

- `math_equation_story_cli.py`: CLI entrypoint.
- `math_equation_story_generator.py`: generation logic.
- `math_equation_story_models.py`: response schema.
- `math_equation_story_prompts.py`: prompt construction.
- `assets/`: equation datasets.
- `test_math_equation_story_mock.py`: tests.

## Usage

```bash
python math_equation_story_cli.py "Pythagorean Theorem"
python math_equation_story_cli.py "E=mc^2" --model ollama/gemma3
```

Default model: `ollama/gemma3`

## Testing

```bash
python -m unittest test_math_equation_story_mock.py
```

## Limitations

- The output emphasizes explanation and narrative, not formal derivation.
- Historical context may be simplified.
- The generated story should not be treated as a source-cited mathematical reference.
