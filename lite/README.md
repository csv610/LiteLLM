# Lite

![CI](https://github.com/csv610/lite/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/github/license/csv610/lite)

**Lite** is a powerful, user-friendly Python toolkit for interacting with Large Language Models (LLMs). Built on top of [LiteLLM](https://github.com/BerriAI/litellm), it simplifies vision processing, structured data extraction, and model evaluation.

---

## 🚀 Quick Start

### Installation

```bash
# Clone and install in editable mode
git clone https://github.com/csv610/lite.git
cd lite
pip install -e .
```

---

## 🛠 Included Apps (CLI Tools)

Lite comes with built-in command-line tools for immediate use without writing any code.

### 1. Interactive Chat (`lite-chat`)
A full-featured terminal chat interface with vision support.
```bash
# Start a simple chat
lite-chat --model gemini/gemini-2.5-flash

# Start chat with an initial image analysis
lite-chat --image_path ./photo.jpg --auto-save
```

### 2. MCQ Solver (`lite-mcq`)
Solve multiple-choice questions with context and images.
```bash
lite-mcq -q "What is the capital of Japan?" -o "Seoul" "Tokyo" "Beijing"
```

### 3. Response Judge (`lite-judge`)
Evaluate any model response for accuracy and quality.
```bash
lite-judge -r "Paris is the capital of France" -g "Paris" -p "What is the capital of France?"
```

---

## 📦 Developer API

Use Lite as a library in your own Python projects. Check out the [examples/](examples/) directory for complete runnable scripts.

### Text & Vision Completion
```python
from lite import LiteClient, ModelConfig, ModelInput

client = LiteClient(ModelConfig(model="gemini/gemini-2.5-flash"))

# Text analysis
response = client.generate_text(ModelInput(user_prompt="Hello!"))

# Vision analysis
vision_response = client.generate_text(ModelInput(
    user_prompt="Describe this image",
    image_path="scene.jpg"
))
```

### Structured Output (JSON)
Ensure your model always returns a valid object using Pydantic.
```python
from pydantic import BaseModel
from lite import LiteClient, ModelConfig, ModelInput

class UserInfo(BaseModel):
    name: str
    age: int

client = LiteClient(ModelConfig(model="gemini/gemini-2.5-flash"))
result = client.generate_text(ModelInput(
    user_prompt="Extract name and age: John is 30",
    response_format=UserInfo
))
print(result.name) # John
```

---

## 📂 Features

- **LiteClient**: Unified interface for text and image-based completions.
- **Vision Sub-package**: Advanced image handling (auto-orient, resizing, base64 encoding).
- **LLM-as-a-Judge**: Comprehensive evaluation scoring (Accuracy, Clarity, etc.).
- **MCQ Engine**: Robust solving for multi-choice scenarios.
- **Auto-Save**: Automatic markdown logging of your chat sessions.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
