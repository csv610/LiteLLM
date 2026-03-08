# Drug Addiction Analyzer

A specialized module for assessing the addictive potential, withdrawal risks, and physiological/psychological dependency factors associated with pharmaceutical substances and other compounds.

## Overview

The **Drug Addiction Analyzer** is a clinical reference tool that leverages advanced language models to evaluate the risk profiles of various medications. It provides structured insights into abuse potential, common withdrawal symptoms, and long-term dependency consequences, catering to both healthcare professionals and patients.

## Key Features

- **Dependency Risk Assessment:** Evaluates the likelihood of developing physiological and psychological dependence.
- **Withdrawal Profile:** Identifies common symptoms and severity levels associated with cessation.
- **Mechanism of Action:** Explains how the substance affects the brain's reward system and neurotransmitters.
- **Risk Mitigation Strategies:** Suggests clinically-grounded approaches for tapering and monitoring.
- **Patient-Centric Summaries:** Provides clear, non-technical explanations of risks and warning signs.
- **Structured Output:** Supports Pydantic-validated JSON data for seamless system integration.

## Project Structure

- `drug_addiction.py`: Core logic for risk analysis and LLM orchestration.
- `drug_addiction_cli.py`: Command-line interface for interactive assessment.
- `drug_addiction_models.py`: Pydantic schemas defining the addiction risk data model.
- `drug_addiction_prompts.py`: Template management for specialized addiction-focused instructions.
- `assets/`: Reference materials and input data.
- `tests/`: Suite of mock and live integration tests.

## Installation

Ensure you have the required dependencies installed:

```bash
pip install pydantic argparse
```

*Note: This module depends on the internal `lite` library for model communication.*

## Usage

### Command Line Interface

Analyze the addiction risk of a specific substance:

```bash
python drug_addiction_cli.py "Ketamine" --structured
```

**Arguments:**
- `substance_name`: The name of the drug or substance to analyze.
- `--structured`: (Optional) Output as validated JSON.
- `--model`: (Optional) LLM Model ID to use.
- `--output-dir`: (Optional) Directory for saving reports.

### Python API

```python
from drug_addiction import DrugAddiction
from drug_addiction_prompts import DrugAddictionInput
from lite.config import ModelConfig

config = ModelConfig(model_id="ollama/gemma3")
analyzer = DrugAddiction(config)

input_data = DrugAddictionInput(medicine_name="Alprazolam")
result = analyzer.generate_text(input_data, structured=True)

print(result.data.addiction_risk_level)
```

## ⚠️ Important Medical Disclaimer

**THIS MODULE IS FOR INFORMATIONAL PURPOSES ONLY.**

- Addiction treatment and risk assessment must be performed by qualified medical professionals.
- If you or someone you know is struggling with substance use, please seek professional help or contact a national helpline immediately.
- AI-generated data may not reflect individual clinical circumstances or the latest pharmacological research.
