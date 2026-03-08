# MedKit Drug

A comprehensive suite of pharmacology-related modules for medication analysis, clinical decision support, and patient education.

## Overview

The `drug` package provides a unified set of tools for processing and analyzing pharmaceutical data. Leveraging advanced language models and structured medical datasets, it enables high-fidelity analysis of drug interactions, patient-friendly medication explanations, and prescription processing.

## Included Modules

| Module | Description |
| :--- | :--- |
| **`drug_addiction`** | Analysis of medication addiction patterns, risk factors, and monitoring. |
| **`drug_disease`** | Drug-disease interaction analysis for contraindications and precautions. |
| **`drug_drug`** | Clinical analysis of potential interactions between multiple medications. |
| **`drug_food`** | Analysis of dietary and beverage interactions with medications. |
| **`drugs_comparision`** | Side-by-side comparison of different medications. |
| **`med_prescription`** | Automated extraction and analysis of medical prescriptions. |
| **`medicine/drugbank`** | Integration with DrugBank for detailed pharmaceutical data. |
| **`medicine/medinfo`** | General medication information and pharmacological profiles. |
| **`medicine/rxmed`** | Integration with RxNorm and RxClass for standardized drug naming and classification. |
| **`similar_drugs`** | Identification of therapeutic alternatives and similar medications. |
| **`symptoms_drugs`** | Mapping of clinical symptoms to appropriate medication categories. |
| **`medicine_explainer.py`** | Plain-language, jargon-free medication explanations for patients. |

## Entry Point

The `drug_cli.py` script serves as the unified command-line interface for the entire `medkit-drug` suite.

```bash
python drug_cli.py [module] [arguments]
```

## Key Objectives

1.  **Clinical Accuracy:** Prioritize evidence-based pharmacological data.
2.  **Safety First:** Explicitly identify contraindications and high-risk interactions.
3.  **Standardization:** Use structured Pydantic models to ensure consistent data output across all modules.
4.  **Accessibility:** Provide both technical clinical insights and simplified patient-centered summaries.

## Installation

Ensure the core `MedKit` environment and dependencies are installed.

```bash
pip install -r requirements.txt
```

*Note: Individual modules may have specific dependencies or configuration requirements (e.g., API keys for LLM access).*

## ⚠️ Important Medical Disclaimer

**THIS SOFTWARE IS FOR INFORMATIONAL AND EDUCATIONAL PURPOSES ONLY.**

- It is **not** a substitute for professional medical advice, diagnosis, or treatment.
- Always consult with a qualified healthcare professional before making any medical decisions.
- AI-generated outputs must be cross-referenced with authoritative clinical sources (e.g., FDA labels, Lexicomp, Micromedex).
- All users must adhere to the terms specified in the `contract.md` found within individual modules.
