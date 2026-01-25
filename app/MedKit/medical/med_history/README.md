# Patient Medical History Generator

A tool for generating comprehensive, exam-specific patient medical history questions. This module uses AI to create trauma-informed, clinically relevant questions tailored to specific medical examinations and clinical purposes.

## Overview

The Patient Medical History Generator creates structured sets of medical history questions based on:
- **Exam Type**: The specific medical examination (e.g., cardiac, respiratory, gastrointestinal)
- **Patient Demographics**: Age and gender
- **Clinical Purpose**: The intended use of the history (surgery prep, medication review, physical examination)

The generated questions are organized into seven clinical categories and include follow-up questions for positive responses to key clinical indicators.

## Clinical Purpose

Medical history is fundamental to clinical assessment. A comprehensive history helps:
- Identify relevant risk factors and comorbidities
- Detect drug interactions and contraindications
- Assess surgical fitness and anesthesia risk
- Establish baseline health status
- Guide physical examination and diagnostic testing
- Ensure informed consent and patient safety

This tool standardizes the generation of history questions specific to clinical context, ensuring consistent, evidence-based inquiry across examinations.

## Installation

### Prerequisites
- Python 3.8+
- LiteClient (configured for your preferred LLM provider)
- Pydantic
- Rich (for CLI output formatting)

### Setup

```bash
cd patient_medical_history
pip install -r requirements.txt
```

## Usage

### Command Line Interface

#### Basic Usage

```bash
python patient_medical_history_cli.py -e "cardiac" -a 55 -g "male" -p "physical_exam"
```

#### Arguments

| Argument | Short | Type | Required | Default | Description |
|----------|-------|------|----------|---------|-------------|
| `--exam` | `-e` | string | Yes | — | Type of medical exam (e.g., cardiac, respiratory, orthopedic) |
| `--age` | `-a` | integer | Yes | — | Patient age in years (1-150) |
| `--gender` | `-g` | string | Yes | — | Patient gender |
| `--purpose` | `-p` | string | No | physical_exam | Purpose of history collection: `surgery`, `medication`, or `physical_exam` |
| `--model` | `-m` | string | No | gemini-1.5-pro | LLM model to use |
| `--output` | `-o` | path | No | — | Path to save JSON output |

#### Examples

**Pre-operative cardiac exam:**
```bash
python patient_medical_history_cli.py \
  -e "cardiac" \
  -a 62 \
  -g "female" \
  -p "surgery"
```

**Medication review for a pediatric patient:**
```bash
python patient_medical_history_cli.py \
  -e "general" \
  -a 8 \
  -g "male" \
  -p "medication" \
  -o history_output.json
```

**Respiratory exam with custom model:**
```bash
python patient_medical_history_cli.py \
  -e "respiratory" \
  -a 45 \
  -g "female" \
  -p "physical_exam" \
  -m "gpt-4"
```

### Programmatic Usage

```python
from lite.config import ModelConfig
from patient_medical_history_cli import PatientMedicalHistoryGenerator
from patient_medical_history_models import MedicalHistoryInput

# Configure the model
model_config = ModelConfig(model="gemini-1.5-pro", temperature=0.3)
generator = PatientMedicalHistoryGenerator(model_config=model_config)

# Create input
medical_history_input = MedicalHistoryInput(
    exam="cardiac",
    age=55,
    gender="male",
    purpose="physical_exam"
)

# Generate questions
result = generator.generate_text(medical_history_input)

# Print formatted output

# Access specific question categories
past_medical = result.past_medical_history
family_history = result.family_history
medications = result.drug_information.medication_questions
allergies = result.drug_information.allergy_questions
```

## Question Categories

The generator produces questions in seven evidence-based clinical categories:

### 1. Past Medical History
- **Condition Questions**: General medical conditions relevant to the exam
- **Hospitalization Questions**: History of hospitalizations, including reason, frequency, and duration
- **Surgery Questions**: Previous surgical procedures and outcomes

*Clinical relevance*: Identifies comorbidities that affect exam interpretation, surgical risk, or medication interactions.

### 2. Family History
- **Maternal History**: Significant maternal medical conditions
- **Paternal History**: Significant paternal medical conditions
- **Genetic Risk**: Hereditary conditions and genetic predispositions

*Clinical relevance*: Establishes risk for inherited conditions, familial disease patterns, and genetic screening needs.

### 3. Drug Information
- **Medication Questions**: Current medications, dosages, adherence, and side effects
- **Allergy Questions**: Drug allergies, including reaction type and severity
- **Adverse Reaction Questions**: Adverse drug reactions and intolerances

*Clinical relevance*: Critical for drug interaction assessment, dosage adjustment, contraindication identification, and safe prescribing.

### 4. Vaccination History
- **Vaccination Status**: Current immunization status
- **Vaccine-Specific Questions**: Details on specific vaccines (dates, reactions)
- **Booster Questions**: Status of recommended booster immunizations

*Clinical relevance*: Assesses immunity status, guides disease prevention, identifies vaccine-preventable disease risk, and informs infection control measures.

### 5. Lifestyle and Social Factors
- **Lifestyle Questions**: Tobacco use, alcohol consumption, diet, exercise, sleep, stress management
- **Personal/Social Questions**: Occupation, housing, relationships, education, support systems

*Clinical relevance*: Identifies modifiable risk factors, social determinants of health, and psychosocial stressors affecting health outcomes.

### 6. Purpose-Specific Variations

#### Surgery Preparation
When `purpose="surgery"`, questions emphasize:
- Anesthesia risk factors
- Bleeding and hemostasis concerns
- Post-operative recovery factors
- Medication interactions with anesthetic agents
- Cardiopulmonary reserve

#### Medication Review
When `purpose="medication"`, questions emphasize:
- Medication adherence and efficacy
- Allergies and adverse reactions
- Drug-drug and drug-disease interactions
- Over-the-counter and herbal supplement use
- Medication compliance barriers

#### Physical Examination
When `purpose="physical_exam"`, questions emphasize:
- Current symptom assessment
- Functional status
- Review of systems
- Baseline health status
- Examination-specific risk factors

## Output Structure

### JSON Output Format

```json
{
  "exam": "cardiac",
  "age": 55,
  "gender": "male",
  "purpose": "physical_exam",
  "past_medical_history": {
    "condition_questions": [...],
    "hospitalization_questions": [...],
    "surgery_questions": [...]
  },
  "family_history": {
    "maternal_history_questions": [...],
    "paternal_history_questions": [...],
    "genetic_risk_questions": [...]
  },
  "drug_information": {
    "medication_questions": [...],
    "allergy_questions": [...],
    "adverse_reaction_questions": [...]
  },
  "vaccination": {
    "vaccination_status_questions": [...],
    "vaccine_specific_questions": [...],
    "booster_questions": [...]
  },
  "lifestyle_and_social": {
    "lifestyle_questions": [...],
    "personal_social_questions": [...]
  }
}
```

### Question Object Structure

Each question includes:

```json
{
  "question": "Do you have a history of high blood pressure?",
  "clinical_relevance": "Hypertension is a major risk factor for coronary artery disease and may affect surgical outcomes.",
  "requirement": "mandatory",
  "expected_answer_type": "yes/no",
  "follow_up_questions": [
    {
      "question": "When were you diagnosed?",
      "clinical_reason": "Establishes disease duration and chronicity",
      "investigation_focus": "Disease timeline and progression"
    }
  ]
}
```

## Clinical Design Principles

### Trauma-Informed Approach
Questions are designed to be:
- **Respectful**: Acknowledging patient autonomy and dignity
- **Non-judgmental**: Free of moral language regarding lifestyle choices
- **Culturally Sensitive**: Appropriate across diverse populations
- **Clear and Accessible**: Written in plain language with medical terminology explained

### Evidence-Based Selection
Question generation follows principles of:
- Clinical relevance to the specific exam
- Evidence-based risk stratification
- Examination-specific detail levels
- Appropriate follow-up questioning for positive responses

### Systematic Structure
Questions follow a logical progression:
1. General screening within each category
2. Specific probing for positive responses
3. Severity and functional impact assessment
4. Relevant treatment and management details

## Data Models

### MedicalHistoryInput
Input dataclass with required parameters:
- `exam` (str): Type of medical examination
- `age` (int): Patient age (1-150)
- `gender` (str): Patient gender
- `purpose` (str): Clinical purpose - `surgery`, `medication`, or `physical_exam`

### PatientMedicalHistoryQuestions
Output dataclass containing:
- `exam`, `age`, `gender`, `purpose`: Input parameters
- Seven question category objects with lists of specific question types

### HistoryPurpose Enum
Valid values:
- `SURGERY = "surgery"`
- `MEDICATION = "medication"`
- `PHYSICAL_EXAM = "physical_exam"`

## Error Handling

The tool includes validation for:
- **Empty exam name**: Raises ValueError
- **Invalid age**: Must be between 1-150, raises ValueError
- **Invalid purpose**: Must be one of three valid purposes, raises ValueError

## Clinical Considerations

### Appropriate Use
This tool is designed to:
- **Standardize** history-taking across clinical settings
- **Ensure completeness** of relevant clinical inquiry
- **Support** (not replace) clinical judgment
- **Generate starting points** for clinician-patient dialogue

### Not a Substitute for Clinical Practice
This tool:
- Does not replace direct clinician-patient communication
- Does not provide clinical decision support or diagnosis
- Does not substitute for individualized patient assessment
- Should be adapted based on specific clinical context and patient needs

### Clinician Responsibility
Clinicians must:
- Adapt questions to individual patient context
- Follow up on positive responses with appropriate depth
- Integrate history findings with physical exam and testing
- Apply clinical judgment in interpreting findings
- Maintain professional standards of informed consent

## Technical Specifications

- **Language Model**: Uses configurable LLM (default: Gemini 1.5 Pro)
- **Temperature**: Set to 0.3 for focused, consistent output
- **Response Format**: Structured JSON via Pydantic models
- **Output Options**: Console display or JSON file export

## Files

- `patient_medical_history_cli.py`: CLI interface and generator class
- `patient_medical_history_models.py`: Pydantic models and dataclasses
- `README.md`: This documentation

## Limitations and Considerations

1. **LLM Dependency**: Output quality depends on the underlying language model
2. **Specialization**: Question sets are general by exam type; may need clinical customization
3. **Population Variation**: May require adaptation for pediatric, geriatric, or other specific populations
4. **Language**: Currently generates English-language questions
5. **Cultural Adaptation**: Questions should be reviewed for cultural appropriateness in specific populations

## Contributing

To improve the tool:
1. Review generated questions for clinical accuracy
2. Provide feedback on question relevance and comprehensiveness
3. Suggest exam-type-specific additions
4. Report issues with follow-up question generation

## References

Medical history-taking follows standards established by:
- American Medical Association (AMA) documentation guidelines
- Internal Review Board (IRB) informed consent principles
- Evidence-based medicine frameworks for risk assessment
- Trauma-informed care standards

## License

[Specify your project's license]

## Support

For questions or issues, contact the development team or submit an issue to the project repository.
