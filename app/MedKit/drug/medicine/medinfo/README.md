# Comprehensive Medicine Information Generator

An AI-powered clinical reference module for generating detailed pharmacological profiles and patient-centered information for any given medication.

## Overview

The **Medicine Information Generator** provides a standardized, deep-dive analysis of individual drugs. By leveraging advanced language models, it produces comprehensive reports covering clinical indications, mechanisms of action, safety profiles, and practical administration guidance, ensuring both technical accuracy for professionals and clarity for patients.

## Key Features

- **Clinical Profile:** Detailed information on indications, contraindications, and off-label uses.
- **Pharmacological Mechanism:** Clear explanation of how the medication works at a molecular and physiological level.
- **Safety & Side Effects:** Categorized list of common and serious adverse reactions and necessary monitoring.
- **Administration Guidance:** Specific instructions on dosage, timing, and what to do in case of a missed dose.
- **Patient-Friendly Summary:** Simplified overview of the medication, its purpose, and critical warnings.
- **Structured Data:** Supports Pydantic-validated JSON output for integration into medical databases and applications.

## Project Structure

- `medicine_info.py`: Core logic for generating medication profiles.
- `medicine_info_cli.py`: Command-line interface for interactive report generation.
- `medicine_info_models.py`: Pydantic schemas defining the comprehensive medicine data model.
- `medicine_info_prompts.py`: Optimized clinical prompts for high-fidelity medication analysis.

## Installation

Ensure dependencies are installed:

```bash
pip install pydantic argparse
```

*Note: Depends on the internal `lite` library.*

## Usage

### Command Line Interface

Generate a comprehensive report for a medication:

```bash
python medicine_info_cli.py "Metoprolol" --structured
```

**Arguments:**
- `medicine`: The name of the medication (e.g., 'Aspirin', 'Metformin').
- `--structured`: (Optional) Output as validated JSON.
- `--model`: (Optional) LLM Model ID to use.
- `--output-dir`: (Optional) Directory for saving generated reports.

### Python API

```python
from medicine_info import MedicineInfoGenerator
from lite.config import ModelConfig

config = ModelConfig(model_id="ollama/gemma3")
generator = MedicineInfoGenerator(config)

result = generator.generate_text("Lisinopril", structured=True)
print(result.data.clinical_profile.indications)
```

## ⚠️ Important Medical Disclaimer

**THIS MODULE IS FOR INFORMATIONAL AND EDUCATIONAL PURPOSES ONLY.**

- **Professional Consultation Required:** Always seek the advice of a physician or other qualified health provider with any questions regarding a medical condition or medication.
- **Verification Mandatory:** AI-generated pharmacological data must be cross-referenced with authoritative sources (e.g., FDA labels, Lexicomp, Micromedex).
- **Not for Clinical Decision-Making:** This tool is a reference and should not be used as the sole basis for prescribing or administering medication.
