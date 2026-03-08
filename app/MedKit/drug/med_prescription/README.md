# Medical Prescription Analyzer & Extractor

An automated module for extracting and clinically analyzing pharmaceutical data from medical prescription images.

## Overview

The **Medical Prescription Analyzer** utilizes advanced vision-language models to digitize handwritten or printed prescriptions. Beyond simple OCR (Optical Character Recognition), it provides a deep clinical assessment of the extracted data, identifying potential drug-drug interactions, dosage compliance, and overall prescription validity to enhance patient safety.

## Key Features

- **Automated Data Extraction:** Accurately extracts patient info, prescriber details, and medication specifics (name, dosage, frequency, route, duration).
- **Clinical Safety Analysis:** Evaluates the extracted prescription for potential drug interactions and contraindications.
- **Dosage Compliance Review:** Checks if prescribed dosages align with standard clinical guidelines for the identified medications.
- **Validity Assessment:** Performs an overall check on the completeness and formal validity of the prescription (e.g., date, prescriber signature).
- **Structured Data Output:** Delivers all extracted and analyzed data via validated Pydantic models for EHR integration.
- **Vision-Powered OCR:** Specifically optimized for the challenges of medical handwriting and complex prescription layouts.

## Project Structure

- `prescription_extractor.py`: Handles the vision-based extraction of raw data from images.
- `prescription_analyzer.py`: Orchestrates the clinical analysis of extracted prescription data.
- `test_prescription_mock.py`: Suite of tests for verifying extraction and analysis logic.
- `logs/`: Diagnostic logs for tracking processing tasks.
- `outputs/`: Default directory for saving digitized prescription reports.

## Installation

Ensure dependencies are installed:

```bash
pip install pydantic pillow
```

*Note: Depends on the internal `lite` library and requires a vision-capable LLM (e.g., Gemini 1.5 Flash).*

## Usage

### Python API

```python
from med_prescription.prescription_analyzer import analyze_prescription
from lite.config import ModelConfig

# Configure with a vision-capable model
config = ModelConfig(model_id="gemini-1.5-flash")

# Path to your prescription image
image_path = "path/to/prescription_image.png"

# Perform extraction and clinical analysis
analysis = analyze_prescription(image_path, config=config)

# Access extracted and analyzed data
print(f"Patient: {analysis.extracted_data.patient_name}")
for med in analysis.extracted_data.medications:
    print(f"- {med.name}: {med.dosage}")

print(f"Safety Assessment: {analysis.overall_assessment}")
```

## ⚠️ Important Medical Disclaimer

**THIS MODULE IS FOR INFORMATIONAL AND ADMINISTRATIVE ASSISTANCE ONLY.**

- **NOT for Dispensing:** This tool is an assistant for data extraction and preliminary safety checks; it is **not** a substitute for a pharmacist's review or a physician's final authorization.
- **Extraction Errors:** OCR and vision-based extraction can contain errors, especially with handwritten medical scripts. **All extracted data must be manually verified by a qualified professional.**
- **Incomplete Context:** The analyzer does not have access to the patient's full medical record, existing allergies, or other current medications unless explicitly provided.
