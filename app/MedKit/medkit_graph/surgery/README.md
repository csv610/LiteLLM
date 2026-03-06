# Surgery Knowledge Graph Generator

This tool extracts surgical knowledge (triplets) from unstructured text and generates a knowledge graph in `.dot` (Graphviz) format.

## Features

- **LiteClient Integration**: Uses the `lite` package's `LiteClient` for high-quality structured extraction.
- **Pydantic Validation**: Ensures extracted triples follow a strict schema and normalizes relations.
- **Graphviz Output**: Generates `.dot` files in an `outputs/` directory, named after the surgery (e.g., `coronary_artery_bypass_surgery.dot`).
- **Offline Mode**: Includes a simulation mode for testing when `LiteClient` is not available.

## Usage

1.  **Configure environment**:
    Ensure `LiteLLM` is in your `PYTHONPATH` so the `lite` package can be imported.
    Set your `GEMINI_API_KEY` or other required LLM keys if using online mode.

2.  **Run the generator**:
    ```bash
    python surgery_graph.py
    ```

3.  **View results**:
    The generated `.dot` files and a JSON export will be located in the `outputs/` directory.

4.  **Visualize the graph**:
    You can use Graphviz to convert the `.dot` file to an image:
    ```bash
    dot -Tpng outputs/coronary_artery_bypass_surgery.dot -o surgery_graph.png
    ```

## Testing

Run the unit tests to verify functionality:

```bash
python test_surgery_graph.py
```

## Implementation Details

- `surgery_models.py`: Core logic for Pydantic models, triplet extraction (via `LiteClient`), and graph building (using `networkx`).
- `surgery_graph.py`: Main entry point for processing a specific surgery.
- `surgery_prompts.py`: System prompt used for LLM-based extraction.
