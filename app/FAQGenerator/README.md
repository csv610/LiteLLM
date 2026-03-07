# FAQGenerator

`FAQGenerator` produces structured question-answer pairs from either a short topic string or a local text file. It is intended for users who need reusable FAQ data rather than an ad hoc explanation.

## What It Does

- Accepts a topic or local file as input.
- Generates a configurable number of FAQs.
- Supports four difficulty levels: `simple`, `medium`, `hard`, and `research`.
- Saves the result as JSON.

## Why It Matters

FAQ generation is often used for documentation, study materials, and content seeding. A structured output format is useful when the result needs to be reviewed, filtered, or imported into another system.

## What Distinguishes It

- Can treat the same CLI argument as either topic text or a file path.
- Uses Pydantic schemas for validation.
- Includes file-size checks and filename sanitization in the generation pipeline.

## Files

- `faq_generator.py`: generation logic and export helpers.
- `faq_generator_cli.py`: command-line interface.
- `faq_generator_models.py`: schemas and constants.
- `faq_generator_prompts.py`: prompt construction.
- `mock_test_faq_generator.py`: tests.

## Installation

This app depends on the local `lite` package and its model providers. Install any required Python packages in your environment before running it.

## Usage

```bash
python faq_generator_cli.py --input "Distributed Systems" --num-faqs 10 --difficulty research
python faq_generator_cli.py --input assets/machine_learning.txt --num-faqs 5 --difficulty medium
python faq_generator_cli.py --input documentation.md --difficulty simple --output ./results
```

Defaults:

- `--num-faqs`: `5`
- `--difficulty`: `medium`
- `--model`: `ollama/gemma3`
- `--temperature`: `0.3`
- `--output`: current directory

## Testing

```bash
python -m unittest mock_test_faq_generator.py
```

## Limitations

- FAQ quality depends on the underlying model and the quality of the source text.
- The `research` difficulty label affects prompting, not independent scholarly verification.
- Generated answers should be reviewed before publication.
