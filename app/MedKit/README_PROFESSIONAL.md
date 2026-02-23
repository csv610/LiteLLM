# MedKit Professional CLI Tools

The MedKit project has been upgraded to use industry-standard Python packaging. You can now use professional CLI commands instead of running Python scripts directly.

## Installation

To enable the new commands, run the following in your terminal from the root of the project:

```bash
pip install -e .
```

The `-e` flag ensures that any changes you make to the code are immediately reflected in the commands.

## Available Commands

Once installed, you can use the following commands from anywhere in your terminal:

| Command | Description | Source File |
|---------|-------------|-------------|
| `medkit-medical` | Unified medical info (anatomy, disease, surgery, etc.) | `medical/medical_cli.py` |
| `medkit-sane` | SANE Interview System | `sane_interview/sane_interview_cli.py` |
| `medkit-recognizer` | Medical Entity Recognition (drugs, pathogens, etc.) | `recognizers/medical_recognizer_cli.py` |
| `medkit-dictionary` | Medical Dictionary Builder & Reviewer | `med_dictionary/medical_dictionary_cli.py` |
| `medkit-codes` | ICD-11 Medical Code Fetcher | `med_codes/get_icd11.py` |
| `medkit-mental` | Mental Health Assessment Chat | `mental_health/mental_health_chat_app.py` |
| `medkit-drug` | Medicine & Interaction Explainer | `drug/medicine_explainer.py` |

## Usage Examples

### Anatomy Info
```bash
medkit-medical anatomy "heart"
```

### Mental Health Assessment
```bash
medkit-mental
```

### Drug Recognition
```bash
medkit-recognizer drug "Aspirin"
```

## Internal Utilities
Internal development scripts and demos have been moved to the `scripts/` folder to keep the main package clean.
- `scripts/med_codes_demo.py`: Demo for ICD-11 code fetching.

---

**Note:** Your existing workflow of running `python folder/script.py` still works perfectly and will not be affected by these changes.
