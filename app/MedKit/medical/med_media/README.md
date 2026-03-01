# MedKit Media

MedKit Media is a specialized module within the MedKit ecosystem for searching, downloading, and analyzing medical media (images and videos). It combines DuckDuckGo's search capabilities with AI-powered medical interpretation to provide high-quality visual references and professional documentation.

## Features

- **🔍 Medical Image Search**: Automated search and validation of medical images (anatomy, radiology, pathology).
- **📥 Robust Downloader**: Downloads images with automatic validation of URLs and image formats.
- **🎥 Video Discovery**: Lists medical videos from across the web with titles, durations, and direct links.
- **✍️ AI-Powered Captions**: Generates clinically accurate captions for images, identifying landmarks and pathology.
- **📊 Educational Summaries**: Creates concise summaries for medical topics or video content, highlighting clinical significance and target audiences.
- **💻 Interactive Streamlit Components**: Includes `ddg_images_sl.py` and `ddg_videos_sl.py` for integration into Streamlit-based medical dashboards.
- **🛡️ Medical Precision**: System prompts are tailored for anatomical identification and technical medical terminology.

## Installation

Install the required dependencies:

```bash
pip install ddgs requests Pillow pydantic streamlit
```

*Note: This module depends on the internal `lite` library for AI generation and model management.*

## CLI Usage

The primary entry point is `med_media_cli.py`.

### 1. Search and Download Images
Downloads medical images to `outputs/media/images/`.

```bash
# Download 5 large images of atrial fibrillation ECG
python med_media_cli.py images "atrial fibrillation ECG" --num 5 --size Large
```

### 2. Search for Videos
Retrieves metadata and links for medical videos.

```bash
# Find 5 laparoscopic cholecystectomy videos
python med_media_cli.py videos "laparoscopic cholecystectomy" --num 5
```

### 3. Generate Medical Captions
Generates a professional description for a specific medical context.

```bash
# Generate a structured caption for a Mitral Valve MRI
python med_media_cli.py caption "mitral valve prolapse" --type "mri" --structured
```

### 4. Generate Medical Summaries
Creates an educational summary for a medical topic.

```bash
# Generate a summary for a diabetes management lecture
python med_media_cli.py summary "type 2 diabetes management" --type "lecture"
```

## Global CLI Options

| Flag | Description | Default |
| :--- | :--- | :--- |
| `-m, --model` | LLM model identifier | `ollama/gemma3` |
| `-d, --output-dir` | Directory to save all outputs | `outputs/media` |
| `-v, --verbosity` | Logging level (0-4) | `2` |
| `-s, --structured` | Output results as structured JSON | `False` |

## Project Structure

```text
med_media/
├── med_media_cli.py     # Main CLI entry point
├── med_media.py         # Core business logic and generator class
├── ddg_images.py        # Image search and download implementation
├── ddg_videos.py        # Video search implementation
├── ddg_images_sl.py     # Streamlit component for image search
├── ddg_videos_sl.py     # Streamlit component for video search
├── med_media_models.py  # Pydantic models for structured AI output
├── med_media_prompts.py # Medical-specialized prompt templates
└── tests/               # Unit and integration tests
```

## Output Models

### `MediaCaptionModel`
- `title`: Short descriptive title.
- `caption`: Comprehensive medical description.
- `key_entities`: List of anatomy, pathology, or tools identified.
- `clinical_context`: Relevance in clinical practice.

### `MediaSummaryModel`
- `topic`: Main medical subject.
- `summary`: Key information presented.
- `clinical_significance`: Medical importance.
- `target_audience`: Recommended level (Student, Resident, Specialist, Patient).

## License

Part of the MedKit Project. Proprietary/Internal Use Only.
