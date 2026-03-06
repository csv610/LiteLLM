# Disease Knowledge Graph Extractor

This module extracts structured disease knowledge from text and builds a relationship graph. It uses `LiteClient` for high-performance LLM interactions and supports exporting graphs to JSON and DOT formats.

## Features

- **Structured Extraction**: Extracts triples (source, relation, target) with associated entity types.
- **Rich Schema**: Supports various relations (`has_symptom`, `caused_by`, `affects_organ`, `complication_of`, `risk_factor_for`, etc.) and node types (`Disease`, `Symptom`, `Organ`, `Treatment`, etc.).
- **Graph Building**: Constructs an in-memory graph representing the extracted knowledge.
- **Multiple Export Formats**: 
    - **JSON**: For data interchange and further processing.
    - **DOT**: For visualization using Graphviz.
- **Offline Simulation**: Includes a fallback mechanism for common diseases when LLM access is unavailable.

## File Overview

- `disease_models.py`: Core data structures (Pydantic models), `DiseaseTripletExtractor`, `DiseaseGraphBuilder`, and `GraphVisualizer`.
- `disease_prompts.py`: Optimized LLM prompts for structured extraction.
- `disease_graph.py`: Main runner script and example usage.
- `test_disease.py`: Unit tests for model validation, normalization, and graph building.

## Requirements

- Python 3.10+
- `pydantic`
- `lite` package (local LiteLLM wrapper)
- `pytest` (for running tests)

## Usage

### Running the Example
To generate a graph for a disease by name:
```bash
python3 disease_graph.py "Diabetes"
```
Or simply:
```bash
python3 disease_graph.py
```
And then enter the disease name when prompted.

This will:
1. Generate knowledge triples for the specified disease.
2. Print the extracted knowledge.
3. Export the graph to `outputs/disease_name.dot`.
4. Display a text representation of the graph.

### Running Tests
To verify the system:
```bash
pytest test_disease.py
```

## Graph Visualization
The generated `.dot` files in the `outputs/` folder can be visualized using Graphviz:
```bash
dot -Tpng outputs/malaria.dot -o malaria.png
```
