# Medical Flashcard Information Generator (Image-to-Report)

A CLI tool that leverages Large Language Models (LLMs) to automatically generate evidence-based medical reports by analyzing images of medical flashcards.

## Features

*   **Automated Term Extraction:** Uses Computer Vision to identify medical terms directly from images.
*   **Comprehensive Generation:** Produces detailed information on anatomy, clinical procedures, risks, and patient education.
*   **Structured Data:** Optional support for Pydantic-based JSON output.
*   **Image Context:** Uses the original image as visual context to improve the accuracy of the generated report.

## Usage

The tool requires an image file as the primary input. It will automatically identify the medical terms and generate the corresponding reports.

### Basic Usage
```bash
python medical_flashcard_cli.py assets/flashcard1.jpeg
```

### Structured Output (JSON)
```bash
python medical_flashcard_cli.py assets/flashcard2.jpeg --structured
```

### Custom Model and Output
```bash
python medical_flashcard_cli.py assets/flashcard3.jpeg -m "google/gemini-2.0-flash-exp" -d ./reports
```

## CLI Arguments

| Argument | Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| **Image** | `image` | Path to the flashcard image (Positional) | N/A |
| **Model** | `pos_model` / `-m` | LLM model to use | `ollama/gemma3:27b-cloud` |
| **Output Dir** | `-d`, `--output-dir` | Directory for output files | `outputs` |
| **Structured** | `-s`, `--structured` | Use Pydantic model for JSON output | `False` |
| **Quick** | `--quick` | Skip structured enforcement | `False` |
| **Verbosity** | `-v`, `--verbosity` | Logging level (0-4) | `2` |

## Project Structure

*   `medical_flashcard_cli.py`: Image-based CLI entry point.
*   `medical_flashcard.py`: Unified `generate_text` logic for extraction and reporting.
*   `medical_flashcard_models.py`: Data models for structured output.
*   `medical_flashcard_prompts.py`: AI persona and prompt builders.
