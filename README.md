# LiteLLM

A collection of CLI tools for interacting with language models and vision models from multiple providers (OpenAI, Ollama, Google Gemini) using the LiteLLM library.

## Features

- **LiteText**: Query language models with customizable temperature and token limits
- **LiteVision**: Analyze images using multimodal vision models
- Support for multiple providers: OpenAI, Ollama, and Google Gemini
- Command-line interfaces for both text and vision operations
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
│   ├── __init__.py
│   └── litellm_tools/
│       ├── __init__.py
│       ├── config.py            # Shared model configuration
│       ├── text.py              # LiteText module
│       └── vision.py            # LiteVision module
├── scripts/                     # CLI and web applications
│   ├── cli_litetext.py          # CLI for text queries
│   ├── cli_litevision.py        # CLI for image analysis
│   ├── streamlit_litetext.py    # Web UI for text
│   └── streamlit_litevision.py  # Web UI for vision
├── tests/                       # Unit tests
│   ├── __init__.py
│   └── test_litetext.py         # Unit tests
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

## Usage

### LiteText CLI

Query language models from the command line:

```bash
python scripts/cli_litetext.py -p "Your prompt here" -m 0
```

#### Arguments:
- `-p, --prompt`: Input prompt for the model (required)
- `-m, --model`: Index of the model to use (default: 0)
- `--list-models`: Display all available models and their indices
- `--temperature`: Sampling temperature, 0.0-1.0 (default: 0.2)
- `--max-tokens`: Maximum tokens in response (default: 1000)

#### Examples:
```bash
# List all available models
python scripts/cli_litetext.py --list-models

# Query using default model (GPT-4o)
python scripts/cli_litetext.py -p "What is AI?"

# Query using a specific model with custom parameters
python scripts/cli_litetext.py -p "Explain quantum computing" -m 5 --temperature 0.7 --max-tokens 500

# Use Ollama model
python scripts/cli_litetext.py -p "Hello" -m 2
```

### LiteText Streamlit Web UI

Run the web interface:

```bash
streamlit run scripts/streamlit_litetext.py
```

This provides an interactive web UI with:
- Model selection dropdown
- Temperature and token limit sliders
- Real-time response display
- Metrics (response time, word count)

### LiteVision CLI

Analyze images using vision models:

```bash
python scripts/cli_litevision.py -i path/to/image.jpg -p "Describe the image" -m 0
```

#### Arguments:
- `-i, --image`: Path to the image file (PNG, JPG, PDF) (required)
- `-p, --prompt`: Prompt to analyze the image (default: "Describe the image")
- `-m, --model`: Index of the model to use (default: 0)
- `--temperature`: Sampling temperature (default: 0.2)
- `--max-tokens`: Maximum tokens in response (default: 1000)

#### Examples:
```bash
# Analyze an image with default prompt
python scripts/cli_litevision.py -i photo.jpg

# Analyze with custom prompt
python scripts/cli_litevision.py -i diagram.png -p "What technology is shown here?" -m 3

# Use a specific vision model
python scripts/cli_litevision.py -i image.jpg -m 5

# List available vision models
python scripts/cli_litevision.py --list-models
```

### LiteVision Streamlit Web UI

Run the web interface:

```bash
streamlit run scripts/streamlit_litevision.py
```

This provides an interactive web UI with:
- Image upload functionality
- Model selection dropdown
- Temperature and token limit sliders
- Image preview with dimensions
- Real-time analysis results
- Metrics (response time, word count)

## Available Models

### Text Models (LiteText)
- OpenAI: `gpt-4o`, `gpt-4o-mini`
- Ollama: `llama3.2`, `phi4`
- Google Gemini: `gemini-2.0-flash`, `gemini-2.0-flash-lite-preview-02-05`, `gemini-2.0-pro-exp-02-05`, `gemini-2.0-flash-thinking-exp-01-21`

### Vision Models (LiteVision)
- OpenAI: `gpt-4o`, `gpt-4o-mini`
- Ollama: `llava`, `llava-llama3`, `bakllava`
- Google Gemini: `gemini-2.0-flash`, `gemini-2.0-flash-lite-preview-02-05`, `gemini-2.0-pro-exp-02-05`, `gemini-2.0-flash-thinking-exp-01-21`

Use `--list-models` flag to see the indexed list of available models.

## Architecture

### Core Modules

**`lite/litellm_tools/`** - Main library package

- **config.py**: Centralized model configuration
  - `ModelConfig`: Manages models from OpenAI, Ollama, and Gemini
  - Supports both text and vision models

- **text.py**: Language model interactions
  - `LiteText`: Core class for text generation
  - `LiteTextResponse`: Response data structure with metrics
  - Error handling with logging

- **vision.py**: Image analysis
  - `LiteVision`: Core class for image analysis
  - Image to base64 conversion
  - Comprehensive error handling

### CLI Scripts (`scripts/`)
- **cli_litetext.py**: Command-line interface for text queries
- **cli_litevision.py**: Command-line interface for image analysis
- **streamlit_litetext.py**: Web UI for text queries
- **streamlit_litevision.py**: Web UI for image analysis

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

Both tools include comprehensive error handling:
- Empty prompt validation
- File not found handling for images
- API error catching and reporting
- Unexpected error logging

## Performance Metrics

Both CLI tools output:
- Response time (in seconds)
- Word count of the response
- Error messages if applicable

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.
