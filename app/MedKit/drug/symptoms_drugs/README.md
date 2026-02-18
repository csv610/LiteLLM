# Symptom-to-Drug Analyzer

## Overview

The Symptom-to-Drug Analyzer is a clinical information tool that lists medications (Generic, OTC, Rx, etc.) typically prescribed or recommended for specific symptoms. It provides rationales, common dosages, and essential safety information (precautions and contraindications) to support healthcare professionals and provide educational information to patients.

## Quick Start

### Basic Usage

List medications for a symptom with just one argument:

```bash
python symptom_drugs_cli.py "Cough"
```

This will generate a detailed list of medications and save results to `outputs/cough_drug_recommendations.json`.

## Command-Line Arguments

### Required Arguments

| Argument | Description |
|----------|-------------|
| `symptom_name` | Name of the symptom to analyze (e.g., "Cough", "Fever", "Nausea"). |

### Optional Arguments

| Short | Long | Description | Default |
|-------|------|-------------|---------|
| `-a` | `--age` | Patient's age in years (0-150) | None |
| `-c` | `--conditions` | Other medical conditions to consider (comma-separated) | None |
| `-od` | `--output-dir` | Directory for output files | `outputs` |
| `-s` | `--style` | Prompt style for analysis: `detailed`, `concise`, or `balanced` | `detailed` |
| `-v` | `--verbosity` | Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG | 2 |
| `-t` | `--structured` | Use structured output (Pydantic model) for the response | False |
| `-m` | `--model` | LLM model to use for analysis | `ollama/gemma3` |

## Usage Examples

### Example 1: Basic Analysis
```bash
python symptom_drugs_cli.py "Headache"
```
Lists common medications for headache.

### Example 2: For Specific Age Group
```bash
python symptom_drugs_cli.py "Fever" --age 5
```
Lists medications for fever suitable for a 5-year-old.

### Example 3: With Comorbidities
```bash
python symptom_drugs_cli.py "Joint Pain" --conditions "Kidney Disease, Hypertension"
```
Lists medications for joint pain while considering the patient's existing conditions.

### Example 4: Full Analysis with All Options
```bash
python symptom_drugs_cli.py "Insomnia" \
  --age 45 \
  --conditions "Anxiety" \
  --output-dir custom_output \
  --style balanced \
  --verbosity 3 \
  --structured
```

## Output Format

### Console Output

The tool provides formatted console output with the following sections:

1. **Symptom Overview**
   - Symptom name and description

2. **Recommended Medications**
   - Drug Name and Type (Generic, OTC, Rx, etc.)
   - Rationale for use
   - Common dosage ranges
   - Precautions and side effects
   - Contraindications

3. **Lifestyle Recommendations**
   - Non-pharmacological approaches

4. **Clinical Red Flags**
   - When to see a doctor urgently

5. **Technical Summary**
   - Pharmacological approach summary

### File Output

Results are saved as JSON (when using `--structured`) or Markdown.

## Understanding Drug Types

- **Generic**: The official non-proprietary name of a drug.
- **OTC (Over-the-Counter)**: Medicines sold directly to a consumer without a prescription.
- **Rx (Prescription)**: Medicines that require a legal prescription from a healthcare provider.
- **Herbal/Supplement**: Natural products or dietary supplements.

## Important Notes

### Disclaimer
This tool is for **educational and informational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

### Accuracy Considerations
- Medication recommendations depend on current clinical guidelines.
- Always verify information against authoritative medical sources.
- Dosage information is for general reference only.
