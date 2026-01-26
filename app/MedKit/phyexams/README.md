# Physical Exams Module

26+ specialized physical examination and assessment tools.

## Overview

The Physical Exams Module provides structured examination tools covering all major body systems and specialized assessments including mental health screening, cognitive testing, and physical examinations.

## Available Exams (26+)

### Mental Health & Cognitive Assessment

- **exam_depression_screening** - PHQ-9 Depression Screening
- **exam_anxiety_screening** - GAD-7 Anxiety Screening
- **exam_emotional_stability** - Emotional Stability Assessment
- **exam_judgement** - Judgment Assessment
- **exam_abstract_reasoning** - Abstract Reasoning Test
- **exam_arithmetic_calculation** - Arithmetic Calculation Test
- **exam_memory_ability** - Memory and Cognition Test
- **exam_attention_span** - Attention and Concentration Test
- **exam_writing_ability** - Writing Ability Assessment

### Physical Examinations

- **exam_head_and_neck** - Head and Neck Examination
- **exam_blood_vessels** - Blood Vessels Examination
- **exam_lymphatic_system** - Lymphatic System Examination
- **exam_breast_axillae** - Breast and Axillae Examination
- **exam_musculoskeletal** - Musculoskeletal Examination
- **exam_musculoskeletal_core** - Core Musculoskeletal Assessment
- **exam_skin_hair_nails** - Skin, Hair, and Nails Examination

### System-Specific Examinations

- **exam_nutrition_growth** - Nutrition and Growth Assessment
- **exam_anal_rectum_prostate** - Anal/Rectal/Prostate Examination
- **exam_ears_nose_throat** - ENT Examination
- **exam_female_genitalia** - Female Genitalia Examination
- **exam_male_genitalia** - Male Genitalia Examination
- **exam_heart** - Cardiac Examination
- **exam_lungs_chest** - Lung and Chest Examination
- **exam_neurology_system** - Neurological Examination

## Usage

### Basic Command

```bash
python -m medkit phyexams exam_<exam_type> --patient-id <patient_id>
```

### Common Options

All exam commands support:

| Option | Description | Example |
|--------|-------------|---------|
| `--patient-id` | Patient identifier (Required) | `--patient-id P001` |
| `--output` | Save to file | `--output exam_result.json` |
| `--model` | LLM model | `--model ollama/mistral` |
| `-v, --verbosity` | Log level (0-4) | `-v 4` |

## Examples

### Example 1: Depression Screening

```bash
python -m medkit phyexams exam_depression_screening --patient-id P001 \
  --output depression_screening.json
```

### Example 2: Musculoskeletal Exam

```bash
python -m medkit phyexams exam_musculoskeletal --patient-id P001 \
  --output musculoskeletal_exam.json
```

### Example 3: Head and Neck Exam

```bash
python -m medkit phyexams exam_head_and_neck --patient-id P001 \
  --output head_neck_exam.json
```

### Example 4: Memory Test

```bash
python -m medkit phyexams exam_memory_ability --patient-id P001 \
  --output memory_test.json
```

### Example 5: Nutrition Assessment

```bash
python -m medkit phyexams exam_nutrition_growth --patient-id P001 \
  --output nutrition_assessment.json
```

## Python API Usage

### Basic Exam Conduction

```python
from phyexams.exam_depression_screening import DepressionScreening

exam = DepressionScreening()
result = exam.conduct_exam(patient_id="P001")
```

### Multiple Exams

```python
from phyexams.exam_depression_screening import DepressionScreening
from phyexams.exam_memory_ability import MemoryAbility
from phyexams.exam_musculoskeletal import MusculoskeletalExam

patient_id = "P001"
results = {}

# Depression screening
depression_exam = DepressionScreening()
results['depression'] = depression_exam.conduct_exam(patient_id)

# Memory test
memory_exam = MemoryAbility()
results['memory'] = memory_exam.conduct_exam(patient_id)

# Musculoskeletal exam
msk_exam = MusculoskeletalExam()
results['musculoskeletal'] = msk_exam.conduct_exam(patient_id)

print(results)
```

## Exam Specifications

See `exam_specifications.py` for comprehensive exam definitions including:
- Questions and prompts
- Scoring criteria
- Interpretation guidelines
- Cutoff values
- Reference ranges

```python
from phyexams.exam_specifications import ExamSpecifications

specs = ExamSpecifications()
phq9_definition = specs.get_exam_definition('PHQ9')
```

## Configuration

### Environment Variables

```bash
export MEDKIT_MODEL=ollama/gemma3
export MEDKIT_OUTPUT_DIR=/path/to/outputs
export MEDKIT_LOG_LEVEL=INFO
```

## Common Use Cases

### Use Case 1: Comprehensive Patient Assessment

```bash
#!/bin/bash
PATIENT_ID=$1

mkdir -p "assessments_${PATIENT_ID}"

# Run multiple exams
python -m medkit phyexams exam_depression_screening --patient-id "$PATIENT_ID" \
  --output "assessments_${PATIENT_ID}/depression.json"

python -m medkit phyexams exam_musculoskeletal --patient-id "$PATIENT_ID" \
  --output "assessments_${PATIENT_ID}/musculoskeletal.json"

python -m medkit phyexams exam_head_and_neck --patient-id "$PATIENT_ID" \
  --output "assessments_${PATIENT_ID}/head_neck.json"

python -m medkit phyexams exam_memory_ability --patient-id "$PATIENT_ID" \
  --output "assessments_${PATIENT_ID}/memory.json"

echo "Assessment complete for $PATIENT_ID"
```

### Use Case 2: Batch Patient Screening

```bash
# Screen multiple patients for depression
for patient_id in P001 P002 P003 P004 P005; do
  python -m medkit phyexams exam_depression_screening \
    --patient-id "$patient_id" \
    --output "screening_${patient_id}.json"
done
```

### Use Case 3: Focused Examination Protocol

```python
# Create examination protocol for specific condition
from phyexams.exam_depression_screening import DepressionScreening
from phyexams.exam_anxiety_screening import AnxietyScreening
from phyexams.exam_memory_ability import MemoryAbility

def mental_health_protocol(patient_id):
    """Run mental health screening protocol."""
    results = {}

    # Depression
    depr = DepressionScreening()
    results['depression'] = depr.conduct_exam(patient_id)

    # Anxiety
    anx = AnxietyScreening()
    results['anxiety'] = anx.conduct_exam(patient_id)

    # Cognition
    mem = MemoryAbility()
    results['memory'] = mem.conduct_exam(patient_id)

    return results

results = mental_health_protocol("P001")
```

## Exam Categories

### Screening Exams
Quick assessment tools for detecting conditions:
- Depression (PHQ-9)
- Anxiety (GAD-7)
- Other screening tools

### Assessment Exams
Comprehensive evaluation tools:
- Cognitive assessments
- Functional assessments
- Specialized evaluations

### Physical Exams
Clinical examination procedures:
- System-based exams
- Organ-specific exams
- Regional exams

## Important Clinical Notes

1. **Not Diagnostic**: These exams are for assessment only, not diagnosis
2. **Professional Review**: Results should be reviewed by healthcare professionals
3. **Contextual**: Interpret results in context of full clinical picture
4. **Limitations**: LLM-based assessments have inherent limitations
5. **Training**: Proper training needed for accurate administration
6. **Standardization**: Follow exam protocols for consistency

## Data Output

All exams produce structured output including:
- Patient information
- Exam date/time
- Questions and responses
- Scoring
- Interpretation
- Clinical recommendations

## Limitations

1. **AI-Generated**: Conducted by LLM, not human examiner
2. **Standardization**: Cannot fully replicate human clinical exam
3. **Context**: May miss important contextual information
4. **Physical**: Cannot assess physical findings (only through reported information)
5. **Interaction**: Limited ability to probe or follow-up

## Best Practices

1. **Use as Screening**: For initial screening and assessment
2. **Professional Review**: Always have results reviewed by professionals
3. **Follow-up**: Use as basis for further clinical evaluation
4. **Documentation**: Maintain complete documentation
5. **Consent**: Ensure informed consent for assessments
6. **Privacy**: Protect patient information and privacy

## Important Disclaimers

**These exams are for educational and screening purposes only.** They are not:
- Clinical diagnoses
- Substitutes for professional evaluation
- Binding assessments
- Replacements for healthcare provider judgment

Users must:
- Consult qualified healthcare professionals
- Not use for clinical decision-making without professional review
- Understand LLM limitations
- Maintain patient confidentiality
- Follow institutional guidelines

## Related Modules

- [mental_health/](../mental_health/) - Mental health assessment
- [medical/](../medical/) - Medical information
- [drug/](../drug/) - Pharmaceutical information
- [diagnostics/](../diagnostics/) - Medical tests and devices

## Support

For help:
1. See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
2. Check [CLI_REFERENCE.md](../CLI_REFERENCE.md)
3. Review [API.md](../API.md)
4. Read [FAQ.md](../FAQ.md)

---

**Last Updated**: January 25, 2026
**Related**: [README.md](../README.md) | [ARCHITECTURE.md](../ARCHITECTURE.md) | [CLI_REFERENCE.md](../CLI_REFERENCE.md)
