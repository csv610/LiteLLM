# Herbal Information Generator

A command-line tool that generates comprehensive information about medicinal herbs using structured language model prompting.

## Overview

The Herbal Information Generator retrieves and formats information about herbs including traditional uses, active compounds, safety considerations, and relevant research. The tool uses a large language model to synthesize information based on a system prompt designed to prioritize accuracy and evidence-based content.

## Important Medical Disclaimers

**This tool is for informational purposes only.** It is not a substitute for professional medical advice, diagnosis, or treatment. Users should:

- Consult qualified healthcare providers before using any herb for medical purposes
- Verify information with peer-reviewed medical literature and authoritative sources
- Be aware that LLM-generated content may contain inaccuracies or outdated information
- Understand that herbal preparations vary in potency and composition
- Consider individual health conditions, medications, and potential drug-herb interactions
- Report any adverse effects to a healthcare provider

The information generated reflects the training data and methodology of the underlying language model and should not be considered definitive or complete.

## Installation

### Requirements

- Python 3.8+
- LiteClient and related dependencies from the parent project
- Rich library for formatted console output

### Setup

```bash
cd herbal_info
pip install -r requirements.txt
```

## Usage

### Basic Command

Generate information for a single herb:

```bash
python herbal_info_cli.py -i "ginger"
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--herb` | `-i` | **Required.** Name of the herb | — |
| `--output` | `-o` | Path to save output JSON file | Auto-generated |
| `--output-dir` | `-d` | Directory for output files | `outputs` |
| `--model` | `-m` | Language model to use | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0-4) | `2` |

### Examples

Save to a specific file:
```bash
python herbal_info_cli.py -i "echinacea" -o echinacea_info.json
```

Use a different model:
```bash
python herbal_info_cli.py -i turmeric -m "ollama/llama2"
```

Increase logging verbosity:
```bash
python herbal_info_cli.py -i "St. John's Wort" -v 4
```

## Features

- **Structured Output**: Results are returned as `HerbalInfo` objects with standardized fields
- **JSON Export**: Save results to files for further processing or archival
- **Formatted Console Output**: Results displayed in organized panels using Rich
- **Configurable Logging**: Multiple verbosity levels for debugging and production use
- **System Prompting**: Uses role-based system prompts to guide information generation

## Code Architecture

### Core Components

**`HerbalInfoGenerator`** - Main class for information generation
- Initializes with language model configuration
- Validates inputs and generates herbal information
- Handles file output

**Prompt Functions**
- `build_system_prompt()`: Defines the LLM's role and instructions
- `build_user_prompt(herb)`: Creates the specific query for a given herb

**Output**
- `save()`: Exports results to JSON files

## Output Format

The tool generates a `HerbalInfo` object with the following structure (see `herbal_info_models.py` for complete schema):

```json
{
  "metadata": {
    "common_name": "...",
    "scientific_name": "...",
    "other_names": ["..."]
  },
  "active_compounds": ["..."],
  "traditional_uses": "...",
  "modern_research": "...",
  "safety_considerations": "...",
  "drug_interactions": "..."
}
```

## Logging

Logs are written to `herbal_info.log` in the working directory.

Verbosity levels:
- `0`: CRITICAL only
- `1`: ERROR messages
- `2`: WARNING messages (default)
- `3`: INFO messages
- `4`: DEBUG messages (verbose)

## Limitations

1. **Model Dependency**: Output quality depends on the underlying language model's training data and capabilities
2. **Knowledge Cutoff**: LLM training data has a cutoff date; recent research may not be included
3. **No Medical Validation**: Generated information is not reviewed by medical professionals
4. **Incomplete Information**: Some herbs may have limited coverage in training data
5. **Dosage Uncertainty**: The tool does not provide personalized dosage recommendations
6. **Interaction Data**: Drug-herb interactions may not be comprehensive or current

## Best Practices

- Use this tool as a starting point for research, not as a final authority
- Cross-reference information with established sources (NIH, PubMed, professional herbalist references)
- Consult healthcare providers before recommending or using herbs
- Keep records of sources and generation dates for audit trails
- Update information periodically as new research emerges

## Related Files

- `herbal_info_models.py` - Pydantic models for structured data
- `herbal_info.log` - Log file (auto-generated)

## License

See parent project LICENSE file.
