# MedKit Media

MedKit Media is a specialized tool within the MedKit ecosystem designed for searching, downloading, and generating AI-powered analysis for medical media, including images and videos. It leverages DuckDuckGo for content discovery and AI models (via the `lite` library) for professional medical interpretation.

## Features

- **Medical Image Search & Download**: Search for high-quality medical images (e.g., anatomy, pathology, radiology) and download them locally with automatic validation.
- **Medical Video Discovery**: Find relevant medical videos, including educational lectures and surgical procedures, with metadata (title, duration, URL).
- **AI-Powered Medical Captions**: Generate professional, clinically accurate captions for medical media, identifying key entities and clinical context.
- **Educational Summaries**: Create concise medical summaries for topics or video content, highlighting clinical significance and target audiences.
- **Streamlit Web Components**: Includes modular components (`ddg_images_sl.py`, `ddg_videos_sl.py`) for building interactive medical media dashboards and search interfaces.
- **Structured Data Support**: Export AI analysis in structured JSON formats or clean Markdown for integration into other medical applications.

## Installation

Ensure you have the necessary dependencies installed:

```bash
pip install ddgs requests Pillow pydantic streamlit
```

*Note: This tool depends on the internal `lite` library for AI generation.*

## CLI Usage

The project provides a unified CLI entry point: `med_media_cli.py`.

### 1. Search and Download Images
Search for medical images and save them to a local directory.

```bash
python med_media_cli.py images "atrial fibrillation ECG" --num 5 --size Large
```

### 2. Search for Videos
Find medical videos related to a specific topic.

```bash
python med_media_cli.py videos "laparoscopic cholecystectomy" --num 3
```

### 3. Generate Medical Captions
Generate a professional caption for a medical topic or image context.

```bash
python med_media_cli.py caption "mitral valve prolapse" --type "mri" --structured
```

### 4. Generate Medical Summaries
Generate a medical summary for educational or clinical review.

```bash
python med_media_cli.py summary "type 2 diabetes management" --type "lecture"
```

## Global Options

- `-m, --model`: AI model to use (default: `ollama/gemma3`).
- `-d, --output-dir`: Base directory for saved results (default: `outputs/media`).
- `-v, --verbosity`: Logging verbosity level (0-4).
- `-s, --structured`: Output results as structured JSON.

## Project Structure

- `med_media_cli.py`: Command-line interface.
- `med_media.py`: Core logic for searching and AI generation.
- `med_media_models.py`: Pydantic models for structured output.
- `ddg_images.py` & `ddg_videos.py`: DuckDuckGo search wrappers.
- `med_media_prompts.py`: Medical-specific AI prompt templates.
- `tests/`: Comprehensive test suite for all modules.

## License

Part of the MedKit Project. Proprietary/Internal Use Only.
