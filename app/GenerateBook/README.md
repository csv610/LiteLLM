# GenerateBook

`GenerateBook` creates chapter plans for a subject across one or more education levels. The output is a curriculum scaffold, not a finished textbook.

## What It Does

- Accepts a subject, optional education level, and chapter count.
- Generates chapter structures for one level or for all supported levels.
- Saves the result through the generator's export path.

## Why It Matters

Curriculum planning often starts with a level-appropriate sequence of topics rather than full prose. This app is useful when the immediate goal is scope, progression, and chapter organization.

## What Distinguishes It

- Works across several education levels from a single CLI.
- Uses typed input and output models rather than raw text only.
- Produces a reusable structure that can be refined later.

## Files

- `bookchapters_cli.py`: CLI entrypoint.
- `bookchapters_generator.py`: generation and save logic.
- `bookchapters_models.py`: typed input and output models.
- `bookchapters_prompts.py`: level-specific prompting.
- `test_bookchapters_mock.py`: tests.

## Usage

```bash
python bookchapters_cli.py "Quantum Physics"
python bookchapters_cli.py "Climate Change" --level "High School" --chapters 8
python bookchapters_cli.py "AI" --level "Post-Graduate" --model "openai/gpt-4"
```

Defaults:

- all supported levels when `--level` is omitted
- `--chapters`: `12`
- `--model`: `ollama/gemma3`

## Testing

```bash
python -m unittest test_bookchapters_mock.py
```

## Limitations

- The generated curriculum reflects model judgment rather than an accredited syllabus.
- Difficulty progression and sequencing should be reviewed by a subject-matter expert.
- The tool generates chapter plans, not complete instructional content.
