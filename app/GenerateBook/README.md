# GenerateBook: Educational Curriculum Generator

GenerateBook is a professional CLI tool designed to architect comprehensive, developmentally appropriate educational curricula using Large Language Models (LLMs). It scaffolds learning across six distinct education levels, from Middle School to Professional and General Public audiences.

## Core Features

- **Multi-Level Scaffolding**: Automatically generates tailored curricula for:
  - Middle School (Ages 11-14)
  - High School (Ages 14-18)
  - Undergraduate (Ages 18-22)
  - Post-Graduate (Ages 22+)
  - Professional (Working Adults)
  - General Public (All Ages)
- **Pedagogical Depth**: Each generated chapter includes:
  - Learning objectives (measurable & action-oriented)
  - Key concepts with definitions
  - Hands-on observations and phenomena
  - Practical experiments and demonstrations
  - Real-world projects
- **Structured Output**: Responses are validated via Pydantic models and saved as organized JSON files for easy integration into other systems.
- **Extensible LLM Support**: Built on the `lite` framework, supporting various providers (Ollama, OpenAI, Anthropic, etc.).

## Project Structure

```text
/GenerateBook
├── bookchapters_cli.py        # CLI Entry point & logging setup
├── bookchapters_generator.py  # Generation logic & file management
├── bookchapters_models.py     # Pydantic data structures (Input/Output)
├── bookchapters_prompts.py    # Pedagogical prompt construction
└── logs/                      # Application execution logs
```

## Installation

Ensure you have the `lite` framework available in your Python environment and the necessary LLM provider (e.g., Ollama) configured.

```bash
# Clone the repository
git clone <repository-url>
cd GenerateBook

# Ensure dependencies are met
pip install pydantic
```

## Usage

Run the tool using `bookchapters_cli.py`. By default, it generates chapters for all 6 education levels.

### Basic Examples

```bash
# Generate a full curriculum for a subject (all levels)
python bookchapters_cli.py 'Quantum Physics'

# Generate for a specific level with a custom number of chapters
python bookchapters_cli.py 'Climate Change' --level 'High School' --chapters 8

# Specify a different LLM model
python bookchapters_cli.py 'AI' --model 'openai/gpt-4'
```

### Command Line Arguments

| Argument | Short | Description | Default |
| :--- | :--- | :--- | :--- |
| `subject` | - | The topic to create a curriculum for | (Required) |
| `--level` | `-l` | Education level (0-5 or name) | All Levels |
| `--chapters`| `-n` | Number of chapters to generate per level | 12 |
| `--model` | `-m` | LLM model to use | `ollama/gemma3` |

## Output Format

The tool generates JSON files using the following naming convention:
`{subject}_{level_code}.json`

Each file contains a `BookChaptersModel` object with detailed pedagogical metadata for every chapter.

## License

Internal Use / Proprietary
