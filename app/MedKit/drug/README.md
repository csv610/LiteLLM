# Drug Module

Drug and pharmaceutical information system.

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

The `medkit-drug` CLI exposes the following subcommands:

| Subcommand | Purpose | Example |
|---|---|---|
| `list` | Show all available drug tools | `medkit-drug list` |
| `info` | Comprehensive medicine information | `medkit-drug info "aspirin"` |
| `interact` | Drug-drug interaction analysis | `medkit-drug interact "warfarin" "aspirin"` |
| `food` | Drug-food interaction analysis | `medkit-drug food "metformin" "grapefruit"` |
| `disease` | Drug-disease safety analysis | `medkit-drug disease "ibuprofen" "kidney disease"` |
| `similar` | Find therapeutically similar medicines | `medkit-drug similar "aspirin"` |
| `compare` | Side-by-side medicine comparison | `medkit-drug compare "ibuprofen" "naproxen"` |
| `symptoms` | Suggest drug categories by symptom context | `medkit-drug symptoms "persistent dry cough"` |
| `addiction` | Addiction and withdrawal information | `medkit-drug addiction "opioids"` |
| `explain` | Patient-friendly medicine explanation | `medkit-drug explain "acetaminophen"` |

Global flags are available for all subcommands:

- `-m, --model`
- `-d, --output-dir`
- `-v, --verbosity`
- `-s, --structured`

## Usage Examples

### Example 1: Get Aspirin Information

```bash
medkit-drug info aspirin -d outputs -s
```

### Example 2: Check Drug Interactions

```bash
# Check interaction between Warfarin and Aspirin
medkit-drug interact warfarin aspirin -s
```

### Example 3: Check Food Interactions

```bash
# Check if Metformin interacts with food
medkit-drug food metformin "dairy products" -s
```

### Example 4: Compare Medicines

```bash
# Compare Ibuprofen vs Aspirin
medkit-drug compare ibuprofen aspirin -s
```

### Example 5: Find Alternatives

```bash
# Find medicines similar to Aspirin
medkit-drug similar aspirin -s
```

### Example 6: Disease-Specific Information

```bash
# Get info about Metformin for Diabetes
medkit-drug disease metformin diabetes -s
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

medkit-drug info "$MEDICINE" -d outputs -s

medkit-drug similar "$MEDICINE" -d outputs -s

echo "Research complete for $MEDICINE"
```

### Use Case 2: Interaction Checking

```bash
#!/bin/bash
# Check multiple drug interactions
PRIMARY_DRUG=$1

for other_drug in ibuprofen aspirin acetaminophen; do
  medkit-drug interact "$PRIMARY_DRUG" "$other_drug" -s
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
