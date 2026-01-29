# MedKit - Medical Speciality Generator

A powerful Python tool designed to generate a comprehensive, structured database of medical specialties using Large Language Models (LLMs). This module is part of the **MedKit** suite and leverages the `LiteClient` for AI interaction.

## 📋 Overview

The Medical Speciality Generator creates a detailed catalog of medical specialists, organizing them by category, role, treated conditions, and more. It is designed to aid in medical education, healthcare system modeling, and data enrichment tasks where a structured understanding of medical roles is required.

## ✨ Features

- **Comprehensive Database:** Generates a wide range of medical specialties, from common fields like Cardiology to specialized areas like Interventional Radiology.
- **Structured Data:** Supports generating output as a strongly-typed Pydantic model (`MedicalSpecialistDatabase`) for reliable programmatic use.
- **Detailed Metadata:** For each specialist, it captures:
  - Official Specialty Name
  - Category & Description
  - Role Description
  - Conditions Treated
  - Common Referral Reasons
  - Subspecialties
  - Surgical Status
  - Patient Population Focus
- **Customizable:** Configurable LLM backend, output directories, and logging verbosity.

## 🚀 Usage

The tool can be run directly from the command line.

### Basic Command

```bash
python medical_speciality_cli.py
```

### Options

| Flag | Long Flag | Description | Default |
|------|-----------|-------------|---------|
| `-d` | `--output-dir` | Directory to save the generated output files. | `outputs` |
| `-m` | `--model` | The LLM model to use for generation. | `ollama/gemma3` |
| `-s` | `--structured` | Force the output to be a structured Pydantic object (JSON). | `False` |
| `-v` | `--verbosity` | Logging level (0=CRITICAL, ..., 4=DEBUG). | `2` (WARNING) |

### Example: Generating Structured Data

To generate a JSON-structured database using a specific model and save it to a custom directory:

```bash
python medical_speciality_cli.py --structured --model "ollama/gemma3" --output-dir "./data" --verbosity 3
```

## 📂 Project Structure

- **`medical_speciality_cli.py`**: The main entry point for the CLI. Handles argument parsing, logging configuration, and execution flow.
- **`medical_speciality.py`**: Contains the `MedicalSpecialityGenerator` class, which manages the interaction with the `LiteClient` to generate content.
- **`medical_speciality_models.py`**: Defines the Pydantic data models (`MedicalSpecialist`, `MedicalSpecialistDatabase`) used for structuring the AI response.
- **`medical_speciality_prompts.py`**: Contains the `PromptBuilder` class responsible for constructing the system and user prompts sent to the LLM.

## 🛠️ Dependencies

This module relies on the internal `lite` package for LLM communication. Ensure the following are available in your python environment:

- `pydantic`
- `lite` (Internal framework)

## 📄 License

[Insert License Information Here]
