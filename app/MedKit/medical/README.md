# Medical Module

Medical information system with 18+ specialized modules.

## Overview

The Medical Module provides medical information across major medical specialties including diseases, anatomy, procedures, surgical information, herbal remedies, FAQs, and more.

## Module Structure

```
medical/
├── disease_info/              # Disease information
├── anatomy/                   # Anatomical information
├── med_procedure_info/        # Medical procedures
├── surgical_info/             # Surgical procedures
├── med_speciality/            # Medical specialties
├── herbal_info/               # Herbal remedies
├── med_faqs/                  # Medical FAQs
├── med_history/               # Patient history
├── med_implant/               # Medical implants
├── med_physical_exams_questions/  # Exam questions
├── med_decision_guide/        # Clinical decision support
├── med_facts_checker/         # Fact verification
├── med_myths_checker/         # Myth debunking
├── med_terms_extractor/       # Term extraction
├── med_topic/                 # Topic information
├── synthetic_case_report/     # Case synthesis
├── surgical_tool_info/        # Surgical tools
├── medical_dictionary.py      # Medical glossary
└── user_guide.py              # User guide
```

## Key Modules

### 1. Disease Information
Information about medical conditions, causes, symptoms, diagnosis, and treatment.

```bash
python -m medkit medical disease_info --disease diabetes
python -m medkit medical disease_info --disease "heart disease"
```

### 2. Anatomy
Detailed anatomical information about body structures.

```bash
python -m medkit medical anatomy --structure heart
python -m medkit medical anatomy --structure brain
```

### 3. Medical Procedures
Information about diagnostic and therapeutic medical procedures.

```bash
python -m medkit medical med_procedure_info --procedure "knee replacement"
python -m medkit medical med_procedure_info --procedure "colonoscopy"
```

### 4. Surgical Information
Details about surgical procedures and outcomes.

```bash
python -m medkit medical surgical_info --surgery "appendectomy"
python -m medkit medical surgical_info --surgery "cardiac bypass"
```

### 5. Herbal Information
Information about medicinal herbs and natural remedies.

```bash
python -m medkit medical herbal_info --herb ginger
python -m medkit medical herbal_info --herb turmeric
```

### 6. Medical FAQs
Frequently asked questions on medical topics.

```bash
python -m medkit medical med_faqs --topic diabetes
python -m medkit medical med_faqs --topic hypertension
```

### 7. Medical Implants
Information about surgical implants and devices.

```bash
python -m medkit medical med_implant --implant "pacemaker"
python -m medkit medical med_implant --implant "hip replacement"
```

### 8. Fact Checker
Verify medical facts and claims.

```bash
python -m medkit medical med_facts_checker --fact "Vaccines are safe"
python -m medkit medical med_facts_checker --fact "Sleep is important"
```

### 9. Myth Checker
Debunk common medical myths.

```bash
python -m medkit medical med_myths_checker --myth "Sugar makes kids hyperactive"
python -m medkit medical med_myths_checker --myth "We only use 10% of our brain"
```

### 10. Medical Terms Extractor
Extract medical terminology from text.

```bash
python -m medkit medical med_terms_extractor --text "Patient presents with dyspnea"
python -m medkit medical med_terms_extractor --text "Diagnosis: Type 2 diabetes mellitus"
```

### 11. Medical Dictionary
Reference medical terms and definitions.

```python
from medical.medical_dictionary import MedicalDictionary

dictionary = MedicalDictionary()
definition = dictionary.get_definition("hypertension")
```

### 12. Medical Specialties
Information about medical specialties and specializations.

```bash
python -m medkit medical med_speciality --specialty cardiology
python -m medkit medical med_speciality --specialty neurology
```

### 13. Medical Decision Guide
Clinical decision support and guidance.

```bash
python -m medkit medical med_decision_guide --condition "chest pain"
python -m medkit medical med_decision_guide --condition "fever"
```

### 14. Surgical Tools
Reference for surgical instruments and tools.

```bash
python -m medkit medical surgical_tool_info --tool "scalpel"
python -m medkit medical surgical_tool_info --tool "sutures"
```

### 15. Synthetic Case Reports
Generate synthetic medical case reports for learning.

```bash
python -m medkit medical synthetic_case_report --condition diabetes
python -m medkit medical synthetic_case_report --condition hypertension
```

## Usage Examples

### Example 1: Research a Disease

```bash
python -m medkit medical disease_info --disease "type 2 diabetes" \
  --output diabetes.json
```

### Example 2: Learn About Anatomy

```bash
python -m medkit medical anatomy --structure heart --output heart.json
```

### Example 3: Understand a Procedure

```bash
python -m medkit medical med_procedure_info --procedure "knee replacement" \
  --output knee_replacement.json
```

### Example 4: Herbal Research

```bash
python -m medkit medical herbal_info --herb ginger --output ginger.json
```

### Example 5: Fact Verification

```bash
python -m medkit medical med_facts_checker \
  --fact "Regular exercise improves health"
```

## Python API Usage

### Disease Information

```python
from medical.disease_info.disease_info_cli import DiseaseInfoGenerator

generator = DiseaseInfoGenerator()
result = generator.generate_text("diabetes", structured=True)

print(f"Disease: {result.name}")
print(f"Symptoms: {result.symptoms}")
print(f"Treatment: {result.treatment}")
```

### Anatomy Information

```python
from medical.anatomy.medical_anatomy_cli import AnatomyInfoGenerator

generator = AnatomyInfoGenerator()
result = generator.generate_text("heart", structured=True)

print(f"Structure: {result.name}")
print(f"Function: {result.function}")
```

### Batch Processing

```python
from medical.disease_info.disease_info_cli import DiseaseInfoGenerator

generator = DiseaseInfoGenerator()
diseases = ["diabetes", "hypertension", "asthma", "arthritis"]

for disease in diseases:
    result = generator.generate_text(disease, structured=True)
    result.save(f"{disease}_info.json")
    print(f"✓ Processed {disease}")
```

## Configuration

### Environment Variables

```bash
export MEDKIT_MODEL=ollama/gemma3
export MEDKIT_OUTPUT_DIR=/path/to/outputs
export MEDKIT_LOG_LEVEL=INFO
```

### Command-Line Options

All medical module commands support:

| Option | Description |
|--------|-------------|
| `--output` | Save to file |
| `--output-dir` | Output directory |
| `--model` | LLM model |
| `-v, --verbosity` | Log level (0-4) |

## Common Use Cases

### Use Case 1: Patient Education

```bash
# Create patient education materials
for disease in diabetes hypertension asthma; do
  python -m medkit medical disease_info --disease "$disease" \
    --output "patient_education_${disease}.json"
done
```

### Use Case 2: Medical Reference

```bash
# Build a medical reference library
mkdir -p medical_reference

# Diseases
python -m medkit medical disease_info --disease diabetes \
  --output medical_reference/diabetes.json

# Procedures
python -m medkit medical med_procedure_info --procedure "knee replacement" \
  --output medical_reference/knee_replacement.json

# Anatomy
python -m medkit medical anatomy --structure heart \
  --output medical_reference/heart.json
```

### Use Case 3: Fact Checking

```python
# Verify medical claims
claims = [
    "Drinking water prevents dehydration",
    "Regular exercise improves mental health",
    "Sleep is essential for health"
]

from medical.med_facts_checker.medical_facts_checker_cli import FactChecker

fact_checker = FactChecker()
for claim in claims:
    result = fact_checker.generate_text(claim, structured=True)
    print(f"Claim: {claim}")
    print(f"Verified: {result.is_verified}")
    print(f"Explanation: {result.explanation}\n")
```

## Limitations

1. **Information Quality**: Depends on LLM training data
2. **Knowledge Cutoff**: May not include recent research
3. **Not Personalized**: Cannot provide individualized medical advice
4. **Educational Purpose**: For learning and reference only
5. **Incomplete**: Coverage varies by topic
6. **No Professional Review**: Not reviewed by medical professionals

## Best Practices

1. **Verify Information**: Cross-reference with authoritative sources
2. **Professional Consultation**: Consult healthcare providers
3. **Current Research**: Check for recent updates
4. **Context Matters**: Individual situations vary
5. **Use as Reference**: For educational and reference purposes
6. **Evidence-Based**: Prefer evidence-based information

## Important Disclaimers

**This module is for educational and informational purposes only.** It is not a substitute for professional medical advice. Users should:

- Consult qualified healthcare professionals
- Verify information with peer-reviewed sources
- Be aware of LLM limitations
- Understand that medical information changes
- Consider individual circumstances
- Report health concerns to healthcare providers

## Related Modules

- [drug/](../drug/) - Pharmaceutical information
- [phyexams/](../phyexams/) - Physical examinations
- [mental_health/](../mental_health/) - Mental health assessment
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
