# Quadrails: Advanced Multi-Modal Content Moderation System

**Quadrails** is a production-grade content moderation and safety guardrail system designed to protect LLM applications from harmful inputs. It leverages Large Language Models (LLMs) via the `LiteClient` to provide structured, high-confidence safety assessments across 15+ industry-standard hazard categories for both **text and images**.

## 🚀 Key Features

- **Multi-Modal Safety**: Unified API for **Text** and **Image** analysis with vision-aware processing.
- **Granular Vision Taxonomy**: Specialized detection for **Nudity** and **Violence** in imagery, moving beyond basic NSFW flags.
- **Asynchronous & High-Performance**: Native `asyncio` support with non-blocking executors for production-grade throughput.
- **Security-First Design**: Automated pre-processing including control-character stripping, null-byte removal, and length-limit enforcement.
- **Intelligent Caching**: Hash-based in-memory result caching to optimize latency and reduce redundant inference costs.
- **Deterministic Validation**: Built with **Pydantic** to ensure LLM outputs strictly adhere to a type-safe schema.
- **MLCommons Aligned**: Comprehensive coverage of industry-standard safety domains.
- **Robust Error Handling**: Domain-specific exception hierarchy (`PreprocessingError`, `AnalysisError`) for granular fault management.

## 🛡️ Safety Categories (MLCommons Aligned)

Quadrails provides deep analysis for 15+ critical safety domains:

### 📸 Vision Categories
- **Nudity**: Explicit sexual content, exposed intimate body parts, or sexually suggestive imagery.
- **Violence**: Images depicting extreme physical harm, blood, gore, or weapons usage.

### ✍️ Text Categories
- **Hate Speech & Harassment**: Discrimination or bullying based on protected characteristics.
- **Illegal Activities**: Promotion or instructions for criminal acts or weapons (CBRNE).
- **Self-Harm**: Encouraging or providing methods for self-injury.
- **PII Detection**: Unauthorized disclosure of sensitive personal data (SSNs, Credit Cards).
- **Jailbreak Detection**: Protection against prompt injection and safety bypass attempts.
- **IP & Defamation**: Identification of copyright infringement and reputational harm.
- **High-Risk Advice**: Specialized guidance in Medical, Legal, or Financial domains.
- **Elections Integrity**: Misinformation regarding civic processes.

## 📂 Project Structure

- `guardrail.py`: Core logic featuring the `GuardrailAnalyzer` with async and caching support.
- `guardrail_models.py`: Pydantic schemas and custom exception hierarchy.
- `guardrail_prompts.py`: Optimized prompt engineering for both text and vision tasks.
- `guardrail_cli.py`: Unified CLI for batch processing and testing.
- `test_guardrail.py`: Automated test suite covering all safety categories.

## 🛠️ Installation

```bash
# Install package dependencies
pip install pydantic tqdm
# Ensure 'lite' package is in your PYTHONPATH
```

## 💻 Usage

### Environment Configuration
```bash
# Optional: Set default model via env
export GUARDRAIL_MODEL="ollama/gemma3"
```

### Analyze via CLI
```bash
# Text analysis example
python guardrail_cli.py --text "Check this text for safety"

# Image analysis example (Nudity/Violence)
python guardrail_cli.py --image ./path/to/image.jpg
```

### Programmatic Async Usage
```python
import asyncio
from guardrail import GuardrailAnalyzer
from lite.config import ModelConfig

async def main():
    # Initialize with optional custom config
    analyzer = GuardrailAnalyzer(ModelConfig(model="ollama/gemma3"))
    
    # 1. Text Analysis
    try:
        text_res = await analyzer.analyze_text("Hello world")
        print(f"Text Safe: {text_res.is_safe}")
        
        # 2. Image Analysis (Vision)
        img_res = await analyzer.analyze_image("./sample.jpg")
        print(f"Image Safe: {img_res.is_safe}")
        
    except Exception as e:
        print(f"Analysis Failed: {e}")

asyncio.run(main())
```

## 🧪 Testing

The project includes 14+ automated tests covering the full hazard taxonomy and caching logic:

```bash
pytest test_guardrail.py test_guardrail_cli.py
```

## 📄 License

This project is licensed under the MIT License.
