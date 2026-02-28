# Med Images: Medical Diagnostics & Image Classification

## Overview

**Med Images** is a comprehensive diagnostic toolkit designed to bridge the gap between complex medical testing and accessible, evidence-based documentation. It provides two core functionalities:

1.  **Medical Test Documentation**: Generates exhaustive, structured information for thousands of medical tests (lab tests, imaging, etc.), covering everything from preparation to interpretation.
2.  **Medical Image Classification**: Directly analyzes and classifies medical images (X-Rays, CT-Scans, Ultrasound, MRI, etc.) to identify modalities, anatomical sites, and clinical findings.

By standardizing access to this information, **Med Images** helps reduce patient anxiety, clinical inefficiency, and potential medical errors due to improper test preparation or result interpretation.

## Quick Start

### Python API

```python
from med_images import MedImageClassifier
from lite.config import ModelConfig
from pathlib import Path

# Initialize with desired model
model_config = ModelConfig(model="ollama/gemma3", temperature=0.2)
classifier = MedImageClassifier(model_config)

# 1. Generate information for a specific test
test_info = classifier.generate_text("blood glucose test")
print(test_info)

# 2. Classify a medical image directly
image_result = classifier.classify_image("assets/xray.jpg")
print(image_result)

# Save results to the outputs directory
classifier.save(image_result, Path("outputs/"))
```

### Command Line Interface (CLI)

#### Generate Test Information
```bash
python med_images_cli.py "complete blood count"
```

#### Classify an Image
```bash
python med_images_cli.py "assets/xray.jpg" --image --structured
```

## CLI Arguments

- `input` (required): Medical test name, image file path, or path to a file containing a list (one per line).
- `-d, --output-dir` (optional): Directory for output files (default: `outputs`).
- `-m, --model` (optional): Model to use (default: `ollama/gemma3`).
- `-v, --verbosity` (optional): Logging level 0-4 (default: `3`).
- `-s, --structured` (optional): Use structured output (Pydantic models).
- `-i, --image` (optional): Force image classification mode.

## Key Features

- **Evidence-Based**: Generates documentation based on clinical standards.
- **Multi-Modal**: Supports X-Ray, CT, MRI, Ultrasound, Mammography, Histopathology, Fundus, Dermoscopy, and SPECT.
- **Structured Output**: Built-in support for Pydantic models for easy integration into healthcare systems.
- **Schema-Aware**: Uses specialized prompts to ensure accuracy in medical terminology and reference ranges.

## Coverage Areas

- **Identification**: Official and alternative names, categories, and specialties.
- **Process**: Preparation, specimen requirements, and step-by-step procedures.
- **Results**: Normal/abnormal ranges, critical values, and interfering factors.
- **Population Specific**: Considerations for pediatrics, geriatrics, and pregnancy.
- **Technical**: Methodology, sensitivity, specificity, and FDA status.

## Testing

Run the included test suite to verify functionality:

```bash
pytest test_med_images.py
```
