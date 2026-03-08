# Side-by-Side Medication Comparison Tool

A clinical decision support module for comparing two medications across therapeutic, regulatory, and safety metrics.

## Overview

The **Medication Comparison Tool** provides a structured, side-by-side analysis of two different drugs. By evaluating clinical efficacy, safety profiles, dosage requirements, and cost-effectiveness, it helps healthcare providers and patients make informed treatment choices tailored to specific indications and patient demographics.

## Key Features

- **Side-by-Side Analysis:** Direct comparison of indications, mechanism of action, and therapeutic class.
- **Safety Profile Comparison:** Evaluates differences in side effects, contraindications, and drug interactions.
- **Patient-Specific Tailoring:** Adjusts comparisons based on patient age, medical conditions, and specific use cases.
- **Efficacy Assessment:** Compares the clinical effectiveness of both medications for a given indication.
- **Practical Considerations:** Includes comparisons of administration routes, frequency, and common costs.
- **Structured Data Support:** Delivers validated JSON output via Pydantic models for systematic integration.

## Project Structure

- `drugs_comparison.py`: Core logic for orchestrating the comparison analysis.
- `drugs_comparison_cli.py`: Feature-rich command-line interface.
- `drugs_comparison_models.py`: Pydantic schemas defining the comparison data model.
- `drugs_comparison_prompts.py`: Optimized templates for side-by-side drug analysis.

## Installation

Ensure dependencies are installed:

```bash
pip install pydantic argparse
```

*Note: Depends on the internal `lite` library.*

## Usage

### Command Line Interface

Compare two medications for a specific use case:

```bash
python drugs_comparison_cli.py "Aspirin" "Ibuprofen" --use-case "Chronic Back Pain" --age 45 --structured
```

**Arguments:**
- `medicine1`, `medicine2`: The names of the two medications to compare.
- `--use-case`: (Optional) The specific clinical indication for the comparison.
- `--age`: (Optional) Patient age for tailored analysis.
- `--conditions`: (Optional) Patient medical conditions (comma-separated).
- `--structured`: (Optional) Output as validated JSON.
- `--model`: (Optional) LLM Model ID to use.

### Python API

```python
from drugs_comparison import DrugsComparison, DrugsComparisonInput
from lite.config import ModelConfig

config = ModelConfig(model_id="ollama/gemma2")
analyzer = DrugsComparison(config)

input_data = DrugsComparisonInput(
    medicine1="Atorvastatin",
    medicine2="Rosuvastatin",
    use_case="Hyperlipidemia"
)

result = analyzer.generate_text(input_data, structured=True)
print(result.data.comparison_summary)
```

## ⚠️ Important Medical Disclaimer

**THIS MODULE IS FOR INFORMATIONAL AND EDUCATIONAL PURPOSES ONLY.**

- **No Medical Recommendation:** This tool compares data; it does **not** recommend one medication over another for a specific patient.
- **Clinical Judgment Required:** All therapeutic decisions must be made by a qualified healthcare professional.
- **Incomplete Data:** Comparison metrics may not capture all clinical nuances, latest trial data, or individual patient sensitivities.
