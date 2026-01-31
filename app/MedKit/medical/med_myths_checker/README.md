# Medical Myths Checker

Medical Myths Checker is a tool designed to analyze medical claims and common myths for factual accuracy. It provides evidence-based assessments grounded exclusively in peer-reviewed scientific literature, clinical trials, and established medical guidelines.

## Features

- **Evidence-Based Analysis**: Every claim is verified against high-quality medical sources (WHO, NIH, CDC, peer-reviewed journals).
- **Structured Output**: Support for structured data extraction using Pydantic models (JSON format).
- **Markdown Reporting**: Generates readable Markdown reports of the analysis.
- **Customizable LLM Integration**: Uses the `LiteClient` to interface with various LLM providers (defaulting to `ollama/gemma3`).
- **Database**: Includes a starter collection of common medical myths across various categories like Mental Health, Skin Health, Cardiovascular Disease, and more.

## Project Structure

- `medical_myth_checker.py`: Core logic for myth analysis and LLM interaction.
- `medical_myth_checker_cli.py`: Command-line interface for running analysis.
- `medical_myth_checker_models.py`: Data models for structured output and type safety.
- `medical_myth_checker_prompts.py`: Optimized prompt templates for medical fact-checking.
- `assets/medical_myths.json`: A categorized database of common medical myths for testing and reference.

## Installation

### Prerequisites

- Python 3.9+
- Access to an LLM provider (e.g., Ollama, OpenAI, etc.) configured via the `lite` library.

### Setup

1. Ensure the `lite` internal library is available in your Python path.
2. Install required dependencies:
   ```bash
   pip install pydantic
   ```

## Usage

You can run the Medical Myths Checker via the CLI:

### Basic Usage
```bash
python medical_myth_checker_cli.py -i "Vitamin C prevents the common cold"
```

### Advanced Usage
```bash
# Use structured output and a specific model
python medical_myth_checker_cli.py -i "Cracking knuckles causes arthritis" -m "ollama/gemma3" -s

# Specify output directory and verbosity
python medical_myth_checker_cli.py -i "Eating carrots improves vision" -d outputs/myths -v 3
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `-i`, `--input` | **Required**: Medical myth/claim to analyze | N/A |
| `-d`, `--output-dir` | Directory for output files | `outputs` |
| `-m`, `--model` | Model to use for generation | `ollama/gemma3` |
| `-v`, `--verbosity` | Logging level (0-4) | `2` (WARNING) |
| `-s`, `--structured` | Use structured JSON output | `False` |

## Output Example

When a myth is analyzed, the tool produces a report containing:
- **Statement**: The original claim.
- **Status**: TRUE, FALSE, or UNCERTAIN.
- **Explanation**: A detailed medical explanation.
- **Peer-Reviewed Sources**: Citations from journals and medical organizations.
- **Risk Level**: LOW, MODERATE, or HIGH risk if the myth is believed.

## Example Myths to Test
You can find hundreds of examples in `assets/medical_myths.json`. Some examples include:
- "Addiction is simply a lack of willpower"
- "Sunscreen is unnecessary on cloudy days"
- "Antibiotics treat viral infections"
- "Humans use only ten percent of the brain"

---
*Note: This tool is for informational purposes and should not replace professional medical advice.*
