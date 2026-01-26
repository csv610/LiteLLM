# Drug Module

Comprehensive drug and pharmaceutical information system.

## Overview

The Drug Module provides tools for accessing pharmaceutical information, checking drug interactions, comparing medicines, and finding similar medications. It includes integration with pharmaceutical databases and LLM-based information synthesis.

## Module Structure

```
drug/
├── medicine/                    # Medicine information system
│   ├── medicine_info.py         # Main CLI and generator
│   ├── medicine_info_models.py  # Pydantic data models
│   ├── drugbank_medicine_cli.py # DrugBank integration
│   ├── rx_med_info_cli.py       # RxNorm integration
│   └── rxnorm_client_cli.py     # RxNorm client
│
├── drug_drug/                   # Drug-drug interactions
│   ├── drug_drug_interaction_cli.py
│   ├── drug_drug_models.py
│   └── README.md
│
├── drug_food/                   # Drug-food interactions
│   └── drug_food_interaction_cli.py
│
├── drug_disease/                # Drug-disease information
│   ├── drug_disease_interaction_cli.py
│   └── README.md
│
├── similar_drugs/               # Similar medicines finder
│   └── similar_drugs_cli.py
│
├── drugs_comparision/           # Medicine comparison
│   ├── drugs_comparison_cli.py
│   └── drugs_comparison_models.py
│
└── medicine_explainer.py        # Utility functions
```

## Features

### 1. Medicine Information
Get comprehensive information about medicines:
- Names and aliases
- Therapeutic uses
- Dosage information
- Side effects
- Drug interactions
- Precautions and warnings

**Command**:
```bash
python -m medkit drug medicine --medicine <name>
```

### 2. Drug-Drug Interactions
Check interactions between two medications:
- Severity level (mild, moderate, severe)
- Mechanism of interaction
- Clinical significance
- Management recommendations

**Command**:
```bash
python -m medkit drug drug_drug --drug1 <drug1> --drug2 <drug2>
```

### 3. Drug-Food Interactions
Check how medicines interact with food:
- Foods to avoid
- Timing considerations
- Nutritional impacts
- Management strategies

**Command**:
```bash
python -m medkit drug drug_food --drug <drug> --food <food>
```

### 4. Drug-Disease Information
Understand how medicines relate to diseases:
- Appropriateness for specific diseases
- Contraindications
- Precautions for disease states
- Monitoring requirements

**Command**:
```bash
python -m medkit drug drug_disease --drug <drug> --disease <disease>
```

### 5. Similar Medicines
Find alternative medicines with similar properties:
- Generic alternatives
- Therapeutic equivalents
- Different drug classes with similar effects
- Cost and availability information

**Command**:
```bash
python -m medkit drug similar_drugs --medicine <medicine>
```

### 6. Medicine Comparison
Compare two medicines side-by-side:
- Efficacy comparison
- Side effect profiles
- Cost differences
- Dosing differences
- Mechanism differences

**Command**:
```bash
python -m medkit drug drugs_comparision --medicine1 <med1> --medicine2 <med2>
```

## Usage Examples

### Example 1: Get Aspirin Information

```bash
python -m medkit drug medicine --medicine aspirin --output aspirin_info.json
```

### Example 2: Check Drug Interactions

```bash
# Check interaction between Warfarin and Aspirin
python -m medkit drug drug_drug --drug1 warfarin --drug2 aspirin
```

### Example 3: Check Food Interactions

```bash
# Check if Metformin interacts with food
python -m medkit drug drug_food --drug metformin --food "dairy products"
```

### Example 4: Compare Medicines

```bash
# Compare Ibuprofen vs Aspirin
python -m medkit drug drugs_comparision --medicine1 ibuprofen --medicine2 aspirin
```

### Example 5: Find Alternatives

```bash
# Find medicines similar to Aspirin
python -m medkit drug similar_drugs --medicine aspirin
```

### Example 6: Disease-Specific Information

```bash
# Get info about Metformin for Diabetes
python -m medkit drug drug_disease --drug metformin --disease diabetes
```

## Python API Usage

### Medicine Information

```python
from drug.medicine.medicine_info import MedicineInfoGenerator
from lite.lite_client import LiteClient

client = LiteClient()
generator = MedicineInfoGenerator(client)

# Get structured output
result = generator.generate_text("aspirin", structured=True)
print(f"Medicine: {result.name}")
print(f"Uses: {result.info}")

# Save to file
result.save("aspirin.json")
```

### Drug Interactions

```python
from drug.drug_drug.drug_drug_interaction_cli import DrugInteractionGenerator

generator = DrugInteractionGenerator()
interaction = generator.generate_text(
    drug1="warfarin",
    drug2="aspirin",
    structured=True
)
print(interaction.severity)
print(interaction.mechanism)
```

### Batch Processing

```python
from drug.medicine.medicine_info import MedicineInfoGenerator

generator = MedicineInfoGenerator()
medicines = ["aspirin", "ibuprofen", "metformin", "lisinopril"]

for medicine in medicines:
    result = generator.generate_text(medicine, structured=True)
    result.save(f"{medicine}_info.json")
    print(f"✓ Processed {medicine}")
```

## Configuration

### Environment Variables

```bash
# Model selection
export MEDKIT_MODEL=ollama/gemma3

# Output directory
export MEDKIT_OUTPUT_DIR=/path/to/outputs

# Logging level
export MEDKIT_LOG_LEVEL=INFO

# API key (for cloud models)
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
```

### Command-Line Options

All drug module commands support:

| Option | Description | Example |
|--------|-------------|---------|
| `--output` | Output file path | `--output result.json` |
| `--output-dir` | Output directory | `--output-dir ./outputs` |
| `--model` | LLM model | `--model ollama/mistral` |
| `--verbosity` | Log level (0-4) | `-v 4` |

## Data Models

### MedicineInfo

```python
from drug.medicine.medicine_info_models import MedicineInfo

class MedicineInfo(BaseModel):
    name: str                              # Medicine name
    generic_name: Optional[str]           # Generic name
    brand_names: List[str]                # Brand names
    uses: List[str]                       # Medical uses
    dosage: Optional[str]                 # Dosage info
    side_effects: List[str]               # Known side effects
    precautions: Optional[str]            # Precautions
    contraindications: List[str]          # Contraindications
    interactions: Optional[str]           # Drug interactions
```

### DrugInteraction

```python
class DrugInteraction(BaseModel):
    drug1: str                            # First drug
    drug2: str                            # Second drug
    severity: str                         # mild/moderate/severe
    mechanism: str                        # How interaction works
    clinical_significance: str            # Clinical importance
    management: str                       # How to manage
```

## Error Handling

```python
from medkit_exceptions import ValidationError, LLMError, MedKitError

try:
    result = generator.generate_text("aspirin")
except ValidationError as e:
    print(f"Invalid input: {e}")
except LLMError as e:
    print(f"LLM error: {e}")
except MedKitError as e:
    print(f"MedKit error: {e}")
```

## Common Use Cases

### Use Case 1: Medication Research

```bash
#!/bin/bash
MEDICINE=$1

python -m medkit drug medicine --medicine "$MEDICINE" \
  --output "${MEDICINE}_info.json"

python -m medkit drug similar_drugs --medicine "$MEDICINE" \
  --output "${MEDICINE}_similar.json"

echo "Research complete for $MEDICINE"
```

### Use Case 2: Interaction Checking

```bash
#!/bin/bash
# Check multiple drug interactions
PRIMARY_DRUG=$1

for other_drug in ibuprofen aspirin acetaminophen; do
  python -m medkit drug drug_drug \
    --drug1 "$PRIMARY_DRUG" \
    --drug2 "$other_drug"
done
```

### Use Case 3: Medication Comparison

```python
# Compare multiple medicines
medicines = ["aspirin", "ibuprofen", "naproxen"]
comparisons = []

generator = MedicineInfoGenerator()
for medicine in medicines:
    result = generator.generate_text(medicine, structured=True)
    comparisons.append({
        'medicine': medicine,
        'info': result.dict()
    })

import json
with open('medicine_comparison.json', 'w') as f:
    json.dump(comparisons, f, indent=2)
```

## Limitations

1. **Model Dependent**: Quality depends on underlying LLM training data
2. **Knowledge Cutoff**: Information reflects LLM training date
3. **No Medical Validation**: Not reviewed by pharmaceutical professionals
4. **Incomplete**: Some medicines may have limited coverage
5. **No Personal Recommendations**: Cannot recommend specific medicines for individuals
6. **Interaction Data**: May not be comprehensive for all drug combinations

## Best Practices

1. **Cross-reference**: Always verify information with authoritative sources
2. **Professional Consultation**: Consult pharmacists and physicians
3. **Current Information**: Check for recent changes/recalls
4. **Patient Context**: Individual patient factors affect medicine choice
5. **Dosage**: Never use generated dosage as final authority
6. **Interactions**: Always check with healthcare provider about interactions

## Related Modules

- [medical/](../medical/) - General medical information
- [mental_health/](../mental_health/) - Mental health assessment
- [phyexams/](../phyexams/) - Physical examination tools
- [diagnostics/](../diagnostics/) - Medical tests and devices

## Important Medical Disclaimers

**This module is for informational purposes only.** It is not a substitute for professional medical advice, diagnosis, or treatment. Users should:

- Consult qualified healthcare providers before using any medicine
- Verify information with peer-reviewed medical literature
- Be aware that LLM-generated content may contain inaccuracies
- Understand that pharmaceutical information changes frequently
- Report any adverse effects to healthcare providers
- Consider individual health conditions and medications

## Support and Troubleshooting

For issues:
1. Check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
2. See [CLI_REFERENCE.md](../CLI_REFERENCE.md) for command details
3. Review [API.md](../API.md) for Python integration
4. Check [FAQ.md](../FAQ.md) for common questions

## License

See parent project LICENSE file.

---

**Last Updated**: January 25, 2026
**Related**: [README.md](../README.md) | [ARCHITECTURE.md](../ARCHITECTURE.md) | [CLI_REFERENCE.md](../CLI_REFERENCE.md)
