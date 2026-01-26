# Mental Health Module

Mental health assessment, screening, and reporting tools.

## Overview

The Mental Health Module provides tools for conducting mental health assessments, screening for common mental health conditions (depression, anxiety), generating mental health reports, and supporting symptom detection through chat interfaces.

## Module Components

```
mental_health/
├── mental_health_assessment.py      # Main assessment logic
├── mental_health_report.py          # Report generation
├── mental_health_chat.py            # Chat interface
├── mental_health_chat_app.py        # Interactive app
├── mental_health_assessment_models.py # Data models
└── sympton_detection_chat.py        # Symptom detection
```

## Key Features

### 1. Mental Health Assessment
Comprehensive assessment tools including:
- PHQ-9 (Patient Health Questionnaire-9) for depression
- GAD-7 (Generalized Anxiety Disorder-7) for anxiety
- Custom assessment protocols
- Structured evaluation

**Command**:
```bash
python -m medkit mental_health assessment --patient-id <id>
```

### 2. Mental Health Reporting
Generate comprehensive mental health reports:
- Assessment summaries
- Clinical findings
- Risk assessment
- Recommendations
- Treatment suggestions

**Command**:
```bash
python -m medkit mental_health report --patient-id <id>
```

### 3. Chat-Based Assessment
Interactive chat interface for assessment:
- Natural conversation flow
- Adaptive questioning
- Real-time feedback
- Engagement-focused design

**Command**:
```bash
python -m medkit mental_health chat --patient-id <id>
```

### 4. Symptom Detection
Detect mental health symptoms through chat:
- Natural language processing
- Symptom identification
- Pattern recognition
- Risk assessment

## Usage Examples

### Example 1: Basic Assessment

```bash
python -m medkit mental_health assessment --patient-id P001
```

### Example 2: Generate Report

```bash
python -m medkit mental_health report --patient-id P001 \
  --output mental_health_report_P001.json
```

### Example 3: Chat Assessment

```bash
python -m medkit mental_health chat --patient-id P001
```

### Example 4: Batch Assessment

```bash
for patient_id in P001 P002 P003; do
  python -m medkit mental_health assessment --patient-id "$patient_id" \
    --output "assessment_${patient_id}.json"

  python -m medkit mental_health report --patient-id "$patient_id" \
    --output "report_${patient_id}.json"
done
```

## Python API Usage

### Mental Health Assessment

```python
from mental_health.mental_health_assessment import MentalHealthAssessment

assessment = MentalHealthAssessment()
result = assessment.conduct_assessment(patient_id="P001")

print(f"Patient: {result.patient_id}")
print(f"Depression Score: {result.phq9_score}")
print(f"Anxiety Score: {result.gad7_score}")
print(f"Risk Level: {result.risk_level}")
```

### Mental Health Report

```python
from mental_health.mental_health_report import MentalHealthReport

report = MentalHealthReport()
result = report.generate_report(patient_id="P001")

print(f"Patient: {result.patient_id}")
print(f"Summary: {result.summary}")
print(f"Recommendations: {result.recommendations}")
```

### Chat-Based Assessment

```python
from mental_health.mental_health_chat import MentalHealthChat

chat = MentalHealthChat()
result = chat.conduct_chat_assessment(patient_id="P001")

print(f"Detected Symptoms: {result.symptoms}")
print(f"Conversation Summary: {result.summary}")
```

## Screening Tools

### PHQ-9 (Depression Screening)

Measures depression severity:
- **Scores**: 0-27
- **Interpretation**:
  - 0-4: No depression
  - 5-9: Mild
  - 10-14: Moderate
  - 15-19: Moderately severe
  - 20-27: Severe

### GAD-7 (Anxiety Screening)

Measures anxiety severity:
- **Scores**: 0-21
- **Interpretation**:
  - 0-4: No anxiety
  - 5-9: Mild
  - 10-14: Moderate
  - 15-21: Severe

## Configuration

### Environment Variables

```bash
export MEDKIT_MODEL=ollama/gemma3
export MEDKIT_OUTPUT_DIR=/path/to/outputs
export MEDKIT_LOG_LEVEL=INFO
```

### Command Options

All mental health commands support:

| Option | Description |
|--------|-------------|
| `--patient-id` | Patient identifier (Required) |
| `--assessment-type` | Type of assessment |
| `--output` | Save to file |
| `--model` | LLM model |
| `-v, --verbosity` | Log level (0-4) |

## Data Models

### MentalHealthAssessment

```python
from mental_health.mental_health_assessment_models import MentalHealthAssessment

class AssessmentResult(BaseModel):
    patient_id: str                    # Patient ID
    assessment_date: str               # Assessment date
    phq9_score: Optional[int]          # PHQ-9 score
    gad7_score: Optional[int]          # GAD-7 score
    overall_risk: str                  # Risk level
    findings: List[str]                # Key findings
    recommendations: List[str]         # Recommendations
```

## Common Use Cases

### Use Case 1: Mental Health Screening Protocol

```python
from mental_health.mental_health_assessment import MentalHealthAssessment
from mental_health.mental_health_report import MentalHealthReport

def mental_health_screening(patient_id):
    """Complete mental health screening protocol."""

    # Conduct assessment
    assessment = MentalHealthAssessment()
    assessment_result = assessment.conduct_assessment(patient_id)

    # Generate report
    report = MentalHealthReport()
    report_result = report.generate_report(patient_id)

    return {
        'assessment': assessment_result,
        'report': report_result
    }

results = mental_health_screening("P001")
```

### Use Case 2: Batch Patient Screening

```bash
#!/bin/bash
# Screen multiple patients

for patient_id in $(cat patient_list.txt); do
  echo "Screening $patient_id..."

  python -m medkit mental_health assessment --patient-id "$patient_id" \
    --output "assessment_${patient_id}.json"

  python -m medkit mental_health report --patient-id "$patient_id" \
    --output "report_${patient_id}.json"
done
```

### Use Case 3: Chat-Based Initial Assessment

```python
from mental_health.mental_health_chat import MentalHealthChat

def interactive_assessment(patient_id):
    """Conduct interactive chat-based assessment."""
    chat = MentalHealthChat()
    result = chat.conduct_chat_assessment(patient_id)

    return {
        'patient_id': patient_id,
        'symptoms': result.symptoms,
        'risk_level': result.risk_level,
        'summary': result.conversation_summary
    }
```

## Important Clinical Notes

### Depression (PHQ-9)

- **Purpose**: Screening for major depressive disorder
- **Administration**: Typically administered by healthcare provider
- **Scoring**: Each item 0-3 points
- **Interpretation**: See score ranges above
- **Limitations**: Screening tool, not diagnostic

### Anxiety (GAD-7)

- **Purpose**: Screening for generalized anxiety disorder
- **Administration**: Self-report or clinician-administered
- **Scoring**: Each item 0-3 points
- **Interpretation**: See score ranges above
- **Limitations**: Screening tool, not diagnostic

## Risk Assessment

The module includes risk assessment capabilities:
- Suicide risk screening
- Self-harm risk
- Danger to others assessment
- Crisis indicators

**Important**: High-risk patients require immediate professional intervention.

## Limitations

1. **Screening Only**: Not diagnostic instruments
2. **AI-Based**: Conducted by LLM, not trained clinician
3. **Self-Report**: Relies on patient responses
4. **Context**: May miss important contextual factors
5. **Privacy**: Sensitive mental health information
6. **Cultural**: May not account for cultural factors

## Best Practices

1. **Professional Review**: Results reviewed by mental health professional
2. **Context**: Interpret within full clinical context
3. **Follow-up**: Use as basis for further evaluation
4. **Confidentiality**: Protect sensitive mental health data
5. **Training**: Proper training for assessment administration
6. **Documentation**: Maintain complete assessment records

## Important Disclaimers

**This module is for screening and assessment purposes only.** It is not:
- A clinical diagnosis
- Treatment
- A substitute for professional evaluation
- Adequate for crisis situations

Users must:
- Consult mental health professionals for all results
- Not use for clinical decision-making without professional review
- Understand assessment limitations
- Follow privacy and confidentiality guidelines
- Seek immediate help for crisis situations
- Report results to healthcare providers

## Crisis Resources

If you or someone you know is in crisis:
- **National Suicide Prevention Lifeline**: 988 (US)
- **Crisis Text Line**: Text HOME to 741741
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

## Related Modules

- [phyexams/](../phyexams/) - Physical examinations
- [medical/](../medical/) - Medical information
- [drug/](../drug/) - Pharmaceutical information
- [diagnostics/](../diagnostics/) - Medical tests

## Support

For help:
1. See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
2. Check [CLI_REFERENCE.md](../CLI_REFERENCE.md)
3. Review [API.md](../API.md)
4. Read [FAQ.md](../FAQ.md)

## References

- DSM-5 (Diagnostic and Statistical Manual)
- PHQ-9 Patient Health Questionnaire
- GAD-7 Generalized Anxiety Disorder Scale
- SAMHSA Mental Health Resources

---

**Last Updated**: January 25, 2026
**Related**: [README.md](../README.md) | [ARCHITECTURE.md](../ARCHITECTURE.md) | [CLI_REFERENCE.md](../CLI_REFERENCE.md)
