# Mathematical Equation Story Generator

A sophisticated tool designed to transform complex mathematical equations into engaging, narrative-driven explanations. Leveraging the power of Large Language Models (LLMs) and structured prompting, this project generates "science journalism" style articles that make mathematics intuitive, accessible, and memorable for general audiences.

## Overview

The **Mathematical Equation Story Generator** moves beyond dry textbook definitions to create flowing narratives similar to those found in publications like *Scientific American*, *Cosmos*, or *The Atlantic*. It focuses on the historical context, human intuition, and real-world implications of equations, ensuring that readers understand not just the *how*, but the *why* and the *who* behind the math.

## Key Features

- **Narrative-Driven Explanations**: Generates substantial essays (700-1200 words) with natural transitions and professional prose.
- **Structured Output**: Uses Pydantic models to ensure consistent delivery of titles, subtitles, stories, technical vocabulary, and discussion questions.
- **Multi-Model Support**: Built on a flexible `LiteClient` architecture, supporting models from Google (Gemini), OpenAI (GPT), and local providers via Ollama.
- **Rich Asset Library**: Includes a curated collection of over 40 famous equations across 9 categories (Algebra, Physics, Calculus, etc.) with LaTeX support.
- **Educational Support**: Automatically generates vocabulary notes and thought-provoking discussion questions suitable for high school students.

## Project Structure

```text
MathEquationStory/
├── math_equation_story_cli.py       # Main Command-Line Interface
├── math_equation_story_generator.py # Core generation logic and LLM client
├── math_equation_story_models.py    # Pydantic data models for structured response
├── math_equation_story_prompts.py   # Advanced prompt engineering logic
└── assets/                          # Supporting data and equation libraries
    ├── well_known_equations.py      # Curated equation datasets
    └── wikipedia_equations.py       # Extended equation references
```

## Getting Started

### Prerequisites

- Python 3.10+
- Dependencies: `pydantic`, `litellm` (or the internal `lite` package provided in the workspace)

### Installation

1. Clone the repository.
2. Install the required packages:
   ```bash
   pip install pydantic
   ```
   *(Note: Ensure the `lite` package from the parent directory is in your PYTHONPATH if running outside the provided environment.)*

## Usage

### Command Line Interface

The simplest way to generate a story is via the CLI:

```bash
# Generate a story for a specific equation using the default model
python math_equation_story_cli.py "Pythagorean Theorem"

# Specify a different model (e.g., Gemini or Claude)
python math_equation_story_cli.py "E=mc²" --model gemini-2.5-flash
```

### Programmatic Usage

You can also integrate the generator into your own Python scripts:

```python
from math_equation_story_generator import MathEquationStoryGenerator

# Initialize the generator
generator = MathEquationStoryGenerator(model_name="ollama/gemma3")

# Generate a structured story
story_data = generator.generate_text("Euler's Identity")

# Access components
print(story_data.title)
print(story_data.story)
```

## Data Assets

The project includes a robust library of equations in `assets/well_known_equations.py`. This library provides:
- **Categories**: Algebra, Geometry, Calculus, Physics, Statistics, and more.
- **Metadata**: LaTeX formulas, brief descriptions, and difficulty levels (Beginner, Intermediate, Advanced).

## Technical Implementation

- **Prompt Engineering**: The `PromptBuilder` uses a "Persona-based" approach, instructing the AI to act as a professional science writer. It emphasizes narrative momentum and conceptual clarity.
- **Data Integrity**: By utilizing Pydantic's `response_format` (via `LiteClient`), the system guarantees that the AI response perfectly maps to the `MathematicalEquationStory` model, preventing parsing errors.
- **Flexibility**: The system is designed to be model-agnostic, allowing easy switching between different LLM providers depending on the desired quality or cost.

## License

This project is intended for educational and research purposes.
