# Surgical Pose Information Generator

A command-line tool that generates information about surgical patient positioning using structured language model prompting.

## Overview

The Surgical Pose Information Generator retrieves and formats detailed information about surgical positions (e.g., Supine, Prone, Lithotomy) including indications, contraindications, setup instructions, safety considerations, and potential complications.

## Important Medical Disclaimers

**This tool is for informational and educational purposes only.** It is not a substitute for professional medical training or clinical expertise. Users should:

- Consult experienced surgeons and clinical staff before positioning patients
- Verify information with institutional protocols
- Be aware that LLM-generated content may contain inaccuracies
- Always prioritize patient safety and comfort

## Installation

### Requirements

- Python 3.8+
- LiteClient and related dependencies from the parent project

## Usage

### Basic Command

Generate information for a specific surgical pose:

```bash
python surgical_pose_info_cli.py -i "lithotomy position"
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--pose` | `-i` | **Required.** Name of the surgical pose | — |
| `--output` | `-o` | Path to save output JSON file | Auto-generated |
| `--output-dir` | `-d` | Directory for output files | `outputs` |
| `--model` | `-m` | Language model to use | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0-4) | `2` |

## Features

- **Pose Documentation**: Generates detailed information covering setup, indications, and safety
- **Structured Output**: Results are returned as structured objects with standardized fields
- **JSON Export**: Save results to files for reference