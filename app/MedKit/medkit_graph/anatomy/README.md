# Anatomy Knowledge Graph Builder

This project builds a medical knowledge graph for anatomical structures using LLMs (via `lite_client`). It extracts entities and relationships (triples) from text and exports them into DOT format for visualization.

## Features
- **LLM-Powered Extraction:** Uses `LiteClient` to extract anatomical triples.
- **Structured Knowledge:** Validates and normalizes entities (Organs, Vessels, Nerves, etc.) and relations (part_of, supplied_by, common_disease, rare_disease, etc.).
- **Graph Export:** Exports the knowledge graph to `.dot` files for Graphviz visualization.
- **Visualization:** Built-in NetworkX and Matplotlib support for quick inspection.
- **Clinically Relevant:** Includes mapping for common and rare diseases associated with anatomical structures.

## Installation
Ensure you have the required dependencies:
```bash
pip install networkx matplotlib pydantic pytest lite
```

## Usage
Run the main script to process a sample text about the heart:
```bash
python anatomy_graph.py
```
This will generate `outputs/heart.dot`.

## Testing
Run the tests using `pytest`:
```bash
pytest test_anatomy.py
```

## Output
Graph files are stored in the `outputs/` directory. Each node is color-coded by its type:
- **Organ:** Cyan
- **Disease:** Yellow
- **Vessel:** Purple
- **Nerve:** Red
- **BodySystem:** Blue
- ...and more.
