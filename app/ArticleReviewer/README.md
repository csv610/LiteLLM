# ArticleReviewer

ArticleReviewer is a professional-grade automated tool designed to provide comprehensive, structured feedback on articles. Leveraging Large Language Models (LLMs) via the `LiteLLM` framework, it performs deep analysis across multiple dimensions including grammar, style, clarity, and structural integrity.

## Key Features

- **Structured Feedback**: Categorizes improvements into three actionable types:
  - **Deletions**: Identifies redundant, irrelevant, or repetitive content.
  - **Modifications**: Suggests specific rewrites for better clarity, tone, and grammatical correctness.
  - **Insertions**: Recommends adding context, transitions, or missing information for completeness.
- **Comprehensive Proofreading Rules**: Applies a rigorous set of rules covering:
  - Grammar & Syntax
  - Style & Clarity
  - Formatting & Punctuation
  - Content & Structure
  - Consistency
- **Severity Scoring**: Each suggestion is assigned a severity level (Low, Medium, High, Critical) to help prioritize revisions.
- **Quality Assessment**: Provides an overall quality score (0-100) and a summary of the article's strengths and weaknesses.
- **Flexible Output**: Generates both a formatted console report and a detailed JSON file for further processing.

## Installation

Ensure you have the necessary dependencies installed. This project requires the `lite` package (part of the LiteLLM ecosystem) and `pydantic`.

```bash
pip install pydantic
# Ensure 'lite' package is available in your python path
```

## Usage

### Command Line Interface

You can run the reviewer directly from the terminal:

```bash
python article_reviewer_cli.py "path/to/your/article.txt"
```

#### CLI Options:
- `article`: (Required) Path to the article file or direct text to review.
- `-m`, `--model`: Specify the LLM model to use (default: `ollama/gemma3`).
- `-o`, `--output`: Specify a custom output filename for the JSON review.

#### Examples:
```bash
# Review a local text file
python article_reviewer_cli.py my_article.md

# Use a specific model
python article_reviewer_cli.py "article.txt" -m "gpt-4"

# Review direct text
python article_reviewer_cli.py "This is a short article that needs review."
```

### Programmatic Usage

Integrate `ArticleReviewer` into your own Python applications:

```python
from lite.config import ModelConfig
from article_reviewer import ArticleReviewer

# Configure the model
config = ModelConfig(model="ollama/gemma3", temperature=0.3)

# Initialize the reviewer
reviewer = ArticleReviewer(model_config=config)

# Perform the review
with open("my_article.txt", "r") as f:
    text = f.read()

review = reviewer.review(text)

# Access the results
print(f"Score: {review.score}")
print(f"Summary: {review.summary}")

# Save or print the review
reviewer.save_review(review, output_filename="review_results.json")
reviewer.print_review(review)
```

## Project Structure

- `article_reviewer.py`: The core engine that orchestrates the review process.
- `article_reviewer_cli.py`: Command-line interface for the tool.
- `article_reviewer_models.py`: Pydantic data models defining the structured output.
- `article_reviewer_prompts.py`: Logic for building comprehensive, rule-based prompts.

## Configuration

The tool defaults to using `ollama/gemma3` via a local Ollama instance. You can easily switch to other providers supported by LiteLLM (e.g., OpenAI, Anthropic, Google Gemini) by passing the appropriate model string to the `ModelConfig` or CLI.

## License

[Specify License Here, e.g., MIT]
