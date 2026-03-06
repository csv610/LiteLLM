# Medicine Knowledge Graph

This project implements an automated pipeline for building a medical knowledge graph. It uses Large Language Models (LLMs) to extract entities and relationships (triples) from unstructured medical text and represents them in a structured graph format.

## Features

- **LLM-Powered Extraction:** Uses `LiteClient` (via the `lite` package) to extract structured biomedical triples.
- **Default Model:** Optimized for `ollama/gemma3`.
- **Rich Schema:** Supports various node types and relationship types:
  - **Node Types:** `Drug`, `Disease`, `Symptom`, `SideEffect`, `DrugClass`, `Condition`, `BodySystem`, etc.
  - **Relations:** `treats`, `has_side_effect`, `belongs_to_class`, `interacts_with`, `contraindicated_in`, etc.
- **Normalization:** Automatically maps common aliases to standardized types and relations.
- **Multiple Exports:**
  - **DOT Format:** Generates `.dot` files in the `outputs/` directory for visualization with Graphviz.
  - **JSON Format:** Exports the complete triple list for programmatic use.

## Project Structure

- `medicine_graph.py`: The main entry point for running the extraction and graph building pipeline.
- `medicine_models.py`: Contains the core Pydantic models for triples and the `MedicineGraphBuilder` / `MedicineTripletExtractor` classes.
- `medicine_prompts.py`: Defines the system prompts used by the LLM for entity and relationship extraction.
- `test_medicine.py`: Unit tests for validating the models, extraction logic, and graph building.
- `outputs/`: Directory where generated graph files (`.dot`, `.json`) are stored.

## Installation

Ensure you have the required dependencies installed:

```bash
pip install networkx matplotlib pydantic
# The 'lite' package must also be available in your environment for LLM extraction.
```

## Usage

Run the main script to process a sample text and generate the graph:

```bash
python3 medicine_graph.py
```

By default, this will:
1. Extract triples from a sample description of Paracetamol.
2. Build a directed multi-graph.
3. Save the results to:
   - `outputs/Paracetamol.dot`
   - `outputs/medicine_graph.json`

## Testing

To run the automated unit tests and ensure everything is working correctly:

```bash
python3 -m unittest test_medicine.py
```

The tests cover:
- Pydantic model validation and normalization.
- Extraction simulation logic.
- Graph construction and querying.
- JSON and DOT export functionality.

## Configuration

You can customize the model and behavior in `medicine_models.py`:
- **Model Name:** The default is set to `ollama/gemma3`.
- **Extraction Schema:** Relationship types and node types are defined in `medicine_models.py`.

## Visualization

To convert the generated `.dot` file into an image (requires Graphviz):

```bash
dot -Tpng outputs/Paracetamol.dot -o outputs/Paracetamol.png
```
