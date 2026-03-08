# Drug-Food Interaction Analyzer

## Overview

The **Drug-Food Interaction Analyzer** is a specialized medical information and reference tool designed to identify and analyze the complex interactions between medications and various food and beverages. By leveraging advanced language models and structured data patterns, it provides healthcare professionals with detailed clinical insights and patients with clear, actionable guidance.

This module is part of a larger medical AI ecosystem and prioritizes clinical accuracy, patient safety, and standardized reporting.

---

## ⚠️ Legal and Ethical Disclaimer

**IMPORTANT: READ BEFORE USE**

This application is classified as a **HIGH-RISK MEDICAL AI SYSTEM**. It is intended for **INFORMATION AND REFERENCE PURPOSES ONLY**.

- **Not for Clinical Diagnosis:** This tool must NOT be used for clinical diagnosis, medical decision-making, or emergency situations.
- **Professional Verification Required:** All information must be verified through authoritative medical sources by qualified healthcare professionals.
- **No Substitute for Judgment:** This software is not a substitute for professional medical judgment.

By using this software, you agree to the terms outlined in the [Legal and Ethical Binding Contract](contract.md).

---

## Key Features

- **Comprehensive Interaction Analysis:** Identifies known drug-food interactions across multiple categories (e.g., Citrus, Dairy, High-Fat, Caffeine).
- **Severity Assessment:** Categorizes interactions from "NONE" to "CONTRAINDICATED" for quick risk evaluation.
- **Mechanism Identification:** Explains how foods affect drug absorption, metabolism, or efficacy (e.g., PK/PD changes).
- **Management Recommendations:** Provides specific guidance on medication timing relative to meals and foods to avoid.
- **Patient-Friendly Summaries:** Translates complex pharmacological data into simple, non-technical instructions and warning signs.
- **Structured Output:** Supports both Markdown reports and machine-readable JSON/Pydantic models for integration.
- **Context-Aware:** Incorporates patient-specific factors such as age, diet type, and medical conditions for more relevant analysis.

---

## Architecture

The module is structured for modularity and scalability:

- **`drug_food_interaction.py`**: The core analyzer class that orchestrates the interaction with the underlying AI models.
- **`drug_food_interaction_models.py`**: Robust Pydantic models defining the structured data schemas for interaction details, patient summaries, and data availability.
- **`drug_food_interaction_prompts.py`**: A specialized prompt engineering layer that ensures consistent and clinically grounded responses from LLMs.
- **`drug_food_interaction_cli.py`**: A feature-rich command-line interface for local execution and integration.
- **`contract.md`**: The foundational legal and ethical framework governing the use of the system.

---

## Installation

Ensure you have the required dependencies installed:

```bash
pip install pydantic argparse
```

*Note: This module depends on the internal `lite` library for model communication and logging configuration.*

---

## Usage

### Command Line Interface

You can run the analyzer directly from the terminal:

```bash
python drug_food_interaction_cli.py "Warfarin" --age 65 --conditions "Atrial Fibrillation" --structured
```

### Arguments

| Argument | Description | Default |
| :--- | :--- | :--- |
| `medicine_name` | Name of the medicine to analyze | (Required) |
| `--age`, `-a` | Patient's age (0-150) | `None` |
| `--conditions`, `-c` | Patient's medical conditions | `None` |
| `--diet-type` | Patient's diet type (e.g., Vegan, Keto) | `None` |
| `--structured`, `-s` | Use Pydantic models for structured output | `False` |
| `--model`, `-m` | LLM Model ID to use | `ollama/gemma3` |
| `--output-dir`, `-d` | Directory for output files | `outputs` |

---

## Data Structure

The application produces a `DrugFoodInteractionModel` which includes:

1.  **Interaction Details**:
    - `overall_severity`: Clinical risk level.
    - `mechanism_of_interaction`: Pharmacological explanation.
    - `food_category_interactions`: Specific breakdown by food group.
2.  **Patient Friendly Summary**:
    - `simple_explanation`: Non-technical overview.
    - `what_patient_should_do`: Clear action steps.
    - `warning_signs`: Symptoms to monitor.
3.  **Metadata**:
    - `confidence_level`: AI's confidence in the assessment.
    - `data_source_type`: Type of data used (e.g., Clinical Studies, FDA Warnings).

---

## License

© 2024 Medical AI Software Provider. All Rights Reserved.
Refer to `contract.md` for full usage rights and restrictions.
