# LiteLLM

A unified CLI tool for interacting with language models and vision models from multiple providers (OpenAI, Ollama, Google Gemini) using the LiteLLM library.

## Features

- **Unified LiteClient**: Single interface for text generation and image analysis
- Support for multiple providers: OpenAI, Ollama, and Google Gemini
- Flexible text and vision capabilities in one command
- Customizable temperature and token limits
- Response timing and word count metrics
- Comprehensive error handling

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd LiteLLM
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API keys as environment variables:
```bash
export OPENAI_API_KEY="your-openai-key"
export GEMINI_API_KEY="your-gemini-key"
```

For Ollama models, ensure Ollama is running locally.

## Project Structure

```
LiteLLM/
├── lite/                        # Core library package
│   ├── __init__.py              # Package exports
│   ├── config.py                # Model configuration
│   ├── image_utils.py           # Image processing utilities
│   ├── logging_config.py        # Logging configuration
│   └── lite_client.py           # Unified LiteClient for text and vision operations
├── app/                         # Applications layer
│   ├── __init__.py
│   ├── cli/                     # Command-line interfaces
│   │   ├── __init__.py
│   │   └── liteclient_cli.py    # Unified CLI for text and vision
│   ├── web/                     # Web applications
│   │   ├── __init__.py
│   │   └── streamlit_liteclient.py # Unified web UI for text and vision
│   └── integrations/            # Domain-specific integrations
│       ├── drugbank/            # DrugBank medicine information
│       │   ├── __init__.py
│       │   ├── drugbank_medicine.py
│       │   └── medicine_info.py
│       └── nobel_prize_info.py  # Nobel Prize information
├── utilities/                   # Experimental utilities
│   ├── __init__.py
│   ├── perplx_chat.py          # Perplexity provider
│   ├── gemini_chat.py          # Gemini chat utilities
│   ├── google_search.py        # Google search
│   ├── url_explain.py          # URL explanation
│   └── websearch.py            # Web search
├── tests/                       # Unit tests
│   ├── __init__.py
│   ├── test_litetext.py        # Unit tests for core library
│   └── jsonout.py              # Test utilities
├── .env.example                 # Environment variables template
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── setup.py                     # Package configuration
├── Makefile                     # Build automation
├── README.md                    # This file
├── LICENSE                      # MIT License
└── .gitignore                   # Git ignore rules
```

## Usage

### Unified LiteClient CLI

Use the unified CLI for both text generation and image analysis:

```bash
python app/cli/liteclient_cli.py --question "Your prompt here"
```

Or use the Makefile:

```bash
make run-cli-text      # List available models
make run-cli-vision    # Show CLI help
```

#### Arguments:
- `-q, --question`: Input prompt for the model (required for text mode)
- `-i, --image`: Optional path to an image file for vision analysis
- `-m, --model`: Index of the model to use (default: 0)
- `-t, --temperature`: Sampling temperature, 0.0-1.0 (default: 0.2)
- `--list-models`: List available models (text or vision)

#### Text Query Examples:
```bash
# Simple text query
python app/cli/liteclient_cli.py -q "What is AI?"

# Text query with custom model and temperature
python app/cli/liteclient_cli.py -q "Explain quantum computing" -m 5 -t 0.7

# List available text models
python app/cli/liteclient_cli.py --list-models
```

#### Image Analysis Examples:
```bash
# Analyze an image with default prompt
python app/cli/liteclient_cli.py -i photo.jpg

# Analyze with custom prompt
python app/cli/liteclient_cli.py -i diagram.png -q "What technology is shown here?"

# Vision analysis with specific model
python app/cli/liteclient_cli.py -i image.jpg -m 3 -t 0.5

# List available vision models
python app/cli/liteclient_cli.py --list-models vision
```

### Streamlit Web UI

Run the unified interactive web interface:

```bash
streamlit run app/web/streamlit_liteclient.py
```

Or use the Makefile:

```bash
make run-web
```

This provides an interactive web interface with:
- Mode selection (Text Generation / Image Analysis)
- Model selection dropdown
- Temperature slider
- Real-time response display
- Image preview with dimensions (for vision mode)

## Available Models

### Text Models
- OpenAI: `gpt-4o`, `gpt-4o-mini`
- Ollama: `llama3.2`, `phi4`
- Google Gemini: `gemini-2.0-flash`, `gemini-2.0-flash-lite-preview-02-05`, `gemini-2.0-pro-exp-02-05`, `gemini-2.0-flash-thinking-exp-01-21`

### Vision Models
- OpenAI: `gpt-4o`, `gpt-4o-mini`
- Ollama: `llava`, `llava-llama3`, `bakllava`
- Google Gemini: `gemini-2.0-flash`, `gemini-2.0-flash-lite-preview-02-05`, `gemini-2.0-pro-exp-02-05`, `gemini-2.0-flash-thinking-exp-01-21`

Use `--list-models` flag with the CLI to see the indexed list of available models:
```bash
python app/cli/liteclient_cli.py --list-models        # Text models
python app/cli/liteclient_cli.py --list-models vision # Vision models
```

Or use the Makefile shortcut:
```bash
make run-cli-text  # List text models
```

## Architecture

### Core Module: LiteClient (`lite/lite_client.py`)

The unified `LiteClient` class provides a single interface for both text and vision operations:

**Key Methods:**
- `generate_text(prompt, model, image_path=None, temperature=0.2)`: Generate text or analyze images
  - Automatically detects whether to perform text generation or image analysis
  - Returns error dict for vision operations, string for text operations
- `create_message(prompt, image_path=None)`: Create formatted messages for the API
  - Handles multimodal content (text + optional image)
- `list_models(model_type="text")`: Get available models by type
- `get_model(index, model_type="text")`: Get specific model by index

**Error Handling:**
- File not found validation
- API error catching and reporting
- Unexpected error logging

### Supporting Modules (`lite/`)

- **config.py**: Model configuration and input validation
  - `ModelConfig`: Centralized configuration class for models from OpenAI, Ollama, and Gemini
    - Supports both text and vision models
    - Class methods: `get_model(index, model_type)`, `get_models(model_type)`
    - Available models: 8 text models, 7 vision models
  - `ModelInput`: Dataclass for model interaction inputs with built-in validation
    - Fields: `user_prompt` (required), `image_path` (optional), `system_prompt` (optional)
    - Validates user_prompt is not empty (unless image_path is provided)
    - Normalizes empty system_prompt to None
    - Auto-defaults to "Describe this image in detail" when user_prompt is empty with image_path

- **image_utils.py**: Image processing utilities
  - Image validation and base64 encoding
  - Support for multiple image formats (JPG, PNG, GIF, WebP)

- **logging_config.py**: Logging configuration
  - Centralized logging setup for the application

### Application Scripts (`scripts/`)
- **liteclient_cli.py**: Unified CLI for text queries and image analysis
- **streamlit_liteclient.py**: Unified web UI for text and vision operations

## Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Or run specific tests:
```bash
python -m pytest tests/test_litetext.py -v
```

## Requirements

- Python 3.8+
- litellm
- streamlit (for web interfaces)
- pytest (for testing)

See `requirements.txt` for specific versions.

## Environment Variables

Configure the following environment variables for API access:

```bash
OPENAI_API_KEY=<your-openai-api-key>
GEMINI_API_KEY=<your-gemini-api-key>
```

For Ollama, no API key is required if running locally.

## Error Handling

The LiteClient includes comprehensive error handling:
- Empty prompt validation (with intelligent defaults for image analysis)
- File not found handling for images
- API error catching and reporting
- Input validation for image files
- Unexpected error logging

## Performance Metrics

The CLI tools provide:
- Response time tracking
- Word count of responses
- Error messages when applicable
- Verbose logging option for debugging

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.
