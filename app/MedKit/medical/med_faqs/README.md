# Medical FAQ Generator

A CLI tool for generating comprehensive, patient-friendly FAQs for medical topics using LLM-based content generation with structured output validation.

## Overview

Medical FAQ Generator provides an easy-to-use command-line interface to automatically generate well-organized, medically accurate FAQ content for healthcare topics. The tool leverages large language models to create consistent, structured responses that are accessible to non-medical audiences while maintaining clinical accuracy.

## Features

- **Structured Output**: Generates FAQs in a consistent JSON format using Pydantic models
- **Patient-Friendly Content**: Optimized prompts ensure answers are clear and accessible to general audiences
- **Flexible Model Selection**: Support for different LLM backends (default: `ollama/gemma3`)
- **Configurable Output**: Save to custom locations or use intelligent default naming
- **Rich Console Output**: Formatted display of generated content with organized panels
- **Comprehensive Logging**: Multiple verbosity levels for debugging and monitoring
- **Schema-Aware Prompting**: Ensures structured responses match expected data models

## Installation

### Requirements

- Python 3.8+
- Dependencies (install via pip):
  ```bash
  pip install -r requirements.txt
  ```

### Setup

1. Ensure the LiteClient is properly configured and accessible
2. Configure your model endpoint (local or remote)
3. Verify model availability: `ollama/gemma3` or configure your preferred model

## Usage

### Basic Usage

Generate FAQs for a medical topic:

```bash
python medical_faq_cli.py -i diabetes
```

### Command-Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--topic` | `-i` | Medical topic to generate FAQs for (required) | — |
| `--output` | `-o` | Path to save the output JSON file | Auto-generated |
| `--output-dir` | `-d` | Directory for output files | `outputs/` |
| `--model` | `-m` | LLM model identifier | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0-4) | `2` (WARNING) |

### Verbosity Levels

- `0`: CRITICAL - Only critical errors
- `1`: ERROR - Errors only
- `2`: WARNING - Warnings and errors
- `3`: INFO - Detailed operation information
- `4`: DEBUG - Full debug output

### Examples

Generate FAQ for hypertension with verbose logging:
```bash
python medical_faq_cli.py -i hypertension -v 3
```

Generate FAQ and save to custom location:
```bash
python medical_faq_cli.py -i "heart disease" -o ./faqs/heart_disease_faq.json
```

Generate FAQ using a different model:
```bash
python medical_faq_cli.py -i asthma -m ollama/llama2
```

Generate multiple FAQs to a custom directory:
```bash
python medical_faq_cli.py -i diabetes -d ./medical_content/faqs
python medical_faq_cli.py -i hypertension -d ./medical_content/faqs
```

## Output Format

The tool generates structured FAQ data in JSON format with the following schema (defined in `medical_faq_models.py`):

```json
{
  "topic": "Medical Topic",
  "introduction": "Overview of the topic",
  "faqs": [
    {
      "question": "Question text",
      "answer": "Detailed, patient-friendly answer"
    }
  ],
  "prevention_tips": ["Tip 1", "Tip 2"],
  "when_to_see_doctor": "Guidelines for seeking medical care",
  "key_terms": {
    "term": "definition"
  }
}
```

Default output filename: `{topic_lowercase_with_underscores}_faq.json`

## Logging

Logs are written to `medical_faq.log` in the current working directory with the following information:

- CLI argument values
- Generation progress and status
- LLM API calls and results
- Save operations and file paths
- Error messages with full exception details

## Architecture

### Core Components

- **MedicalFAQGenerator**: Main class handling FAQ generation workflow
  - `generate_text()`: Initiates FAQ generation for a topic
  - `save()`: Persists FAQ data to JSON file
  - `ask_llm()`: Calls the LLM client with structured input

- **Prompt Functions**:
  - `create_system_prompt()`: Defines the LLM's role and behavior
  - `create_user_prompt()`: Generates topic-specific user prompts

- **CLI Functions**:
  - `get_user_arguments()`: Parses command-line arguments
  - `app_cli()`: Main entry point orchestrating the workflow

## Error Handling

The tool provides comprehensive error handling:

- **Empty Topic Validation**: Rejects empty or whitespace-only topics
- **File I/O Errors**: Catches and logs filesystem errors with full details
- **LLM Errors**: Propagates LLM-related exceptions with context
- **Exit Codes**: Returns 0 on success, 1 on failure

## Development

### Adding Custom Models

Modify `medical_faq_models.py` to adjust the FAQ output structure, then update `create_user_prompt()` and `create_system_prompt()` accordingly.

### Customizing Prompts

Edit the `create_system_prompt()` and `create_user_prompt()` functions to adjust content style, tone, or structure.

### Extending Functionality

The `MedicalFAQGenerator` class can be extended to support:
- Batch processing of multiple topics
- Different output formats (Markdown, HTML)
- Custom validation rules
- External data source integration

## Best Practices

1. **Use Appropriate Verbosity**: Use `-v 3` or `-v 4` during development, `-v 2` in production
2. **Organize Outputs**: Use `-d` to organize FAQs in topic-specific directories
3. **Monitor Logs**: Review `medical_faq.log` for generation quality and issues
4. **Validate Content**: Always review generated content before publishing for medical accuracy
5. **Test Models**: Verify model availability before batch generation

## Limitations & Disclaimers

- Generated content is AI-produced and should be reviewed by medical professionals
- Accuracy depends on the underlying LLM model quality
- Not suitable as a replacement for professional medical advice
- Always encourage users to consult healthcare providers

## Troubleshooting

### Model Not Found
```
Error: Model 'ollama/gemma3' not available
```
**Solution**: Verify model is running locally or update `-m` with available model

### Permission Denied (File Save)
```
Error saving FAQ to output_path: Permission denied
```
**Solution**: Check write permissions on output directory or use `-d` with writable path

### Empty or Invalid Output
**Solution**: Increase verbosity (`-v 4`) to see detailed LLM responses and debug prompts

## Dependencies

- `pathlib` (stdlib) - Path handling
- `argparse` (stdlib) - CLI argument parsing
- `json` (stdlib) - JSON serialization
- `logging` (stdlib) - Application logging
- `typing` (stdlib) - Type hints
- `rich` - Rich console output formatting
- `pydantic` - Data model validation
- `lite.lite_client` - LLM client
- `lite.config` - Model configuration
- `lite.logging_config` - Logging setup

## License

[Add your project license here]

## Contributing

Contributions are welcome. Please ensure:
- Code follows existing style conventions
- Changes maintain backward compatibility
- New features include appropriate logging
- Error messages are clear and actionable

## Support

For issues, questions, or suggestions, please refer to the project's issue tracker or contact the development team.
