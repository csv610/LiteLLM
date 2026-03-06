# Symptom Knowledge Graph Generator

This project extracts medical knowledge triples from symptom descriptions and generates a knowledge graph in DOT and JSON formats.

## Features
-   **Knowledge Extraction**: Uses `LiteClient` from the `lite` package (default model: `ollama/gemma3`) to extract (subject, relation, object) triples.
-   **Graph Generation**: Builds a directed graph using `networkx`.
-   **Export Formats**:
    -   `.dot`: Graphviz DOT format for visualization (saved in `outputs/{symptom}.dot`).
    -   `.json`: JSON representation of the triples (saved in `outputs/{symptom}.json`).
-   **Visualization**: (Optional) Visualizes the graph using `matplotlib`.

## Usage
To generate a graph for a specific symptom:
```bash
python3 sympton_graph.py "Fever"
```
The output files will be created in the `outputs/` directory.

## Testing
Run the test script to verify graph generation and DOT export:
```bash
python3 test_sympton_graph.py
```

## Requirements
-   `lite` package
-   `networkx`
-   `matplotlib` (for visualization)
-   `pydantic`
