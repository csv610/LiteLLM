# Synthetic Case Report Generator

A command-line tool that generates comprehensive, realistic synthetic medical case reports using structured language model prompting following CARE Guidelines standards.

## Overview

The Synthetic Case Report Generator creates detailed medical case narratives including patient demographics, clinical findings, diagnostic workup, therapeutic interventions, outcomes, and clinical discussion. The tool uses a large language model guided by system prompts designed to produce clinically accurate, educationally valuable synthetic case reports that follow standard case report structure and medical documentation practices.

## Important Medical Disclaimers

**This tool generates SYNTHETIC (not real) medical case reports for educational, training, and research purposes only.** It is not a substitute for real clinical experience, actual patient data, or professional medical judgment. Users should:

- Understand that all generated cases are fictional and created by an AI model
- Never use synthetic cases as a basis for actual clinical decision-making
- Recognize that LLM-generated content may contain inaccuracies, inconsistencies, or medically implausible scenarios
- Verify clinical concepts and information with authoritative medical sources and literature
- Consult with clinical educators and experienced practitioners when using for training
- Be aware that synthetic cases cannot capture the full complexity of real patient presentations
- Follow institutional review board (IRB) and ethical guidelines when using for research
- Clearly label all synthetic cases as "synthetic" or "simulated" to prevent confusion with real patient data
- Never include or mix synthetic cases with real patient data in medical records or databases
- Understand limitations in representing diverse patient populations and rare conditions

The information generated reflects the training data and methodology of the underlying language model and should be considered as educational simulation material only, not as clinically validated case reports.

## Installation

### Requirements

- Python 3.8+
- LiteClient and related dependencies from the parent project
- Rich library for formatted console output

### Setup

```bash
cd synthetic_case_report
pip install -r requirements.txt
```

## Usage

### Basic Command

Generate a synthetic case report for a medical condition:

```bash
python synthetic_case_report_cli.py -i "myocardial infarction"
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--condition` | `-i` | **Required.** Disease or medical condition name | — |
| `--output` | `-o` | Path to save output JSON file | Auto-generated |
| `--output-dir` | `-d` | Directory for output files | `outputs` |
| `--model` | `-m` | Language model to use | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0-4) | `2` |

### Examples

Generate a case report and save to specific file:
```bash
python synthetic_case_report_cli.py -i "pneumonia" -o pneumonia_case.json
```

Use a different model:
```bash
python synthetic_case_report_cli.py -i "diabetes mellitus type 2" -m "ollama/llama2"
```

Increase logging verbosity for debugging:
```bash
python synthetic_case_report_cli.py -i "acute appendicitis" -v 4
```

Save to a custom directory:
```bash
python synthetic_case_report_cli.py -i "stroke" -d /path/to/case_reports
```

Generate multiple case reports for different conditions:
```bash
python synthetic_case_report_cli.py -i "asthma exacerbation" -d outputs/respiratory
python synthetic_case_report_cli.py -i "atrial fibrillation" -d outputs/cardiac
python synthetic_case_report_cli.py -i "acute kidney injury" -d outputs/renal
```

## Features

- **Comprehensive Case Reports**: Generates detailed synthetic cases following CARE Guidelines structure
- **Structured Output**: Results returned as `SyntheticCaseReport` objects with standardized fields
- **CARE Guidelines Compliant**: Follows international case report standards for medical documentation
- **Realistic Patient Narratives**: Creates coherent, clinically plausible patient presentations
- **Complete Clinical Timeline**: Tracks disease progression from onset through treatment and outcomes
- **Diagnostic Reasoning**: Includes diagnostic workup, challenges, and clinical decision-making processes
- **Treatment Documentation**: Details therapeutic interventions, responses, and adjustments
- **Educational Discussion**: Provides learning points, clinical pearls, and practice implications
- **Patient Perspective**: Includes patient experience and psychosocial factors
- **JSON Export**: Save cases for training databases, educational materials, or research
- **Formatted Console Output**: Results displayed in organized panels using Rich for readability
- **Configurable Logging**: Multiple verbosity levels for debugging and production use
- **System Prompting**: Uses role-based prompts to guide clinically accurate case generation

## Code Architecture

### Core Components

**`SyntheticCaseReportGenerator`** - Main class for case report generation
- Initializes with language model configuration
- Validates condition inputs
- Generates comprehensive synthetic case reports
- Handles file output and logging

**Prompt Functions**
- `create_system_prompt()`: Defines the LLM's role as an expert medical case report writer
- `create_user_prompt(condition)`: Creates structured queries requesting specific case report components

**Output Functions**
- `save()`: Exports results to JSON files with proper directory creation

**CLI Entry Point**
- `app_cli()`: Handles argument parsing, logging configuration, and orchestrates the generation workflow
- `get_user_arguments()`: Parses command-line arguments with validation

## Output Format

The tool generates a `SyntheticCaseReport` object following CARE Guidelines (see `synthetic_case_report_models.py` for complete schema):

```json
{
  "metadata": {
    "case_report_title": "Descriptive title of clinical presentation",
    "keywords": "Clinical keywords describing findings/presentations",
    "medical_specialty": "Primary medical specialty",
    "date_case_compiled": "Date of compilation",
    "case_authors": "Author names (fictional)",
    "institution": "Medical institution name",
    "information_sources": "Sources of medical information",
    "confidence_level": "Realism confidence rating",
    "clinical_accuracy": "Note on clinical accuracy",
    "bias_mitigation_note": "Note on diagnosis withholding"
  },
  "patient_information": {
    "age": "Patient age in years",
    "gender": "Patient gender",
    "ethnicity": "Patient ethnicity",
    "occupation": "Patient occupation",
    "relevant_family_history": "Relevant family history",
    "past_medical_history": "Previous medical conditions",
    "surgical_history": "Previous surgeries",
    "medication_history": "Current medications",
    "allergy_history": "Known allergies",
    "social_history": "Smoking, alcohol, living situation"
  },
  "clinical_findings": {
    "chief_complaint": "Primary reason for presentation",
    "history_of_present_illness": "Detailed chronological illness description",
    "symptom_onset": "When symptoms started",
    "symptom_progression": "How symptoms evolved",
    "associated_symptoms": "Related symptoms",
    "alleviating_factors": "What improves symptoms",
    "aggravating_factors": "What worsens symptoms",
    "impact_on_activities": "Effect on daily life",
    "physical_exam_findings": "Physical examination results",
    "abnormal_findings": "Specific abnormal findings"
  },
  "timeline": {
    "initial_presentation_date": "Date of first symptoms",
    "key_clinical_events": "Major events chronologically",
    "diagnostic_workup_timeline": "Sequence of diagnostic tests",
    "treatment_initiation_date": "When treatment began",
    "significant_changes": "Important status changes",
    "duration_of_illness": "Total time from onset"
  },
  "diagnostic_assessment": {
    "laboratory_tests_performed": "Lab tests and results",
    "laboratory_values": "Abnormal lab values",
    "imaging_studies": "Imaging performed",
    "imaging_findings": "Abnormal imaging findings",
    "pathology_results": "Tissue diagnosis",
    "specialized_testing": "EKG, EEG, genetic tests, etc.",
    "diagnostic_criteria_assessment": "Clinical criteria findings",
    "diagnostic_challenges": "Difficulties in diagnosis",
    "noteworthy_findings_pattern": "Overall findings pattern"
  },
  "therapeutic_interventions": {
    "initial_management": "First-line treatment approach",
    "medications_prescribed": "Medications with dosages",
    "dosage_adjustments": "Medication dose changes",
    "surgical_interventions": "Surgical procedures performed",
    "procedural_interventions": "Non-surgical procedures",
    "supportive_care": "Supportive measures",
    "lifestyle_modifications": "Dietary/activity changes",
    "rehabilitation_therapy": "Physical/occupational therapy",
    "adverse_events": "Treatment complications",
    "treatment_response": "Response to treatment"
  },
  "follow_up_and_outcomes": {
    "clinical_response_to_treatment": "Symptom improvement",
    "symptom_resolution": "Whether symptoms resolved",
    "functional_status": "Ability to perform activities",
    "final_clinical_status": "Current health status",
    "complications_during_course": "Any complications",
    "length_of_hospital_stay": "Hospital duration",
    "duration_of_followup": "Follow-up period length",
    "discharge_medications": "Medications at discharge",
    "followup_schedule": "Planned follow-up",
    "current_status": "Most recent assessment"
  },
  "discussion": {
    "case_significance": "Why case is important",
    "findings_interpretation": "Analysis of findings",
    "diagnostic_approach_discussion": "Diagnostic strategy analysis",
    "treatment_rationale": "Why treatments were chosen",
    "treatment_effectiveness": "Assessment of response",
    "learning_points": "Key clinical lessons",
    "pathophysiological_insights": "Biological mechanisms",
    "clinical_pearls": "Important observations",
    "implications_for_practice": "How case informs practice",
    "recommendations": "Recommendations for similar cases"
  },
  "patient_perspective": {
    "patient_experience": "How patient experienced illness",
    "understanding_of_diagnosis": "Patient comprehension",
    "treatment_satisfaction": "Satisfaction with care",
    "quality_of_life_impact": "Impact on quality of life",
    "adherence_to_treatment": "Treatment adherence",
    "psychosocial_factors": "Emotional/social aspects"
  },
  "informed_consent": {
    "consent_statement": "Consent obtained statement",
    "patient_anonymity": "Anonymization confirmation",
    "institutional_approval": "IRB approval status",
    "ethical_considerations": "Ethical issues"
  }
}
```

## Logging

Logs are written to `synthetic_case_report.log` in the working directory.

Verbosity levels:
- `0`: CRITICAL only
- `1`: ERROR messages
- `2`: WARNING messages (default)
- `3`: INFO messages
- `4`: DEBUG messages (verbose)

## Use Cases

### Medical Education
- Creating training materials for medical students and residents
- Developing clinical reasoning exercises and case-based learning modules
- Building practice case libraries for examination preparation
- Simulating rare or complex clinical presentations for educational purposes

### Clinical Research
- Generating synthetic datasets for algorithm development and testing
- Creating control cases for research study design
- Developing case-based research protocols
- Testing clinical decision support systems

### Healthcare Technology
- Populating electronic health record (EHR) systems for testing
- Training natural language processing models on medical text
- Developing clinical documentation tools and templates
- Testing medical information systems with realistic case data

### Quality Improvement
- Creating standardized case scenarios for quality audits
- Developing performance assessment tools for clinicians
- Building case libraries for peer review exercises
- Simulating patient cases for workflow optimization

## Limitations

1. **Synthetic Nature**: All cases are AI-generated and do not represent real patients
2. **Clinical Accuracy**: May contain medically implausible combinations or inaccuracies
3. **Model Dependency**: Quality depends on the underlying language model's training data
4. **Knowledge Cutoff**: LLM training data has a cutoff date; recent medical advances may not be included
5. **Lack of Clinical Validation**: Generated cases are not reviewed by medical experts
6. **Population Representation**: May not accurately represent diverse patient populations
7. **Rare Conditions**: Complex or rare conditions may have less accurate representations
8. **Cultural Context**: May lack nuanced cultural or regional medical practice variations
9. **Inconsistencies**: May occasionally generate contradictory information within a case
10. **Diagnostic Bias**: Despite mitigation efforts, may reflect biases present in training data
11. **Liability**: Cannot be used for actual clinical decision-making or patient care
12. **Privacy Concerns**: While synthetic, must be clearly labeled to prevent confusion with real data

## Best Practices

### For Educational Use
- Clearly label all cases as "synthetic" or "simulated"
- Review generated cases with clinical educators before use in curricula
- Use cases as starting points for discussion, not definitive clinical examples
- Combine with real case experiences and clinical guidelines
- Verify medical facts and concepts with authoritative sources
- Adapt cases to match learning objectives and student level

### For Research Use
- Never mix synthetic cases with real patient data
- Document generation parameters (model, date, prompts) for reproducibility
- Consider validation by clinical experts when accuracy is critical
- Use appropriate sample sizes and recognize synthetic data limitations
- Follow ethical guidelines for synthetic data use in research
- Disclose synthetic data use in publications and reports

### For System Testing
- Generate diverse cases covering edge cases and common presentations
- Validate system behavior with both synthetic and real (de-identified) data
- Use cases to test error handling and boundary conditions
- Maintain separate databases for synthetic and real patient data
- Document test case origins clearly in system documentation

### General Recommendations
- Regularly update cases as medical knowledge evolves
- Keep records of generation dates and model versions
- Report any medically dangerous or inappropriate generated content
- Use cases as supplements to, not replacements for, real clinical experience
- Follow institutional policies on synthetic data use
- Provide feedback on case quality to improve future generations

## Related Files

- `synthetic_case_report_models.py` - Pydantic models for structured case reports following CARE Guidelines
- `synthetic_case_report.log` - Log file (auto-generated)
- `outputs/` - Default directory for generated case reports (auto-created)

## References

- CARE Guidelines (Case Reports): Standard framework for case report structure
- Medical case report writing principles and best practices
- HIPAA guidelines on synthetic data and de-identification

## License

See parent project LICENSE file.
