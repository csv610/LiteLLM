# Procedure Knowledge Graph Generator

This tool extracts medical procedure relationships from text and builds a structured, queryable knowledge graph using `lite_client`.

## Features
- **Structured Extraction**: Leverages LLMs (via `lite_client`) to identify subject-relation-object triples.
- **Validation**: Strict Pydantic models ensure all extracted entities and relations conform to a predefined schema.
- **Graph Management**: Uses `networkx` for powerful graph operations and relationship mapping.
- **Multi-Format Export**: Generates both JSON (for data interchange) and DOT (for Graphviz visualization).

## Data Model

### Supported Node Types
- `Procedure`, `Disease`, `Organ`, `BodySystem`, `Instrument`, `Specialist`, `Risk`, `Benefit`, `Complication`, `AnesthesiaType`, `Preparation`, `FollowUp`, `Condition`.

### Supported Relations
- `treats_disease`, `used_for_diagnosis`, `performed_on`, `requires_instrument`, `performed_by_specialist`, `has_risk`, `has_benefit`, `has_complication`, `requires_anesthesia`, `requires_preparation`, `follow_up_by`, `related_to_procedure`.

## Installation

Ensure you have the required dependencies:

```bash
pip install networkx matplotlib pydantic
```

*Note: Requires the `lite` package for LLM client functionality.*

## Usage

### 1. Generate the Graph
Run the main script to process text and generate output files:

```bash
python3 procedure_graph.py
```

### 2. View Outputs
Outputs are saved in the `outputs/` directory, named after the primary procedure identified:
- `outputs/{procedure}.json`: Structured list of all triples.
- `outputs/{procedure}.dot`: DOT file for graph visualization.

### 3. Visualization
You can visualize the DOT file using Graphviz:

```bash
dot -Tpng outputs/appendectomy.dot -o appendectomy.png
```

## Testing
Run the unit test suite to verify extraction logic and graph building:

```bash
python3 test_procedure.py
```

## Project Structure
- `procedure_graph.py`: Main execution script.
- `procedure_models.py`: Core logic including Pydantic models, extraction class, and graph builder.
- `procedure_prompts.py`: Optimized LLM prompts for relationship extraction.
- `test_procedure.py`: Comprehensive unit tests.
- `outputs/`: Generated data files.
