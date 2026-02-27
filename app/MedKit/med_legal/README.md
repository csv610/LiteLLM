# Patient Legal Rights Information Generator

A command-line tool that generates structured information about the legal rights of patients using large language models to create detailed educational and reference materials for healthcare law and ethics.

## Overview

The Patient Legal Rights Information Generator analyzes legal topics related to patient care and produces documentation covering 11 distinct aspects including legal basis, core rights, provider responsibilities, practical implementation, exceptions, and recourse. The tool uses a large language model to generate detailed, well-structured overviews suitable for patient education, advocacy, or healthcare administration reference.

## Important Legal Disclaimers

**This tool is for informational and educational purposes only.** It is not a substitute for professional legal advice or formal legal consultation. Users should:

- Understand that this tool generates AI-generated content that may contain errors, inaccuracies, or outdated information regarding laws and regulations.
- Verify all legal information with authoritative sources, actual statutes (e.g., HIPAA, EMTALA), and qualified legal professionals.
- Not use this tool as a basis for legal decisions, filing lawsuits, or interpreting complex legal scenarios.
- Recognize that LLM-generated content may include hallucinations or misrepresentations of specific jurisdictional laws (which vary by state and country).
- Always consult with a licensed attorney for specific legal advice and representation.
- Be aware that laws evolve rapidly and AI-generated content may not reflect the latest legislative changes or court rulings.

The information generated reflects the capabilities and limitations of the underlying language model and should not be considered definitive, legally validated, or suitable for formal legal action without expert review.

## Installation

### Requirements

- Python 3.8+
- LiteClient and related dependencies from the parent project

### Setup

```bash
cd med_legal
pip install -r requirements.txt
```

## Usage

### Basic Command

Generate patient legal rights information (defaults to India):

```bash
python medical_topic_cli.py "Informed Consent"
```

Specify a country:

```bash
python medical_topic_cli.py "Informed Consent" -c "USA"
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `topic` | — | **Required.** The name of the legal right topic or file path containing topics | — |
| `--country` | `-c` | The country/jurisdiction for the legal rights (e.g., 'USA', 'UK', 'India') | `India` |
| `--user-name` | `-u` | Name of the user for the output filename | `anonymous` |
| `--output-dir` | `-d` | Directory for output files | `outputs` |
| `--model` | `-m` | Language model to use | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0-4): 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG | 2 |
| `--structured` | `-s` | Use structured output (returns JSON based on Pydantic model) | False |

### Examples

Generate information for India (default) with a user name:
```bash
python medical_topic_cli.py "Right to Refuse Treatment" -u "jdoe"
```

The output will be saved as `jdoe_complain_feb272026.md`.

Generate information for the USA:
```bash
python medical_topic_cli.py "HIPAA Privacy Rule" -c "USA"
```

Generate information for the UK:
```bash
python medical_topic_cli.py "Access to Medical Records" -c "UK"
```

Use custom output directory with verbose logging:
```bash
python medical_topic_cli.py "Informed Consent" -c "Australia" -d outputs/legal -v 3
```

Generate multiple topics from a file for a specific country:
```bash
python medical_topic_cli.py assets/topics_list.txt -c "Canada" -s
```

## Features

- **Detailed Coverage**: Generates 11 distinct aspects of patient legal rights information.
- **Structured Output**: Returns `LegalRightsModel` objects with standardized Pydantic schema when using `-s`.
- **System Prompting**: Uses specialized prompts for healthcare law and patient advocacy expertise.
- **Markdown and JSON Support**: Saves results in human-readable Markdown and machine-readable JSON.
- **Configurable Models**: Supports multiple LLM backends via LiteClient.

## Code Architecture

### Core Components

**`LegalRightsGenerator`** - Main class for legal rights information generation.
- Initializes with language model configuration.
- Generates comprehensive legal documentation based on `PromptBuilder`.
- Handles result display and file output.

**`PromptBuilder`** (`medical_topic_prompts.py`)
- `create_system_prompt()`: Defines the LLM's role as a legal expert in healthcare.
- `create_user_prompt(topic)`: Creates structured queries for the specified legal topic.

**`LegalRightsModel`** (`medical_topic_models.py`)
- Pydantic models for structured representation of legal information.

**CLI Entry Point** (`medical_topic_cli.py`)
- Handles argument parsing and orchestrates the generation workflow.

## Output Format

The tool generates information covering the following sections:

1. **Definition and Legal Scope**: Core understanding and extent of the right.
2. **Historical and Regulatory Context**: Evolution and key governing laws.
3. **Core Patient Rights**: Specific rights guaranteed to patients.
4. **Healthcare Provider Responsibilities**: Obligations and compliance requirements.
5. **Practical Implementation**: How patients can exercise these rights.
6. **Exceptions and Legal Limitations**: Situations where the right may not apply.
7. **Dispute Resolution and Recourse**: Mechanisms for resolving conflicts and legal remedies.
8. **Key Legal Terminology**: Glossary of essential terms.
9. **Related Legal Concepts**: Overlapping legal or ethical topics.
10. **Current Legal Trends and Future Perspectives**: Emerging issues and future outlook.

## License

See parent project LICENSE file.
