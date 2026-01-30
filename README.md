# LiteLLM

A unified CLI tool and library for interacting with language models and vision models from multiple providers (OpenAI, Ollama, Google Gemini, Anthropic, etc.) using the LiteLLM library.

## Features

- **Unified LiteClient**: Single interface for text generation and image analysis across all supported providers.
- **MedKit**: A comprehensive medical and healthcare information toolkit with modules for drugs, diagnostics, physical exams, and mental health.
- **Specialized CLI Tools**: Dozens of purpose-built tools for article reviewing, FAQ generation, book chapter creation, and more.
- **Support for Multiple Providers**: Seamless integration with OpenAI, Ollama, Google Gemini, and others.
- **Flexible Interactions**: Support for single and multi-image vision analysis.
- **Structured Data**: Built-in support for Pydantic models to ensure type-safe and validated model responses.
- **Streamlit Web UI**: Interactive web interface for both text and vision operations.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd LiteLLM
```

2. Create and activate a virtual environment (recommended):

**Using uv (fastest):**
```bash
uv venv
source .venv/bin/activate
```

**Using standard venv:**
```bash
make venv
source litenv/bin/activate
```

3. Install dependencies:

**Using uv:**
```bash
uv pip install -r requirements.txt
uv pip install -e .
```

**Using make/pip:**
```bash
make install
```

4. Set up your API keys in a `.env` file or as environment variables:
```bash
export OPENAI_API_KEY="your-openai-key"
export GEMINI_API_KEY="your-gemini-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

For Ollama models, ensure Ollama is running locally.

## Project Structure

```
LiteLLM/
├── lite/                        # Core library package
│   ├── config.py                # Model configuration & input validation
│   ├── lite_client.py           # Unified client for text/vision operations
│   ├── image_utils.py           # Image processing and encoding
│   └── logging_config.py        # Centralized logging
├── app/                         # Applications layer
│   ├── cli/                     # Specialized command-line interfaces
│   │   ├── liteclient_cli.py    # Main unified CLI
│   │   ├── article_reviewer.py  # AI-powered article review
│   │   ├── faq_generator.py     # FAQ generation tool
│   │   ├── feymann_tutor.py     # Feynman technique tutor
│   │   └── ... (many other specialized tools)
│   ├── MedKit/                  # Comprehensive Medical Toolkit
│   │   ├── drug/                # Drug information and interactions
│   │   ├── medical/             # Disease info, anatomy, procedures
│   │   ├── phyexams/            # 26+ Physical examination modules
│   │   ├── mental_health/       # Mental health assessment & reporting
│   │   └── diagnostics/         # Medical devices and tests
│   └── web/                     # Web applications
│       └── streamlit_liteclient.py # Interactive web UI
├── utilities/                   # Search and experimental utilities
├── tests/                       # Comprehensive test suite
├── Makefile                     # Automation for setup, testing, and execution
└── requirements.txt             # Project dependencies
```

## Usage

### Unified CLI

The main CLI tool handles both text queries and vision analysis:

```bash
# Text query
python app/cli/liteclient_cli.py -q "Explain the benefits of modular software design"

# Vision analysis
python app/cli/liteclient_cli.py -i path/to/image.jpg -q "What is shown in this image?"

# Custom model and temperature
python app/cli/liteclient_cli.py -q "Write a poem about AI" -m "gpt-4" -t 0.8
```

#### Arguments:
- `-q, --question`: Input prompt (required for text mode, optional for vision).
- `-i, --image`: Path or URL to an image file (enables vision mode).
- `-m, --model`: Model identifier (e.g., `ollama/gemma3`, `gpt-4o`, `gemini/gemini-2.0-flash`).
- `-t, --temperature`: Sampling temperature (0.0 to 2.0).
- `-o, --output`: Optional file path to save the response.

### MedKit

MedKit provides specialized medical information tools. Most submodules have their own CLI:

```bash
# Get disease information
python app/MedKit/medical/disease_info/disease_info_cli.py --disease "Diabetes"

# Check drug information
python app/MedKit/drug/medicine/medicine_cli.py -i "Aspirin"

# Run a physical exam module
python app/MedKit/phyexams/exam_depression_screening.py
```

See [app/MedKit/README.md](app/MedKit/README.md) for more details.

### Streamlit Web UI

Launch the interactive web interface:

```bash
make run-web
```

## Architecture

### LiteClient (`lite/lite_client.py`)
The core `LiteClient` provides a unified interface for all model interactions. It abstracts the complexities of different providers and handles message formatting for both text and multimodal (vision) inputs.

### Structured Output
The library leverages Pydantic for structured data extraction. By passing a Pydantic model to `generate_text`, you can ensure the LLM response is validated and parsed into a Python object.

## Testing

Run the full test suite using the Makefile:
```bash
make test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.