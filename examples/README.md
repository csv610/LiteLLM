# LiteLLM Examples

This directory contains simple examples demonstrating how to use the LiteLLM library.

## Simple Example

**File**: `simple_example.py`

A basic example showing direct usage of the litellm library with different providers.

### Usage

```bash
python examples/simple_example.py "What is AI?"
```

This example demonstrates switching between different models:
- Claude (Anthropic)
- Llama (Ollama)
- Sonar (Perplexity)
- Gemini (Google)

## More Examples

For complete CLI usage with the unified LiteClient, see:
- `scripts/liteclient_cli.py` - Full-featured CLI with text and vision support
- `scripts/streamlit_liteclient.py` - Interactive web UI

Refer to the main [README.md](../README.md) for detailed documentation.
