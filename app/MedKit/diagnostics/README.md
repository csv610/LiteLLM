# Diagnostics Module

Medical tests and devices information system.

## Overview

The Diagnostics Module provides information about medical tests, diagnostic procedures, and medical devices used in healthcare.

While there is no single "final" number because medical science is constantly evolving, there are thousands of individual medical tests. For context, the international standard used by hospitals and insurance companies (ICD-10-CM) contains over 70,000 codes for different medical tests and procedures. 
Most tests fall into these primary categories:
Laboratory Tests: These analyze samples of blood, urine, or tissue.
Blood Tests: Common ones include the Complete Blood Count (CBC) and Lipid Panels for cholesterol.
Urinalysis: Checks for kidney function, diabetes, and infections.
Genetic Testing: Screens for inherited conditions or disease predispositions.
Diagnostic Imaging: Non-invasive ways to look inside the body.
X-rays & CT Scans: Used for bones and identifying internal structures.
MRI & Ultrasound: Detailed imaging for soft tissues and organs.
PET Scans: Often used to detect cancer or monitor organ function.
Physical & Visual Examinations:
Endoscopy: Using a camera to look inside the digestive tract.
Biopsy: Removing a small tissue sample for laboratory analysis.


## Module Structure

```
diagnostics/
├── medical_devices/        # Medical devices information
│   ├── medical_devices_cli.py
│   ├── medical_devices_models.py
│   └── README.md
│
├── medical_tests/          # Medical tests information
│   ├── medical_tests_cli.py
│   ├── medical_tests_models.py
│   └── README.md
│
└── __init__.py
```

## Module Components

### 1. Medical Devices

Information about medical devices, equipment, and instruments used in healthcare.

```bash
python medical_test_devices_cli.py -i "pacemaker" \
  --output-dir outputs/
```

### 2. Medical Tests

Information about laboratory and diagnostic tests.

```bash
python medical_test_info_cli.py -i "CBC" \
  --output-dir outputs/
```

**Information Includes**:
- Test purpose and clinical use
- Sample requirements
- Procedure description
- Reference ranges/normal values
- Interpretation guidelines
- Limitations and considerations

## Usage Examples

### Example 1: Get Device Information

```bash
python medical_test_devices_cli.py -i "pacemaker" \
  --output-dir outputs/
```

### Example 2: Get Test Information

```bash
python medical_test_info_cli.py -i "CBC" \
  --output-dir outputs/
```

### Example 3: Batch Device Processing

```bash
for device in "pacemaker" "defibrillator" "stent"; do
  python medical_test_devices_cli.py -i "$device" \
    --output-dir outputs/
done
```

### Example 4: Batch Test Processing

```bash
for test in "CBC" "BMP" "CMP" "TSH" "Lipid Panel"; do
  python medical_test_info_cli.py -i "$test" \
    --output-dir outputs/
done
```

## Python API Usage

### Medical Devices

```python
from lite.config import ModelConfig
from diagnostics.medical_devices.medical_test_devices import MedicalTestDeviceGenerator

model_config = ModelConfig(model="ollama/gemma3", temperature=0.2)
generator = MedicalTestDeviceGenerator(model_config)
result = generator.generate_text("pacemaker", structured=True)

print(result)
```

### Medical Tests

```python
from lite.config import ModelConfig
from diagnostics.medical_tests.medical_test_info import MedicalTestInfoGenerator

model_config = ModelConfig(model="ollama/gemma3", temperature=0.2)
generator = MedicalTestInfoGenerator(model_config)
result = generator.generate_text("CBC", structured=True)

print(result)
```

## Common Use Cases

### Use Case 1: Device Research

```bash
#!/bin/bash
DEVICE=$1

python medical_test_devices_cli.py -i "$DEVICE" \
  --output-dir outputs/

echo "Device information saved for $DEVICE"
```

### Use Case 2: Test Reference

```python
# Build test reference library
from lite.config import ModelConfig
from diagnostics.medical_tests.medical_test_info import MedicalTestInfoGenerator
from pathlib import Path

tests = [
    "CBC",          # Complete Blood Count
    "BMP",          # Basic Metabolic Panel
    "CMP",          # Comprehensive Metabolic Panel
    "TSH",          # Thyroid Stimulating Hormone
    "Lipid Panel"   # Cholesterol and triglycerides
]

model_config = ModelConfig(model="ollama/gemma3", temperature=0.2)
generator = MedicalTestInfoGenerator(model_config)

for test in tests:
    result = generator.generate_text(test, structured=True)
    generator.save(result, Path("outputs/"))
```

### Use Case 3: Comprehensive Diagnostic Information

```bash
#!/bin/bash
# Get comprehensive diagnostic information

mkdir -p outputs

# Collect test information
echo "Collecting test information..."
for test in CBC TSH CMP BMP; do
  python medical_test_info_cli.py -i "$test" \
    --output-dir outputs/
done

# Collect device information
echo "Collecting device information..."
for device in "pacemaker" "stent"; do
  python medical_test_devices_cli.py -i "$device" \
    --output-dir outputs/
done

echo "Diagnostic reference complete"
```

## Data Models

### MedicalDevice

```python
class MedicalDevice(BaseModel):
    name: str                          # Device name
    full_name: Optional[str]           # Full/official name
    category: str                      # Device category
    purpose: str                       # Primary purpose
    applications: List[str]            # Clinical applications
    principle: str                     # Operating principle
    safety_considerations: str         # Safety information
    maintenance: Optional[str]         # Maintenance requirements
    cost: Optional[str]                # Cost information
    availability: Optional[str]        # Availability
```

### MedicalTest

```python
class MedicalTest(BaseModel):
    name: str                          # Test name/abbreviation
    full_name: str                     # Full test name
    category: str                      # Test category
    purpose: str                       # Clinical purpose
    sample_type: str                   # Sample requirement (blood, urine, etc.)
    procedure: str                     # How test is performed
    normal_range: Optional[str]        # Normal reference range
    interpretation: str                # How to interpret results
    limitations: Optional[str]         # Test limitations
    notes: Optional[str]               # Additional notes
```

## Configuration

### Environment Variables

```bash
export MEDKIT_MODEL=ollama/gemma3
export MEDKIT_OUTPUT_DIR=/path/to/outputs
export MEDKIT_LOG_LEVEL=INFO
```

### Command Options

| Option | Description |
|--------|-------------|
| `--output` | Save to file |
| `--output-dir` | Output directory |
| `--model` | LLM model |
| `-v, --verbosity` | Log level (0-4) |

## Common Devices

Typical devices covered:

### Monitoring Devices
- Pacemakers
- Defibrillators (ICD)
- Heart monitors
- Pulse oximetry

### Imaging Devices
- X-ray machines
- MRI machines
- CT scanners
- Ultrasound machines

### Therapeutic Devices
- Stents
- Implants
- Prosthetics
- Surgical instruments

## Common Tests

Typical tests covered:

### Blood Tests
- CBC (Complete Blood Count)
- CMP (Comprehensive Metabolic Panel)
- BMP (Basic Metabolic Panel)
- Lipid Panel
- Liver Function Tests

### Hormonal Tests
- TSH (Thyroid Stimulating Hormone)
- Glucose
- Insulin

### Specialized Tests
- EKG/ECG
- Echocardiogram
- Endoscopy
- Biopsy

## Limitations

1. **Model Dependent**: Quality depends on LLM training data
2. **Knowledge Cutoff**: Information reflects training date
3. **No Professional Review**: Not medically reviewed
4. **Educational**: For learning purposes
5. **Incomplete**: May not cover all devices/tests
6. **Changing Information**: Medical practice evolves

## Best Practices

1. **Verify Information**: Cross-reference with authoritative sources
2. **Professional Consultation**: Consult healthcare providers
3. **Current Data**: Check for recent updates/changes
4. **Context**: Understand individual circumstances vary
5. **Limitations**: Know test/device limitations
6. **Documentation**: Keep complete records

## Important Disclaimers

**This module is for educational and informational purposes only.** It is not:
- Medical advice
- A substitute for professional consultation
- Diagnostic tool
- Treatment recommendation

Users must:
- Consult qualified healthcare professionals
- Verify information with authoritative sources
- Understand information is educational only
- Follow healthcare provider guidance
- Report results to appropriate providers

## Related Modules

- [medical/](../medical/) - Medical information
- [drug/](../drug/) - Pharmaceutical information
- [phyexams/](../phyexams/) - Physical examinations
- [mental_health/](../mental_health/) - Mental health assessment

## Support

For help:
1. See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
2. Check [CLI_REFERENCE.md](../CLI_REFERENCE.md)
3. Review [API.md](../API.md)
4. Read [FAQ.md](../FAQ.md)

## References

- FDA Medical Device Database
- CDC Laboratory Test Information
- Clinical Laboratory Standards Institute (CLSI)
- American Clinical Laboratory Association

---

**Last Updated**: January 25, 2026
**Related**: [README.md](../README.md) | [ARCHITECTURE.md](../ARCHITECTURE.md) | [CLI_REFERENCE.md](../CLI_REFERENCE.md)
