# MathEquationStory Assets

This directory contains equation datasets used by `MathEquationStory`.

## Purpose

- Provide named equations and related metadata for the story generator.
- Support categorization and filtering by mathematical area or difficulty.

## Files

- `well_known_equations.py`: curated equation collection used by the generator.
- `wikipedia_equations.py`: additional equation references.

## Data Shape

The assets are intended to provide fields such as:

- equation name
- LaTeX representation
- category
- short description
- difficulty label

## Why It Matters

Keeping equation metadata in a separate asset layer makes the generator easier to extend and test.

## Limitations

- The collection is curated rather than exhaustive.
- Difficulty labels are approximate and depend on educational context.
- Metadata should be reviewed before reuse in formal educational material.
