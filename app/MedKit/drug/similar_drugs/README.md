# Similar Drugs Finder

A powerful, AI-driven tool for identifying pharmaceutical alternatives. This module leverages Large Language Models (LLMs) to find medicines with similar active ingredients, therapeutic classes, and mechanisms of action. It provides detailed comparisons, including efficacy, side effects, and switching guidance.

## Features

*   **Comprehensive Search**: Finds top 10-15 similar medicines for any given drug.
*   **Multi-Factor Analysis**: Considers active ingredients, therapeutic class, and mechanism of action.
*   **Context-Aware**: Can adjust recommendations based on patient age and medical conditions.
*   **Detailed Comparisons**: Provides side-by-side comparison of efficacy, onset, duration, and side effects.
*   **Flexible Output**: Supports both human-readable text (Markdown) and structured data (JSON) for programmatic use.
*   **Switching Guidance**: Offers clinical advice on transitioning between medications.

## Components

The module consists of the following key files:

*   `similar_drugs_cli.py`: The command-line interface entry point.
*   `similar_drugs.py`: Core logic class (`SimilarDrugs`) that interacts with the LLM.
*   `similar_drugs_models.py`: Pydantic data models defining the structure of the input/output.
*   `similar_drugs_prompts.py`: Logic for constructing effective prompts for the LLM.

## Prerequisites

*   Python 3.8+
*   Access to a compatible LLM backend (configured via the `lite` package, default: `ollama/gemma2`).
*   Dependencies: `pydantic`, and the local `lite` library.

## Usage

### Command Line Interface (CLI)

Run the tool directly from the terminal using `similar_drugs_cli.py`.

#### Basic Search
Find similar medicines for a specific drug:

```bash
python similar_drugs_cli.py "Ibuprofen"
```

#### Advanced Search
Include patient details and specific constraints:

```bash
python similar_drugs_cli.py "Metformin" \
  --age 65 \
  --conditions "kidney disease, hypertension" \
  --output my_results.json
```

#### Options

| Flag | Description | Default |
|------|-------------|---------|
| `medicine_name` | Name of the medicine to analyze (Positional argument) | Required |
| `--include-generics` | Include generic formulations | `True` |
| `--no-generics` | Exclude generic formulations | |
| `--age`, `-a` | Patient's age in years (0-150) | `None` |
| `--conditions`, `-c` | Patient's medical conditions (comma-separated) | `None` |
| `--output`, `-o` | Custom output file path | `outputs/{name}_similar_medicines.{ext}` |
| `--json-output`, `-j` | Print JSON output to stdout | `False` |
| `--structured`, `-s` | Force structured Pydantic model output | `False` |
| `--verbosity`, `-v` | Logging level (0=CRITICAL to 4=DEBUG) | `2` (WARNING) |

### Python API

You can integrate the finder into your own Python code.

```python
from lite.config import ModelConfig
from similar_drugs import SimilarDrugs, SimilarDrugsConfig

# Configuration
config = SimilarDrugsConfig(verbosity=3)
model_config = ModelConfig(model="ollama/gemma2", temperature=0.7)

# Initialize
finder = SimilarDrugs(config, model_config)

# Find similar drugs
result = finder.find(
    medicine_name="Lisinopril",
    patient_age=50,
    patient_conditions="Diabetes",
    structured=True  # Returns a SimilarMedicinesResult object
)

# Access data (if structured=True)
print(f"Top recommendation: {result.top_recommended}")
for category in result.categorized_results:
    print(f"Category: {category.category}")
    for med in category.medicines:
        print(f" - {med.medicine_name}: {med.similarity_score}% match")
```

## Output Formats

### Structured (JSON)
When `--structured` is used, the output adheres to the schema defined in `similar_drugs_models.py`. This includes:
*   `categorized_results`: Medicines grouped by similarity type.
*   `switching_guidance`: Clinical advice for transition.
*   `clinical_notes`: Important warnings and considerations.

### Text (Markdown)
By default (or when structured is false), the tool generates a readable report describing the alternatives, suitable for direct reading or inclusion in documents.

## Logging

Logs are written to `logs/similar_drugs.log` relative to the module directory. Verbosity can be controlled via the `--verbosity` flag or `SimilarDrugsConfig`.

```