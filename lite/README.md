# Lite

A lightweight, opinionated wrapper around [LiteLLM](https://github.com/BerriAI/litellm) for robust LLM interactions, structured output, vision processing, and "LLM-as-a-judge" evaluation.

## Features

- **LiteClient**: Simplified interface for text and image-based completions.
- **Vision Support**: Robust image handling with automatic MIME type detection and path normalization.
- **Structured Output**: Direct support for Pydantic models to ensure JSON consistency.
- **Response Judge**: Built-in "LLM-as-a-judge" for evaluating model responses against ground truth.
- **MCQ Client**: Specialized client for solving multiple-choice questions.
- **LMDB Storage**: Persistent storage for session histories or cached evaluations.

## Installation

```bash
pip install -r requirements.txt
```

Or install as a package:

```bash
pip install -e .
```

## Usage

### Simple Text Completion

```python
from lite import LiteClient, ModelConfig, ModelInput

config = ModelConfig(model="gemini/gemini-2.5-flash")
client = LiteClient(model_config=config)

user_input = ModelInput(user_prompt="Explain quantum entanglement simply.")
response = client.generate_text(model_input=user_input)

print(response.markdown)
```

### Vision Processing

```python
from lite import LiteClient, ModelConfig, ModelInput

config = ModelConfig(model="gemini/gemini-2.5-flash")
client = LiteClient(model_config=config)

user_input = ModelInput(
    user_prompt="What's in this image?",
    image_path="path/to/image.jpg"
)
response = client.generate_text(model_input=user_input)
print(response.markdown)
```

### LLM-as-a-Judge

```python
from lite import ResponseJudge, ModelConfig, UserInput

judge_config = ModelConfig(model="gemini/gemini-2.5-flash")
judge = ResponseJudge(model_config=judge_config)

evaluation = judge.evaluate(UserInput(
    user_prompt="What is the capital of France?",
    model_response="The capital of France is Paris.",
    ground_truth="Paris"
))

print(f"Score: {evaluation.score}")
print(f"Reasoning: {evaluation.reasoning}")
```

## License

MIT License. See [LICENSE](LICENSE) for details.
