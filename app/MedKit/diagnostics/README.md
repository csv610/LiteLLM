# Diagnostics Module

Medical tests and devices information system.

## Overview

The Diagnostics Module provides comprehensive information about medical tests, diagnostic procedures, and medical devices used in healthcare.

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
python -m medkit diagnostics medical_devices --device <device_name>
```

**Information Includes**:
- Device description and purpose
- Clinical applications
- Operation principles
- Safety considerations
- Maintenance requirements
- Cost and availability

### 2. Medical Tests

Information about laboratory and diagnostic tests.

```bash
python -m medkit diagnostics medical_tests --test <test_name>
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
python -m medkit diagnostics medical_devices --device "pacemaker" \
  --output pacemaker_info.json
```

### Example 2: Get Test Information

```bash
python -m medkit diagnostics medical_tests --test "CBC" \
  --output cbc_test.json
```

### Example 3: Batch Device Processing

```bash
for device in "pacemaker" "defibrillator" "stent"; do
  python -m medkit diagnostics medical_devices --device "$device" \
    --output "devices_${device}.json"
done
```

### Example 4: Batch Test Processing

```bash
for test in "CBC" "BMP" "CMP" "TSH" "Lipid Panel"; do
  python -m medkit diagnostics medical_tests --test "$test" \
    --output "tests_${test}.json"
done
```

## Python API Usage

### Medical Devices

```python
from diagnostics.medical_devices.medical_devices_cli import MedicalDevicesGenerator

generator = MedicalDevicesGenerator()
result = generator.generate_text("pacemaker", structured=True)

print(f"Device: {result.name}")
print(f"Purpose: {result.purpose}")
print(f"Applications: {result.applications}")
```

### Medical Tests

```python
from diagnostics.medical_tests.medical_tests_cli import MedicalTestsGenerator

generator = MedicalTestsGenerator()
result = generator.generate_text("CBC", structured=True)

print(f"Test: {result.name}")
print(f"Full Name: {result.full_name}")
print(f"Purpose: {result.purpose}")
print(f"Normal Range: {result.normal_range}")
```

## Common Use Cases

### Use Case 1: Device Research

```bash
#!/bin/bash
DEVICE=$1

python -m medkit diagnostics medical_devices --device "$DEVICE" \
  --output "${DEVICE}_info.json"

echo "Device information saved for $DEVICE"
```

### Use Case 2: Test Reference

```python
# Build test reference library
from diagnostics.medical_tests.medical_tests_cli import MedicalTestsGenerator

tests = [
    "CBC",          # Complete Blood Count
    "BMP",          # Basic Metabolic Panel
    "CMP",          # Comprehensive Metabolic Panel
    "TSH",          # Thyroid Stimulating Hormone
    "Lipid Panel"   # Cholesterol and triglycerides
]

generator = MedicalTestsGenerator()

for test in tests:
    result = generator.generate_text(test, structured=True)
    result.save(f"{test}_reference.json")
```

### Use Case 3: Comprehensive Diagnostic Information

```bash
#!/bin/bash
# Get comprehensive diagnostic information

mkdir -p diagnostic_reference

# Collect test information
echo "Collecting test information..."
for test in CBC TSH CMP BMP; do
  python -m medkit diagnostics medical_tests --test "$test" \
    --output "diagnostic_reference/${test}.json"
done

# Collect device information
echo "Collecting device information..."
for device in "pacemaker" "stent"; do
  python -m medkit diagnostics medical_devices --device "$device" \
    --output "diagnostic_reference/${device}.json"
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
