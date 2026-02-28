# Med Images: Medical Image Classification

## Overview

**Med Images** is a specialized diagnostic toolkit designed to classify medical images using AI models. It focuses on providing concise, professional assessments of various imaging modalities and anatomical sites.

Core functionality:
- **Medical Image Classification**: Directly analyzes and classifies medical images (X-Rays, CT-Scans, Ultrasound, MRI, etc.) to identify modalities, anatomical sites, and primary findings.

## Quick Start

### Python API

```python
from med_images import MedImageClassifier
from lite.config import ModelConfig
from pathlib import Path

# Initialize with desired model
model_config = ModelConfig(model="ollama/gemma3", temperature=0.2)
classifier = MedImageClassifier(model_config)

# Classify a medical image directly
image_result = classifier.classify_image("assets/xray.jpg")
print(image_result)

# Save results to the outputs directory
classifier.save(image_result, Path("outputs/"))
```

### Command Line Interface (CLI)

#### Classify an Image
```bash
python med_images_cli.py "assets/xray.jpg"
```

#### Classify all images in a directory
```bash
python med_images_cli.py "assets/"
```

## CLI Arguments

- `input` (required): Image file path, directory of images, or path to a file containing a list of image paths (one per line).
- `-d, --output-dir` (optional): Directory for output files (default: `outputs`).
- `-m, --model` (optional): Model to use (default: `ollama/gemma3`).
- `-v, --verbosity` (optional): Logging level 0-4 (default: `3`).
- `-s, --structured` (optional): Use structured output (Pydantic models, default: `True`).

## Key Features

- **Concise Classification**: Provides brief, professional medical assessments.
- **Multi-Modal**: Supports X-Ray, CT, MRI, Ultrasound, Mammography, Histopathology, Retinal Fundus, Dermoscopy, and SPECT.
- **Structured Output**: Uses Pydantic models for consistent, machine-readable results.
- **Batch Processing**: Easily process individual files, entire directories, or custom lists of images.

## Output Structure (Structured Mode)

When using structured output, the model returns:
- `modality`: The imaging modality (e.g., X-Ray, CT-Scan).
- `anatomical_site`: The body part or organ being imaged.
- `classification`: The primary classification or finding.
- `confidence_score`: A score from 0.0 to 1.0 representing classification confidence.

## Testing

Run the included test suite to verify functionality:

```bash
pytest test_med_images.py
```
