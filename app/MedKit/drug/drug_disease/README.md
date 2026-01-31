# Drug-Disease Interaction Analyzer 

## Overview

The Drug-Disease Interaction Analyzer is a clinical decision support tool that analyzes how medical conditions affect drug efficacy, safety, and metabolism. It provides guidance on potential interactions between medications and patient conditions, helping clinicians make informed prescribing decisions.

## Quick Start

### Basic Usage

Analyze the interaction between a medicine and a condition with just two arguments:

```bash
python drug_disease_interaction_cli.py "Metformin" "Kidney Disease"
```

This will generate a detailed analysis and save results to `outputs/metformin_kidney_disease_interaction.json`.

## Command-Line Arguments

### Required Arguments

| Argument | Description |
|----------|-------------|
| `medicine_name` | Name of a **single** medicine to analyze (e.g., "Metformin", "Warfarin"). Multiple medicines are not supported. |
| `condition_name` | Name of a **single** medical condition (e.g., "Kidney Disease", "Liver Disease"). Multiple conditions are not supported. |

### Optional Arguments

| Short | Long | Description | Default |
|-------|------|-------------|---------|
| `-S` | `--severity` | Severity level of the condition: `mild`, `moderate`, or `severe` | None |
| `-a` | `--age` | Patient's age in years (0-150) | None |
| `-M` | `--medications` | Other medications the patient is taking (comma-separated) | None |
| `-od` | `--output-dir` | Directory for output files | `outputs` |
| `-s` | `--style` | Prompt style for analysis: `detailed`, `concise`, or `balanced` | `detailed` |
| `-v` | `--verbosity` | Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG | 2 |
| `-t` | `--structured` | Use structured output (Pydantic model) for the response | False |
| `-m` | `--model` | LLM model to use for analysis | `ollama/gemma3` |

## Usage Examples

### Example 1: Basic Analysis
```bash
python drug_disease_interaction_cli.py "Metformin" "Kidney Disease"
```
Analyzes how kidney disease affects metformin use.

### Example 2: With Condition Severity
```bash
python drug_disease_interaction_cli.py "Warfarin" "Liver Disease" --severity severe
```
Analyzes warfarin interaction with severe liver disease, which affects dosing and safety.

### Example 3: With Patient Demographics
```bash
python drug_disease_interaction_cli.py "Lisinopril" "Hypertension" --age 72 --medications "Atorvastatin, Aspirin"
```
Analyzes lisinopril use in a 72-year-old patient already on cholesterol and blood-thinning medications.

### Example 4: Full Analysis with All Options
```bash
python drug_disease_interaction_cli.py "NSAIDs" "Asthma" \
  --severity moderate \
  --age 45 \
  --medications "Albuterol, Prednisone" \
  --output-dir custom_analysis_output \
  --style balanced \
  --verbosity 3 \
  --structured
```
Complete analysis with all optional parameters and structured output.

### Example 5: Concise Analysis
```bash
python drug_disease_interaction_cli.py "Ibuprofen" "Hypertension" --style concise
```
Generates a more concise analysis focused on key findings.

## Output Format

### Console Output

The tool provides formatted console output with the following sections:

1. **Interaction Overview**
   - Medicine and condition names
   - Overall severity level (NONE → CONTRAINDICATED)
   - Confidence level of the analysis
   - Data source type

2. **Mechanism of Interaction**
   - How the condition affects the drug pharmacokinetics and pharmacodynamics

3. **Efficacy Impact**
   - Whether the condition reduces or enhances drug effectiveness
   - Clinical significance of the impact

4. **Safety Impact**
   - Additional safety risks when using the drug in this condition
   - Risk level assessment

5. **Dosage Adjustments**
   - Whether dose or frequency adjustments are needed
   - Specific recommendations for modifications

6. **Management Recommendations**
   - Clinical action items for safe prescribing
   - Monitoring requirements

7. **Patient-Friendly Guidance**
   - Simple explanation in layman's terms
   - What patients should do
   - Signs of problems to watch for
   - When to contact a doctor

8. **Technical Summary**
   - Key findings and evidence summary

### File Output

Results are saved as JSON with the following structure:

```json
{
  "interaction_details": {
    "medicine_name": "Metformin",
    "condition_name": "Kidney Disease",
    "overall_severity": "CONTRAINDICATED",
    "confidence_level": "HIGH",
    "data_source_type": "CLINICAL_GUIDELINE",
    "mechanism_of_interaction": "...",
    "efficacy_impact": { ... },
    "safety_impact": { ... },
    "dosage_adjustment": { ... },
    "management_strategy": { ... }
  },
  "patient_friendly_summary": {
    "simple_explanation": "...",
    "what_patient_should_do": "...",
    "signs_of_problems": "...",
    "when_to_contact_doctor": "..."
  },
  "data_availability": {
    "data_available": true,
    "reason": null
  },
  "technical_summary": "..."
}
```

## Understanding Severity Levels

The tool classifies interaction severity on this scale:

| Severity | Meaning | Action |
|----------|---------|--------|
| **NONE** | No significant interaction | Use with standard precautions |
| **MINOR** | Small interaction with limited clinical significance | Monitor patient; minimal adjustment needed |
| **MODERATE** | Moderate interaction affecting safety or efficacy | Consider alternatives or dose adjustment; monitor closely |
| **SEVERE** | Significant interaction with major clinical implications | Avoid if possible; if necessary, careful monitoring required |
| **CONTRAINDICATED** | Dangerous combination, avoid use | Do not use unless absolutely necessary with expert supervision |

## Confidence Levels

The analysis includes a confidence level indicating the strength of evidence:

| Level | Meaning |
|-------|---------|
| **HIGH** | Strong clinical evidence from multiple studies or guidelines |
| **MODERATE** | Moderate evidence from clinical studies |
| **LOW** | Limited evidence; more research needed |

## Key Features

### 1. Analysis
- Examines multiple dimensions of drug-disease interactions
- Considers patient demographics and comorbidities
- Integrates clinical guidelines and evidence

### 2. Clinical Guidance
- Provides actionable management recommendations
- Identifies monitoring requirements
- Suggests dosage adjustments when needed

### 3. Patient Education
- Generates simple, understandable summaries
- Lists signs of problems to watch for
- Provides guidance on when to seek medical help

### 4. Flexible Output
- Console formatting with color coding
- JSON export for integration with other systems
- Stdout output for automation and scripting

### 5. Logging and Verbosity
- Detailed logging for troubleshooting
- Verbose mode for comprehensive operation tracking
- Structured logging with timestamps

## Common Use Cases

### 1. Pre-Prescription Review
Check for interactions before prescribing a new medication:
```bash
python drug_disease_interaction_cli.py "ACE Inhibitor" "Diabetes" --age 65
```

### 2. Comorbidity Assessment
Understand how multiple conditions affect drug safety:
```bash
python drug_disease_interaction_cli.py "Statin" "Liver Disease" --severity moderate
```

### 3. Clinical Decision Support
Support clinical decisions during patient consultations:
```bash
python drug_disease_interaction_cli.py "Beta Blocker" "Asthma" --verbosity 3
```

### 4. Patient Counseling
Generate patient-friendly information (included in standard output):
```bash
python drug_disease_interaction_cli.py "Warfarin" "Kidney Disease"
```

### 5. Integration with Workflows
Export results for integration with medical records systems:
```bash
python drug_disease_interaction_cli.py "Medication" "Condition" \
  --output-dir results \
  --structured
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Medicine name cannot be empty` | Missing medicine name | Provide a valid medicine name |
| `Condition name cannot be empty` | Missing condition name | Provide a valid condition name |
| `Only one medicine can be analyzed...` | Multiple medicines provided | Provide only one medicine name (no commas or "and") |
| `Only one condition can be analyzed...` | Multiple conditions provided | Provide only one condition name (no commas or "and") |
| `Age must be between 0 and 150 years` | Invalid age value | Enter a realistic age between 0-150 |
| `Invalid prompt style` | Wrong prompt style option | Use: `detailed`, `concise`, or `balanced` |
| `Error analyzing disease interaction` | API or network issue | Check internet connection; review logs with `-v` flag |

### Debugging

Enable verbose logging to troubleshoot issues:
```bash
python drug_disease_interaction_cli.py "Medicine" "Condition" --verbosity 4
```

This displays detailed information about:
- Configuration settings
- API calls and responses
- Data processing steps
- Any errors or warnings

## Data Caching

The tool caches analysis results to improve performance. Cache settings can be configured through the `DrugDiseaseInteractionConfig` class:

- **db_path**: Location of the cache database (default: `storage/drug_disease_interaction.lmdb`)
- **db_capacity_mb**: Maximum cache size in MB (default: 500 MB)
- **db_store**: Enable/disable caching (default: enabled)
- **db_overwrite**: Force refresh cache for a query (default: disabled)

## Python API Usage

### Basic Analysis
```python
from lite.config import ModelConfig
from drug_disease_interaction import DrugDiseaseInteraction, DrugDiseaseInput, PromptStyle

# Configure Model
model_config = ModelConfig(model="ollama/gemma3", temperature=0.2)

# Initialize Analyzer
analyzer = DrugDiseaseInteraction(model_config)

# Prepare Input
input_config = DrugDiseaseInput(
    medicine_name="Metformin",
    condition_name="Kidney Disease",
    prompt_style=PromptStyle.DETAILED
)

# Analyze
result = analyzer.generate_text(input_config, structured=True)

# Access results
if result.data and result.data.interaction_details:
    print(f"Severity: {result.data.interaction_details.overall_severity}")
    print(f"Efficacy Impact: {result.data.interaction_details.efficacy_impact}")
    print(f"Safety Impact: {result.data.interaction_details.safety_impact}")
```

### With Additional Context
```python
input_config = DrugDiseaseInput(
    medicine_name="Warfarin",
    condition_name="Liver Disease",
    condition_severity="severe",
    age=72,
    other_medications="Aspirin, Atorvastatin",
    prompt_style=PromptStyle.DETAILED
)
result = analyzer.generate_text(input_config, structured=True)
```

## Output Location

Results are saved to the `outputs/` directory by default:
```
outputs/
├── metformin_kidney_disease_interaction.json
├── warfarin_liver_disease_interaction.json
└── lisinopril_hypertension_interaction.json
```

Specify a custom directory with the `--output-dir` flag:
```bash
python drug_disease_interaction_cli.py "Medicine" "Condition" \
  --output-dir /path/to/custom_directory
```

## Data Sources

The analysis draws from multiple clinical data sources:

- **Clinical Guidelines**: Established medical guidelines (ACCP, AHA, etc.)
- **FDA Labels**: Official drug labeling information
- **Literature**: Peer-reviewed clinical studies
- **Expert Consensus**: Clinical expert consensus documents

Each result includes the data source type used for the analysis.

## Important Notes

### Disclaimer
This tool is designed as a **clinical decision support tool**, not a replacement for professional medical judgment. Always consult with qualified healthcare professionals before making prescribing decisions.

### Accuracy Considerations
- The quality of results depends on the accuracy of input information
- Provide as much clinical context as possible (age, severity, other medications)
- Always verify results against current clinical guidelines and patient-specific factors

### Input Guidelines
- Use standard drug names (generic names are preferred).
- Use recognized medical condition names.
- **Single Item Only**: Provide exactly one medicine and one condition. Do not use commas or "and" to list multiple items.
- Provide realistic age values for personalized recommendations.
- List other medications that might interact in the `--medications` field, not the primary medicine field.

## Getting Help

For issues or questions:
- Run with `--verbosity 4` flag to see detailed logs
- Check that input medicine and condition names are valid
- Verify internet connection for API calls
- Review output JSON for detailed analysis data

## See Also

- Drug Interaction Models: `drug_disease_interaction_models.py`
- MedKit Documentation: See MedKit core client documentation
- Clinical Guidelines: Refer to ACCP, AHA, and FDA resources
