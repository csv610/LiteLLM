# Drug-Drug Interaction Analyzer - User Guide

## Overview

The Drug-Drug Interaction Analyzer is a command-line tool that analyzes potential harmful interactions between two medicines and provides clinical recommendations. It uses AI-powered analysis to identify dangerous drug combinations and understand the mechanisms, clinical effects, and management strategies for interactions.

**Key Use Cases:**
- Identify dangerous drug combinations before prescribing
- Counsel patients on medication compatibility
- Review patient medications for interactions
- Support polypharmacy management in elderly patients
- Generate clinical decision support recommendations
- Create interaction reports for healthcare providers

---

## Installation & Requirements

### Prerequisites
- Python 3.8+
- MedKit client library
- Required dependencies: `rich` (for formatted output), `argparse`, `logging`

### Running the Tool
```bash
python drug_drug_interaction_cli.py MEDICINE1 MEDICINE2 [OPTIONS]
```

---

## Basic Usage

### Simplest Example: Two Medicines
```bash
python drug_drug_interaction_cli.py "Warfarin" "Aspirin"
```

This performs a basic interaction analysis between Warfarin and Aspirin, with results saved to `outputs/warfarin_aspirin_interaction.json`.

### With Patient Age
```bash
python drug_drug_interaction_cli.py "Metformin" "Lisinopril" --age 65
```

Analyzes the interaction with patient age context (useful for age-dependent interactions).

---

## Command-Line Arguments

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `MEDICINE1` | Name of the first medicine | `Warfarin` |
| `MEDICINE2` | Name of the second medicine | `Aspirin` |

### Optional Arguments

#### Patient Information
| Argument | Short | Type | Description | Example |
|----------|-------|------|-------------|---------|
| `--age` | `-a` | int | Patient's age in years (0-150) | `--age 65` |
| `--dosage1` | `-d1` | str | Dosage information for first medicine | `--dosage1 "500mg twice daily"` |
| `--dosage2` | `-d2` | str | Dosage information for second medicine | `--dosage2 "100mg once daily"` |
| `--conditions` | `-c` | str | Patient's medical conditions (comma-separated) | `--conditions "hypertension, diabetes"` |

#### Output Options
| Argument | Short | Type | Description | Example |
|----------|-------|------|-------------|---------|
| `--output` | `-o` | path | Output file path for results | `--output interaction.json` |
| `--json-output` | `-j` | flag | Output results as JSON to stdout (in addition to file) | `--json-output` |

#### Analysis Options
| Argument | Short | Type | Description | Options |
|----------|-------|------|-------------|---------|
| `--prompt-style` | `-p` | str | Prompt style for analysis | `detailed`, `concise`, `balanced` |
| `--no-schema` | | flag | Disable schema-based prompt generation | (flag, no value) |
| `--verbose` | `-v` | flag | Enable verbose logging output | (flag, no value) |

---

## Usage Examples

### Example 1: Basic Analysis
```bash
python drug_drug_interaction_cli.py "Ibuprofen" "Aspirin"
```
**Output:** Results displayed in formatted panels + saved to `outputs/ibuprofen_aspirin_interaction.json`

### Example 2: Comprehensive Analysis with Patient Details
```bash
python drug_drug_interaction_cli.py "Simvastatin" "Clarithromycin" \
  --age 72 \
  --dosage1 "20mg once daily" \
  --dosage2 "500mg twice daily" \
  --conditions "high cholesterol, infection"
```
Analyzes the interaction with full patient context for more personalized recommendations.

### Example 3: With Custom Output Path
```bash
python drug_drug_interaction_cli.py "Metformin" "ACE inhibitor" \
  --output /reports/diabetes_medication_interaction.json
```
Saves results to a custom location with a descriptive filename.

### Example 4: Detailed Analysis with Verbose Output
```bash
python drug_drug_interaction_cli.py "Warfarin" "NSAIDs" \
  --prompt-style detailed \
  --verbose
```
Provides detailed analysis with full logging information for debugging or documentation.

### Example 5: JSON Output to Console
```bash
python drug_drug_interaction_cli.py "Sertraline" "Tramadol" \
  --json-output
```
Displays structured JSON results directly in the terminal in addition to saving to file.

### Example 6: Concise Analysis
```bash
python drug_drug_interaction_cli.py "Lisinopril" "Potassium supplement" \
  --prompt-style concise
```
Provides a shorter, more concise analysis compared to the default detailed style.

---

## Output Structure

The tool produces two types of output:

### 1. Console Display (Formatted Panels)
When you run the command, you'll see formatted output including:
- **Data Availability:** Whether sufficient data exists for the analysis
- **Drug Interaction Details:** Severity, confidence level, and data source
- **Mechanism of Interaction:** How the drugs interact chemically/pharmacologically
- **Clinical Effects:** Observable symptoms and complications
- **Management Recommendations:** How to handle the interaction
- **Alternative Medicines:** Safe alternatives to consider
- **Simple Explanation:** Patient-friendly explanation of the interaction
- **What Patient Should Do:** Action items for patients
- **Warning Signs:** Symptoms to watch for
- **When to Seek Help:** Emergency situations requiring medical attention
- **Technical Summary:** Detailed clinical summary

### 2. JSON File Output
Results are automatically saved to a JSON file with the structure:
```json
{
  "interaction_details": {
    "drug1_name": "...",
    "drug2_name": "...",
    "severity_level": "NONE|MINOR|SIGNIFICANT|CONTRAINDICATED",
    "confidence_level": "HIGH|MODERATE|LOW",
    "mechanism_of_interaction": "...",
    "clinical_effects": "...",
    "management_recommendations": "...",
    "alternative_medicines": "...",
    "data_source_type": "..."
  },
  "patient_friendly_summary": {
    "simple_explanation": "...",
    "what_patient_should_do": "...",
    "warning_signs": "...",
    "when_to_seek_help": "..."
  },
  "technical_summary": "...",
  "data_availability": {
    "data_available": true|false,
    "reason": "..."
  }
}
```

---

## Severity Levels

The tool classifies interactions into four severity levels:

| Level | Description | Action |
|-------|-------------|--------|
| **NONE** | No significant interaction | Safe to use together |
| **MINOR** | Small interaction with minimal clinical significance | Monitor but generally safe |
| **SIGNIFICANT** | Notable interaction requiring management | Requires dose adjustment or monitoring |
| **CONTRAINDICATED** | Dangerous combination that should be avoided | Do not use together; consider alternatives |

---

## Confidence Levels

The confidence of the interaction assessment:

| Level | Meaning |
|-------|---------|
| **HIGH** | Strong clinical evidence and documentation |
| **MODERATE** | Moderate evidence, well-documented |
| **LOW** | Limited evidence or theoretical interaction |

---

## Common Use Cases with Examples

### Use Case 1: Emergency Department Triage
```bash
python drug_drug_interaction_cli.py "Warfarin" "Ibuprofen" \
  --verbose \
  --output /emergency/drug_check_warfarin_ibuprofen.json
```

### Use Case 2: Patient Counseling
```bash
python drug_drug_interaction_cli.py "Metformin" "Lisinopril" \
  --age 58 \
  --dosage1 "1000mg twice daily" \
  --dosage2 "10mg once daily" \
  --prompt-style balanced
```

### Use Case 3: Medication Review for Elderly Patient
```bash
python drug_drug_interaction_cli.py "Simvastatin" "Amiodarone" \
  --age 82 \
  --conditions "heart failure, high cholesterol, arrhythmia" \
  --verbose
```

### Use Case 4: Pharmacy System Integration
```bash
python drug_drug_interaction_cli.py "Drug1" "Drug2" \
  --json-output \
  --output /pharmacy/integration/check_result.json
```
This can be easily parsed by other systems due to JSON output.

---

## Understanding the Results

### Data Availability
If the tool cannot find sufficient information about the drug combination, it will display:
```
⚠️ Data not available for this drug combination
```
This might happen for very new medications or uncommon combinations.

### Severity Color Coding (Console Output)
- 🟢 **NONE** (Green): Safe combination
- 🔵 **MINOR** (Blue): Minor interaction, usually safe
- 🟡 **SIGNIFICANT** (Yellow): Important interaction, management needed
- 🔴 **CONTRAINDICATED** (Red): Dangerous combination, avoid

---

## Troubleshooting

### Issue: "Invalid input: Medicine name cannot be empty"
**Solution:** Ensure both medicine names are provided and non-empty.
```bash
python drug_drug_interaction_cli.py "Aspirin" "Ibuprofen"
```

### Issue: "Invalid input: Age must be between 0 and 150 years"
**Solution:** Provide a valid age between 0 and 150.
```bash
python drug_drug_interaction_cli.py "Drug1" "Drug2" --age 65
```

### Issue: "Invalid prompt style"
**Solution:** Use only valid options: `detailed`, `concise`, or `balanced`.
```bash
python drug_drug_interaction_cli.py "Drug1" "Drug2" --prompt-style detailed
```

### Issue: Output file not created
**Solution:** Ensure the output directory exists or use the `--output` flag with a full path. The tool will auto-create directories.
```bash
python drug_drug_interaction_cli.py "Drug1" "Drug2" --output results/interaction.json
```

### Issue: Verbose logging is too much
**Solution:** Omit the `--verbose` flag for normal output.

---

## Configuration

The tool uses a configuration system (`DrugDrugInteractionConfig`) that supports:
- **Database Path:** Auto-generated LMDB cache at `../storage/drug_drug_interaction.lmdb`
- **Database Capacity:** Default 500 MB for storing cached results
- **Caching:** Enabled by default to speed up repeated queries
- **Prompt Style:** Affects detail level of analysis

### Default Settings
- **Model:** `ollama/gemma3:12b`
- **Prompt Style:** Detailed
- **Cache:** Enabled
- **Output Location:** `outputs/{medicine1}_{medicine2}_interaction.json`

---

## Advanced Features

### Schema-Based Prompting
By default, the tool uses schema-based prompting for structured, reliable responses. To disable:
```bash
python drug_drug_interaction_cli.py "Drug1" "Drug2" --no-schema
```

### Caching System
Results are cached in an LMDB database for faster repeated queries. Clear the cache by deleting:
```bash
rm ../storage/drug_drug_interaction.lmdb
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success - analysis completed |
| `1` | Error - invalid input or processing error |

---

## Performance Notes

- First run for a drug combination may take longer (AI processing)
- Subsequent identical queries return cached results instantly
- Verbose mode (`--verbose`) will show detailed processing steps
- Disable verbose for cleaner output in production use

---

## API Integration

For programmatic use, import the module directly:

```python
from lite.config import ModelConfig
from drug_drug_interaction import DrugDrugInteractionGenerator
from drug_drug_interaction_prompts import DrugDrugInput

# Initialize the generator
model_config = ModelConfig(model="ollama/gemma3", temperature=0.2)
generator = DrugDrugInteractionGenerator(model_config)

# Create input configuration
drug_input = DrugDrugInput(
    medicine1="Warfarin",
    medicine2="Aspirin",
    age=65,
    dosage1="5mg once daily",
    dosage2="100mg once daily",
    medical_conditions="atrial fibrillation"
)

# Generate interaction analysis
result = generator.generate_text(drug_input, structured=True)

# Save to file
from pathlib import Path
saved_path = generator.save(result, Path("outputs/"))
print(f"Interaction analysis saved to: {saved_path}")
```

---

## Tips for Best Results

1. **Use Full Drug Names:** Use complete, accurate drug names (e.g., "Warfarin" not "Warf")
2. **Include Patient Context:** Age and medical conditions improve recommendation accuracy
3. **Be Specific with Dosages:** Dosage information helps assess risk level
4. **Review Both Views:** Check both clinical details and patient-friendly summary
5. **Save Results:** Always use `--output` to save results for medical records
6. **Consult Professionals:** Use this tool to inform, not replace, professional medical judgment

---

## Support & Documentation

For additional information:
- Check logs with `--verbose` flag for debugging
- Review the JSON output for structured data integration
- Refer to drug interaction databases (e.g., DrugBank, FDA) for authoritative information
- Consult with healthcare professionals for clinical decisions

---

## Disclaimer

This tool is designed for educational and decision-support purposes. Always consult qualified healthcare professionals before making medication decisions. The AI-generated analysis is informational and should not replace professional medical judgment.

