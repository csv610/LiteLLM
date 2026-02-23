# Medical Entity Recognizers

A modular, extensible, and professional-grade framework for identifying and analyzing medical entities using Large Language Models (LLMs). This package provides a standardized interface for recognizing various medical concepts, including medications, diseases, anatomical structures, and clinical findings.

## Overview

The Medical Entity Recognizers module is designed to provide high-fidelity identification of medical concepts from text. By leveraging a common abstraction layer, it ensures consistency in how different medical entities are processed, validated, and returned.

### Key Features

*   **DRY (Don't Repeat Yourself) Architecture**: All 19+ recognizers inherit from a common `BaseRecognizer` class, eliminating redundant boilerplate code and centralizing core logic.
*   **Standardized Interface**: Every recognizer implements a consistent `identify(name, structured=False)` method, ensuring a predictable API across the entire package.
*   **Unified CLI**: A single command-line interface (`medical_recognizer_cli.py`) to interact with all supported medical entity types.
*   **Structured Output**: Support for both descriptive Markdown and structured JSON output using Pydantic models.
*   **Dynamic Discovery**: A factory-based registry (`RecognizerFactory`) allows for lazy loading and easy instantiation of recognizers by type name.
*   **Professional Package Structure**: Built using robust relative imports, making it suitable for both standalone CLI use and as an installable library.

## Architecture

The system follows a Research-Strategy-Execution lifecycle pattern, supported by these core components:

1.  **`BaseRecognizer`**: An abstract base class that centralizes `LiteClient` initialization and common generation logic. It provides a protected `_generate()` method to handle LLM calls.
2.  **`RecognizerFactory`**: A centralized registry that manages the discovery and instantiation of recognizer implementations. It handles dynamic imports to prevent circular dependencies.
3.  **Specialized Recognizers**: Domain-specific implementations (e.g., `DrugIdentifier`, `DiseaseIdentifier`) that define only their unique prompts and data models.

## Supported Entity Types

The framework currently supports the following 19 categories:

| Category | Entities |
| :--- | :--- |
| **Pharmaceutical** | `drug`, `med_class`, `vaccine`, `supplement` |
| **Clinical** | `disease`, `condition`, `symptom`, `clinical_sign`, `imaging` |
| **Anatomical** | `anatomy`, `genetic` |
| **Operational** | `procedure`, `test`, `lab_unit`, `device`, `pathogen` |
| **Knowledge** | `specialty`, `coding` (ICD/CPT), `abbreviation` |

## Usage

### Command Line Interface

Use the `medical_recognizer_cli.py` for direct interaction.

```bash
# Basic identification (Markdown output)
python medical_recognizer_cli.py drug "Aspirin"

# Structured JSON output
python medical_recognizer_cli.py disease "Pneumonia" --structured

# Specify a different model and temperature
python medical_recognizer_cli.py anatomy "Biceps Brachii" --model ollama/gemma3 --temperature 0.1
```

### Programmatic Usage

The framework is designed to be easily integrated into Python applications.

```python
from recognizer_factory import RecognizerFactory
from lite.config import ModelConfig

# Configure the model
config = ModelConfig(model="ollama/gemma3", temperature=0.2)

# Get a recognizer from the factory (lazy-loaded)
recognizer = RecognizerFactory.get("drug", config)

# Perform identification
result = recognizer.identify("Lisinopril", structured=True)

# Access validated data
if result.data:
    print(f"Well Known: {result.data.identification.is_well_known}")
    print(f"Summary: {result.summary}")
```

## Development

### Adding a New Recognizer

To add a new entity type while maintaining the "No Boilerplate" standard:
1.  Create a directory for the entity (e.g., `my_entity/`).
2.  Define Pydantic models in `my_entity_models.py`.
3.  Define prompts in `my_entity_prompts.py`.
4.  Implement a class in `my_entity_identifier.py` that inherits from `BaseRecognizer`.
5.  Register the new class string in `RecognizerFactory._initialize_registry()`.

## Requirements

*   Python 3.10+
*   `lite` LLM library (installed in environment)
*   `pydantic`
*   `litellm`
*   Access to an LLM provider (e.g., Ollama, OpenAI, Anthropic)
