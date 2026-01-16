# Medical Test Devices Guide

## Overview

The **Medical Test Devices CLI** is a comprehensive documentation generator for medical devices and equipment. It leverages AI-powered analysis to produce detailed, evidence-based information about diagnostic imaging equipment, surgical instruments, monitoring devices, and other medical devices.

This tool is designed for:
- **Clinical staff** preparing procurement decisions and specifications
- **Hospital administrators** evaluating equipment investments
- **Training coordinators** developing operator training materials
- **Compliance officers** documenting safety and regulatory requirements
- **Quality assurance teams** establishing maintenance and calibration schedules

## Key Features

- **Comprehensive Coverage**: Generates 15+ categories of device information
- **Evidence-Based**: Uses AI-powered analysis based on medical knowledge
- **Structured Output**: Organized JSON format for easy processing and integration
- **Flexible Configuration**: Customizable model selection, caching, and logging
- **Both CLI and API**: Command-line interface for quick access, Python API for integration
- **Automatic File Management**: Creates output directories as needed

## Installation & Setup

### Prerequisites
- Python 3.8+
- MedKit dependencies installed
- Ollama running with Gemma3:12b model (or configured alternative)
- Access to the MedKit client and configuration

### Basic Setup

```bash
# No additional installation required beyond MedKit
# Ensure Ollama service is running:
ollama serve
```

## Quick Start

### Using the CLI

Generate information for a medical device with a single command:

```bash
# Basic usage - saves to default output directory
python medical_test_devices_cli.py -i "Ultrasound Machine"

# Specify custom output directory
python medical_test_devices_cli.py -i "CT Scanner" -o ./medical_equipment/

# Device name with multiple words
python medical_test_devices_cli.py -i "Laparoscopic Surgical Tower" -o ./surgical_tools/
```

### Using the Python API

```python
from medical_test_devices_cli import MedicalTestDeviceGenerator

# Initialize generator with default configuration
generator = MedicalTestDeviceGenerator()

# Generate device information
result = generator.generate("Electrocardiogram Machine")

# Access the generated data
print(f"Device: {result.basic_info.device_name}")
print(f"Category: {result.basic_info.device_category}")
print(f"Manufacturer: {result.manufacturer_and_support.manufacturer_name}")

# Specify custom output path
from pathlib import Path
result = generator.generate(
    "MRI Scanner",
    output_path=Path("imaging_devices/mri_scanner.json")
)
```

## Detailed Usage

### Command-Line Interface (CLI)

#### Syntax
```bash
python medical_test_devices_cli.py -i DEVICE_NAME [-o OUTPUT_PATH]
```

#### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `-i, --input` | string | Yes | The name of the medical device to generate information for |
| `-o, --output` | string | No | Path to save the output JSON file (defaults to output directory) |

#### Examples

**Example 1: Generate information for a diagnostic device**
```bash
python medical_test_devices_cli.py -i "X-Ray Machine"
```
Output: `output/x_ray_machine_device_info.json`

**Example 2: Generate with custom directory**
```bash
python medical_test_devices_cli.py -i "Digital Microscope" -o ./equipment/microscopes/
```
Output: `equipment/microscopes/digital_microscope_device_info.json`

**Example 3: Generate for surgical equipment**
```bash
python medical_test_devices_cli.py -i "Surgical Laser System" -o ./surgical_equipment/
```

### Python API

#### Class: MedicalTestDeviceGenerator

```python
from medical_test_devices_cli import MedicalTestDeviceGenerator, Config
```

##### Initialization

**Default Configuration:**
```python
generator = MedicalTestDeviceGenerator()
```

**Custom Configuration:**
```python
from medical_test_devices_cli import Config
from pathlib import Path

config = Config(
    enable_cache=True,
    verbosity=3,  # INFO level
    db_path="/custom/path/to/database.lmdb",
    output_dir=Path("./custom_output/")
)

generator = MedicalTestDeviceGenerator(config=config)
```

##### Methods

**generate(device_name, output_path=None)**

Generates comprehensive medical device information.

```python
result = generator.generate(
    device_name="Defibrillator",
    output_path=Path("cardiac/defibrillator.json")
)
```

Returns: `MedicalDeviceInfo` object

**save(device_info, output_path)**

Saves generated device information to JSON file.

```python
output_location = generator.save(device_info, Path("output/device.json"))
```

Returns: `Path` object indicating saved file location

**print_summary(device_info, output_path)**

Displays a formatted summary in the console.

```python
generator.print_summary(device_info, Path("output/device.json"))
```

## Configuration

### Config Class

Configuration is managed through the `Config` dataclass which extends `MedKitConfig`:

```python
from medical_test_devices_cli import Config
from pathlib import Path

config = Config(
    enable_cache=True,           # Enable/disable response caching
    verbosity=2,                 # Logging level (0-4)
    db_path="/path/to/db.lmdb", # Cache database location
    output_dir=Path("./output")  # Default output directory
)
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable_cache` | bool | `True` | Enable caching to avoid redundant AI calls |
| `verbosity` | int | `2` | Logging level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG |
| `db_path` | str | `app/storage/medical_test_devices.lmdb` | Path to cache database |
| `output_dir` | Path | `./output/` | Default directory for saving output files |

### Model Selection

The default model is `ollama/gemma3:12b`. To use a different model, modify the `__init__` method or extend the class:

```python
class CustomMedicalGenerator(MedicalTestDeviceGenerator):
    def __init__(self, config=None):
        super().__init__(config)
        self.client = MedKitClient(model_name="ollama/mistral:latest")
```

## Output Format

Generated information is saved as structured JSON following the `MedicalDeviceInfo` schema.

### Sample Output Structure

```json
{
  "basic_info": {
    "device_name": "Ultrasound Machine",
    "device_category": "Diagnostic Imaging",
    "intended_use": "Pregnancy monitoring, abdominal imaging",
    "fda_classification": "Class II"
  },
  "physical_specifications": {
    "dimensions": "1.2m x 0.8m x 0.5m",
    "weight": "150 kg",
    "portability": "Mobile cart with wheels"
  },
  "technical_specifications": {
    "operating_principle": "Piezoelectric transducers",
    "frequency_range": "2-18 MHz",
    "resolution": "High resolution imaging"
  },
  "manufacturer_and_support": {
    "manufacturer_name": "GE Healthcare",
    "contact_information": "Provided in documentation"
  },
  "safety_and_regulatory": {
    "safety_features": "Thermal index monitoring, mechanical index monitoring",
    "adverse_events": "Rare thermal effects in fetal imaging"
  }
}
```

## Integration Examples

### Integration with Training Systems

```python
from pathlib import Path
from medical_test_devices_cli import MedicalTestDeviceGenerator

# Generate information for all devices in training program
devices = ["Ultrasound", "CT Scanner", "X-Ray Machine"]
generator = MedicalTestDeviceGenerator()

for device in devices:
    result = generator.generate(
        device,
        output_path=Path(f"training_materials/{device.lower().replace(' ', '_')}.json")
    )
    print(f"Generated training material for {result.basic_info.device_name}")
```

### Integration with Procurement System

```python
from medical_test_devices_cli import get_device_info
from pathlib import Path

# Generate specification documents for procurement
devices_for_purchase = [
    "Surgical Microscope",
    "Anesthesia Workstation",
    "Patient Monitor"
]

for device in devices_for_purchase:
    info = get_device_info(device, Path(f"procurement/{device}.json"))
    print(f"Cost: {info.cost_and_reimbursement.device_cost}")
    print(f"Certifications: {info.regulatory_and_certification.regulatory_status}")
```

### Batch Generation

```python
from medical_test_devices_cli import MedicalTestDeviceGenerator
from pathlib import Path
import json

generator = MedicalTestDeviceGenerator()

devices = {
    "Cardiac Devices": ["Defibrillator", "Pacemaker", "ECG Machine"],
    "Imaging": ["MRI Scanner", "PET Scanner", "Ultrasound"],
    "Surgical": ["Surgical Laser", "Electrosurgical Unit"]
}

for category, device_list in devices.items():
    category_path = Path(f"equipment/{category.lower().replace(' ', '_')}")

    for device in device_list:
        try:
            result = generator.generate(device, category_path / f"{device.lower()}.json")
            print(f"✓ {device}")
        except Exception as e:
            print(f"✗ {device}: {e}")
```

## Logging & Debugging

### Verbosity Levels

Control output detail through the `verbosity` configuration:

```python
from medical_test_devices_cli import Config, MedicalTestDeviceGenerator

# Silent operation (critical errors only)
config = Config(verbosity=0)

# Full debug information
config = Config(verbosity=4)

generator = MedicalTestDeviceGenerator(config)
```

### Monitoring Generation Progress

```python
import logging
from medical_test_devices_cli import MedicalTestDeviceGenerator

# Enable debug logging
generator = MedicalTestDeviceGenerator(Config(verbosity=4))

# Monitor the generation process
result = generator.generate("Surgical Robot")
```

The logger provides:
- Generation start/completion status
- File save confirmation
- Error messages with context
- Performance metrics (at DEBUG level)

## Troubleshooting

### Common Issues

#### Issue: "Device name cannot be empty"
**Solution**: Provide a valid device name to the `-i` argument
```bash
# ✗ Wrong
python medical_test_devices_cli.py -i ""

# ✓ Correct
python medical_test_devices_cli.py -i "Ultrasound Machine"
```

#### Issue: Output directory not found
**Solution**: The tool automatically creates directories. Ensure you have write permissions:
```bash
# Check permissions on parent directory
ls -ld ./output/
```

#### Issue: Model not found / Ollama connection error
**Solution**: Ensure Ollama is running and the model is available:
```bash
# Start Ollama (if not running)
ollama serve

# Download the model if needed
ollama pull gemma3:12b
```

#### Issue: JSON parsing errors in output
**Solution**: Check that the generated data is valid. Review logs with verbosity=4
```python
config = Config(verbosity=4)
generator = MedicalTestDeviceGenerator(config)
```

## File Management

### Output File Organization

By default, files are saved with names derived from the device name:

```
output/
├── ultrasound_machine_device_info.json
├── ct_scanner_device_info.json
└── surgical_laser_system_device_info.json
```

### Custom Organization

Organize by category or department:

```python
from pathlib import Path
from medical_test_devices_cli import MedicalTestDeviceGenerator

generator = MedicalTestDeviceGenerator()

# Organize by medical specialization
result = generator.generate(
    "Cardiology Monitor",
    output_path=Path("departments/cardiology/devices/monitor.json")
)
```

### File Size Considerations

Each generated file is typically 10-50 KB depending on device complexity. Plan storage accordingly for batch operations.

## Performance Considerations

### Caching

The generator caches results to avoid duplicate AI calls:

```python
from medical_test_devices_cli import Config

# Disable caching for always-fresh data
config = Config(enable_cache=False)
```

Benefits of caching:
- Faster repeated queries
- Reduced API costs
- Consistent results

### Batch Processing

For multiple devices, process sequentially to avoid overwhelming the system:

```python
from medical_test_devices_cli import MedicalTestDeviceGenerator
from pathlib import Path
import time

generator = MedicalTestDeviceGenerator()
devices = ["Device A", "Device B", "Device C"]

for device in devices:
    try:
        generator.generate(device)
        time.sleep(2)  # Brief pause between requests
    except Exception as e:
        print(f"Error generating {device}: {e}")
```

## Best Practices

### 1. Use Descriptive Device Names
```python
# ✓ Good - specific device name
generator.generate("GE Logiq E10 Ultrasound Machine")

# ✗ Avoid - too generic
generator.generate("Machine")
```

### 2. Organize Output Hierarchically
```python
# Organize by department and function
output_path = Path(f"equipment/{department}/{function}/{device_name}.json")
```

### 3. Version Your Equipment Database
```python
# Include timestamps for tracking equipment history
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d")
output_path = Path(f"equipment_db/{timestamp}/{device_name}.json")
```

### 4. Implement Error Handling
```python
from medical_test_devices_cli import MedicalTestDeviceGenerator
from pathlib import Path

generator = MedicalTestDeviceGenerator()

try:
    result = generator.generate("Device Name")
except ValueError as e:
    print(f"Invalid device name: {e}")
except (OSError, IOError) as e:
    print(f"File operation failed: {e}")
```

### 5. Regular Cache Maintenance
```python
# Periodically disable cache for updated information
config = Config(enable_cache=False)
generator = MedicalTestDeviceGenerator(config)
result = generator.generate("Device Name")  # Fresh data
```

## Advanced Usage

### Custom Configuration for Different Environments

```python
from pathlib import Path
from medical_test_devices_cli import Config, MedicalTestDeviceGenerator

def create_generator_for_environment(env: str):
    """Create a configured generator based on environment."""
    configs = {
        "production": Config(
            enable_cache=True,
            verbosity=1,  # Errors only
            output_dir=Path("/data/equipment_docs")
        ),
        "development": Config(
            enable_cache=False,
            verbosity=4,  # Full debug
            output_dir=Path("./output")
        ),
        "testing": Config(
            enable_cache=True,
            verbosity=0,  # Silent
            output_dir=Path("./test_output")
        )
    }

    return MedicalTestDeviceGenerator(configs.get(env))

# Usage
prod_generator = create_generator_for_environment("production")
```

### Extending the Generator

```python
from medical_test_devices_cli import MedicalTestDeviceGenerator
from pathlib import Path

class HospitalDeviceGenerator(MedicalTestDeviceGenerator):
    """Extended generator with hospital-specific features."""

    def generate_with_metadata(self, device_name: str,
                              department: str,
                              budget_code: str):
        """Generate device info with hospital metadata."""
        result = self.generate(device_name)

        # Add hospital-specific metadata
        metadata = {
            "department": department,
            "budget_code": budget_code,
            "device_info": result.model_dump()
        }

        return metadata
```

## API Reference

### MedicalTestDeviceGenerator

#### `__init__(config: Optional[Config] = None)`
Initialize the generator with optional configuration.

#### `generate(device_name: str, output_path: Optional[Path] = None) -> MedicalDeviceInfo`
Generate comprehensive device information.

#### `_generate_info(device_name: str) -> MedicalDeviceInfo`
Internal method to generate device information via AI client.

#### `save(device_info: MedicalDeviceInfo, output_path: Path) -> Path`
Save device information to JSON file.

#### `print_summary(device_info: MedicalDeviceInfo, output_path: Path) -> None`
Print formatted summary to console.

### Configuration

#### `Config` (extends `MedKitConfig`)
Configuration dataclass for the generator.

Properties:
- `enable_cache: bool = True`
- `verbosity: int = 2`
- `db_path: str` (auto-configured)
- `output_dir: Path` (auto-configured)

### Helper Functions

#### `get_device_info(device_name: str, output_path: Optional[Path] = None) -> MedicalDeviceInfo`
High-level convenience function for quick device information generation.

## FAQ

**Q: How long does it take to generate device information?**
A: Generation time depends on the AI model and system resources. Typically 30-120 seconds per device.

**Q: Can I use a different AI model?**
A: Yes, extend the class and modify the `__init__` method to use a different model with MedKitClient.

**Q: Is the generated information clinically accurate?**
A: The generator produces evidence-based information, but all outputs should be verified with official manufacturer documentation and clinical guidelines.

**Q: Can I batch process multiple devices?**
A: Yes, see the batch processing examples in this guide.

**Q: How do I update existing device information?**
A: Regenerate with `enable_cache=False` to get fresh data.

**Q: What file formats are supported for output?**
A: Currently supports JSON format. Use the output file to convert to other formats if needed.

## Support & Resources

- For MedKit client issues, refer to MedKit documentation
- For Ollama setup, visit https://ollama.ai
- For model information, check the Gemma3 documentation

---

**Last Updated**: 2026-01-16
**Version**: 1.0
