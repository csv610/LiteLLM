# Medical Test Devices Guide

## Overview

The **Medical Test Devices CLI** is a documentation generator for medical devices and equipment. It uses AI-powered analysis to produce detailed information about diagnostic imaging equipment, surgical instruments, monitoring devices, and other medical devices.

This tool is designed for:
- **Clinical staff** preparing procurement decisions and specifications
- **Hospital administrators** evaluating equipment investments
- **Training coordinators** developing operator training materials
- **Compliance officers** documenting safety and regulatory requirements
- **Quality assurance teams** establishing maintenance and calibration schedules

## Key Features

- **Coverage**: Generates 15+ categories of device information
- **AI-Analysis**: Uses AI-powered analysis based on medical knowledge
- **Structured Output**: Organized JSON format for easy processing and integration
- **Flexible Configuration**: Customizable model selection, caching, and logging
- **Both CLI and API**: Command-line interface for quick access, Python API for integration
- **Automatic File Management**: Creates output directories as needed
- **Fail-Fast Validation**: Early validation of output paths before expensive LLM calls

## Installation & Setup

### Prerequisites
- Python 3.8+
- MedKit dependencies installed
- Ollama running with Gemma3 model (or configured alternative)
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
python medical_test_devices_cli.py -i "CT Scanner" -d ./medical_equipment/

# Use structured output with Pydantic model
python medical_test_devices_cli.py -i "MRI Scanner" -s

# Specify model and verbosity
python medical_test_devices_cli.py -i "X-Ray Machine" -m ollama/gemma3 -v 3
```

### Command-Line Arguments

| Argument | Short | Long | Description | Default |
|----------|-------|------|-------------|---------|
| **Test Device** | `-i` | `--test-device`, `--test_device` | Medical test device name (required) | - |
| **Output Directory** | `-d` | `--output-dir` | Directory for output files | `outputs/` |
| **Model** | `-m` | `--model` | LLM model to use | `ollama/gemma3` |
| **Verbosity** | `-v` | `--verbosity` | Logging level (0-4) | `2` |
| **Structured** | `-s` | `--structured` | Use structured Pydantic output | `False` |

### Usage Examples

```bash
# Generate basic device information
python medical_test_devices_cli.py --test-device "ECG Machine"

# With custom output directory and structured output
python medical_test_devices_cli.py -i "Blood Pressure Monitor" -d ./reports/ -s

# Full configuration
python medical_test_devices_cli.py \
  --test-device "Patient Monitor" \
  --output-dir ./medical_devices/ \
  --model ollama/gemma3 \
  --verbosity 3 \
  --structured

# Quick usage with short arguments
python medical_test_devices_cli.py -i "Ultrasound Probe" -d results/ -s
```

### Output Structure

The tool generates comprehensive device information in JSON format:

```json
{
  "device_name": "Ultrasound Machine",
  "basic_information": {
    "device_type": "Diagnostic Imaging",
    "primary_use": "Medical imaging and diagnostics",
    "manufacturer": "Various manufacturers available"
  },
  "technical_specifications": {
    "dimensions": "Detailed physical specifications",
    "weight": "Device weight specifications",
    "power_requirements": "Electrical requirements"
  },
  "clinical_applications": {
    "primary_uses": ["List of primary medical applications"],
    "specialties": ["Relevant medical specialties"]
  },
  "safety_features": {
    "electrical_safety": "Safety certifications and features",
    "patient_safety": "Patient protection mechanisms"
  },
  "maintenance_requirements": {
    "routine_maintenance": "Regular maintenance schedule",
    "calibration_requirements": "Calibration procedures"
  },
  "regulatory_compliance": {
    "fda_status": "FDA approval status",
    "ce_marking": "CE marking information",
    "other_certifications": ["Additional certifications"]
  }
}
```

## Advanced Usage

### Structured Output Mode

Use the `-s` flag to get structured Pydantic model output:

```bash
python medical_test_devices_cli.py -i "MRI Scanner" -s
```

This provides:
- **Type-safe** data structures
- **Validation** of output format
- **Better IDE support** with autocompletion
- **Easier integration** with Python applications

### Custom Model Configuration

```bash
# Use different models
python medical_test_devices_cli.py -i "CT Scanner" -m ollama/llama2

# Adjust temperature (in code, not CLI)
# Modify the ModelConfig in the CLI file
```

### Verbosity Levels

Control logging output with verbosity levels:

```bash
# Critical errors only
python medical_test_devices_cli.py -i "Device" -v 0

# Errors only
python medical_test_devices_cli.py -i "Device" -v 1

# Warnings (default)
python medical_test_devices_cli.py -i "Device" -v 2

# Info messages
python medical_test_devices_cli.py -i "Device" -v 3

# Debug messages
python medical_test_devices_cli.py -i "Device" -v 4
```

## Project Structure

```
medical_devices/
├── README.md                    # This documentation
├── medical_test_devices_cli.py  # CLI interface
├── medical_test_devices.py      # Core generator class
├── medical_test_devices_models.py  # Pydantic data models
├── medical_test_devices_prompts.py  # Prompt templates
├── outputs/                     # Generated reports
├── logs/                        # Application logs
└── assets/                      # Documentation assets
```

## API Usage

### Python Integration

```python
from lite.config import ModelConfig
from medical_test_devices import MedicalTestDeviceGenerator

# Configure the generator
model_config = ModelConfig(model="ollama/gemma3", temperature=0.2)
generator = MedicalTestDeviceGenerator(model_config)

# Generate device information
result = generator.generate_text("ECG Machine", structured=True)

# Save to file
from pathlib import Path
saved_path = generator.save(result, Path("outputs/ecg_machine.json"))
```

### Configuration Class

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class DeviceConfig:
    output_path: Optional[Path] = None
    verbosity: int = 2
    enable_cache: bool = True

# Use with the generator
config = DeviceConfig(verbosity=3)
```

## Device Categories Supported

The tool can generate information for various medical device categories:

### Diagnostic Imaging
- MRI Scanners
- CT Scanners
- X-Ray Machines
- Ultrasound Systems
- Mammography Systems
- Fluoroscopy Equipment

### Patient Monitoring
- ECG Machines
- Blood Pressure Monitors
- Pulse Oximeters
- Patient Monitors
- Fetal Monitors
- Temperature Monitoring

### Laboratory Equipment
- Blood Analyzers
- Microscopes
- Centrifuges
- Spectrometers
- Autoclaves
- Incubators

### Surgical Equipment
- Surgical Lights
- Operating Tables
- Electrosurgical Units
- Anesthesia Machines
- Surgical Microscopes
- Endoscopy Equipment

### Therapeutic Devices
- Infusion Pumps
- Ventilators
- Dialysis Machines
- Radiation Therapy
- Laser Systems
- Physiotherapy Equipment

## Error Handling

The CLI provides comprehensive error handling:

```bash
# Invalid device name
python medical_test_devices_cli.py -i ""
# Error: Test device name cannot be empty

# Permission issues
python medical_test_devices_cli.py -i "Device" -d /protected/
# Error: Permission denied creating directory

# Model unavailable
python medical_test_devices_cli.py -i "Device" -m invalid/model
# Error: Model not available
```

## Troubleshooting

### Common Issues

1. **Model Not Available**
   ```bash
   # Check available models
   ollama list
   
   # Pull required model
   ollama pull gemma3
   ```

2. **Permission Denied**
   ```bash
   # Check directory permissions
   ls -la outputs/
   
   # Create directory manually if needed
   mkdir -p outputs/
   chmod 755 outputs/
   ```

3. **Import Errors**
   ```bash
   # Check Python path and dependencies
   python -c "import medical_test_devices; print('OK')"
   ```

### Debug Mode

Enable debug logging for troubleshooting:

```bash
python medical_test_devices_cli.py -i "Test Device" -v 4
```

This provides detailed logging information including:
- Model configuration
- Prompt details
- API responses
- File operations

## Performance Considerations

### Optimization Tips

1. **Use Structured Output** (`-s`) for better performance
2. **Cache Results** when using the same device repeatedly
3. **Adjust Temperature** for different use cases:
   - `0.1-0.3`: Factual, technical information
   - `0.5-0.7`: Balanced output
   - `0.8-1.0`: Creative descriptions

### Resource Usage

- **Memory**: Minimal overhead
- **CPU**: Light usage during generation
- **Disk**: Output files typically 10-50KB
- **Network**: Required for LLM API calls

## Contributing

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd MedKit/diagnostics/medical_devices

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Check code style
python -m flake8 medical_test_devices*.py
```

### Adding New Device Categories

1. Update `medical_test_devices_models.py` with new fields
2. Modify prompts in `medical_test_devices_prompts.py`
3. Update documentation in README.md
4. Add tests for new functionality

## License

This project is part of the MedKit framework and follows the same licensing terms.

## Support

For issues, questions, or contributions:
- Create an issue in the project repository
- Check existing documentation
- Review test cases for usage examples

---

**Last Updated**: February 2026
**Version**: 1.0.0
**Framework**: MedKit

## Legal and Ethical Considerations

### **Medical Device Information Disclaimer**
- Generated information is for reference and educational purposes only
- Not a substitute for manufacturer documentation or clinical guidelines
- Always verify critical specifications with official sources
- Consult qualified biomedical engineers for equipment decisions

### **Contract and Usage Terms**
See [contract.md](contract.md) for legally binding usage terms and limitations

### **Intended Use**
- Equipment reference and educational purposes
- Training material development
- Procurement decision support
- Regulatory compliance documentation

### **Limitations**
- Not for clinical diagnosis or treatment decisions
- May not reflect latest manufacturer specifications
- Should be verified with official documentation
- Not a substitute for professional biomedical expertise

## Support & Resources

- For MedKit client issues, refer to MedKit documentation
- For Ollama setup, visit https://ollama.ai
- For model information, check the Gemma3 documentation
- Review [contract.md](contract.md) for legal and ethical usage terms
