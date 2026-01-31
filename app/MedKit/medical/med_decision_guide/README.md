# Medical Decision Guide

A Python-based tool for generating and visualizing medical decision trees for symptom assessment using LLMs (Large Language Models). This project creates structured decision guides to assist in clinical decision support and triage.

## Overview

The Medical Decision Guide system leverages generative AI to synthesize clinical knowledge into structured decision trees. It allows users to input a symptom (e.g., "fever", "abdominal pain") and receive a JSON-based decision guide. This guide includes logic paths (Yes/No questions), clinical outcomes, severity assessments, and triage recommendations.

## Features

*   **Symptom-Specific Generation:** Dynamically creates decision trees tailored to specific medical complaints.
*   **Structured Output:** Uses Pydantic models to ensure strictly typed, reliable JSON output suitable for software integration.
*   **LLM Powered:** Built to work with modern LLMs (defaulting to `ollama/gemma3`) via a `LiteClient` wrapper.
*   **Visualization Tools:** Includes utilities to convert decision trees into **DOT** (Graphviz) and **Mermaid** formats for visual inspection.
*   **CLI:** Command-line interface for batch processing or single-use generation.

## Project Structure

*   **`medical_decision_guide_cli.py`**: The main entry point for the command line. Handles arguments and orchestration.
*   **`medical_decision_guide.py`**: Contains the `MedicalDecisionGuideGenerator` class, which manages the LLM interaction and file saving.
*   **`medical_decision_guide_models.py`**: Defines the data schema (Pydantic models) for `DecisionNode`, `Outcome`, and the overall `MedicalDecisionGuideModel`.
*   **`medical_decision_guide_prompts.py`**: Manages the construction of system and user prompts to guide the LLM.
*   **`visualize_decision_guide.py`**: A standalone module for converting the generated JSON files into graph formats.

## Setup & Dependencies

This module is designed to work within a larger application context (specifically the `MedKit/LiteLLM` ecosystem).

**Prerequisites:**
*   Python 3.8+
*   `pydantic`
*   Access to the internal `lite` library (expected in parent directories).

## Usage

### Command Line Interface

You can generate decision guides directly from the terminal.

**Basic Generation:**
```bash
python medical_decision_guide_cli.py -i "sore throat"
```

**Advanced Usage:**
Generate a structured JSON response for "chest pain", save it to a specific directory, and use verbose logging.

```bash
python medical_decision_guide_cli.py --symptom "chest pain" --structured --output-dir ./guides --verbosity 4
```

**CLI Arguments:**
*   `-i`, `--symptom`: **(Required)** The symptom to analyze.
*   `-s`, `--structured`: Request structured JSON output (Essential for visualization).
*   `-o`, `--output`: Specific filename for the output.
*   `-d`, `--output-dir`: Directory to save outputs (default: `outputs`).
*   `-m`, `--model`: The LLM model identifier (default: `ollama/gemma3`).
*   `-v`, `--verbosity`: Logging level (0=CRITICAL to 4=DEBUG).

### Visualization

The project includes a tool to visualize the generated JSON files.

```python
from visualize_decision_guide import visualize_guide

# Convert a JSON guide to a Mermaid diagram
mermaid_graph = visualize_guide(
    decision_guide_path="outputs/sore_throat_decision_tree.json",
    format="mermaid"
)

# Convert to DOT format
dot_graph = visualize_guide(
    decision_guide_path="outputs/sore_throat_decision_tree.json",
    format="dot"
)

print(mermaid_graph)
```

## Data Schema

The decision guides are built on the following core components:

*   **DecisionNode**: Represents a branching point with a specific question and pointers to subsequent nodes (`yes_node_id`, `no_node_id`).
*   **Outcome**: A terminal node detailing the `severity_level`, `urgency`, `recommendation`, and `possible_diagnoses`.
*   **MedicalDecisionGuideModel**: The container for the entire tree, including metadata like `age_groups_covered` and `warning_signs`.
