# MedKit

A comprehensive medical information toolkit providing command-line access to disease identification, drug interaction checking, medical reference information, and clinical decision support tools.

## Why Use MedKit

### **Medical Terminology Recognition**
- 19 specialized recognizers for diseases, symptoms, drugs, and medical procedures
- Quick identification of medical terms with confidence levels
- Standardized medical terminology validation
- Support for clinical signs, lab units, and genetic variants

### **Drug Information and Safety**
- Drug-drug interaction checking with severity levels
- Drug-disease contraindication identification
- Drug-food interaction analysis
- Medication reference and safety information

### **Clinical Reference Tools**
- Disease information with symptoms and treatments
- Medical procedure descriptions and guidelines
- Anatomy and specialty information
- Physical examination guides and protocols

### **Decision Support Systems**
- Medical fact checking and validation
- Clinical decision guidance frameworks
- Symptom assessment and screening tools
- Mental health evaluation modules

## Quick Start

### **Medical Recognition Tools**
```bash
# Disease identification
python app/MedKit/recognizers/disease/disease_identifier_cli.py "diabetes mellitus"

# Symptom recognition
python app/MedKit/recognizers/medical_symptom/medical_symptom_cli.py "chest pain"

# Clinical sign identification
python app/MedKit/recognizers/clinical_sign/clinical_sign_cli.py "babinski sign"

# Drug identification
python app/MedKit/recognizers/medication_class/medication_class_cli.py "beta blockers"
```

### **Drug Interaction Tools**
```bash
# Drug-drug interactions
python app/MedKit/drug/drug_drug/drug_drug_interaction_cli.py --drug1 "aspirin" --drug2 "warfarin"

# Drug-disease interactions
python app/MedKit/drug/drug_disease/drug_disease_interaction_cli.py --drug "metformin" --disease "renal impairment"

# Drug-food interactions
python app/MedKit/drug/drug_food/drug_food_interaction_cli.py --drug "warfarin" --food "leafy greens"
```

### **Medical Reference Tools**
```bash
# Disease information
python app/MedKit/medical/disease_info/disease_info_cli.py --disease "hypertension"

# Medical procedures
python app/MedKit/medical/med_procedure_info/med_procedure_info_cli.py "appendectomy"

# Anatomy information
python app/MedKit/medical/anatomy/medical_anatomy_cli.py "heart"

# Medical specialties
python app/MedKit/medical/med_specialty/med_specialty_cli.py "cardiology"
```

### For Developers
- **[GETTING_STARTED.md](./GETTING_STARTED.md)** - Quick setup and first steps
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System design, modules, and data flow
- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Development environment setup, testing, running code
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Contribution guidelines and standards

### For Users
- **[CLI_REFERENCE.md](./CLI_REFERENCE.md)** - All available CLI commands
- **[API.md](./API.md)** - Public API documentation and usage examples
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - Quick lookup for common tasks

### For Operations
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Deployment procedures and configurations
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Common issues and solutions
- **[PERFORMANCE.md](./PERFORMANCE.md)** - Performance optimization and tuning
- **[FAQ.md](./FAQ.md)** - Frequently asked questions

### For Reference
- **[CLASS_REFERENCE.md](./CLASS_REFERENCE.md)** - Complete class and API reference
- **[CODE_STYLE_GUIDE.md](./CODE_STYLE_GUIDE.md)** - Code style and quality standards

## Directory Structure

```
MedKit/
├── drug/                          # Drug-related information systems
│   ├── medicine/                  # Medicine information and details
│   ├── drug_drug/                 # Drug-drug interaction checker
│   ├── drug_food/                 # Drug-food interaction checker
│   ├── drug_disease/              # Drug-disease information
│   ├── similar_drugs/             # Similar medicines finder
│   └── drugs_comparision/         # Drug comparison tool
│
├── medical/                       # Medical information modules
│   ├── disease_info/              # Disease information
│   ├── anatomy/                   # Anatomical information
│   ├── med_procedure_info/        # Medical procedures
│   ├── surgical_info/             # Surgical information
│   ├── med_speciality/            # Medical specialties
│   ├── herbal_info/               # Herbal remedies information
│   ├── med_faqs/                  # Frequently asked questions
│   ├── med_history/               # Patient medical history
│   ├── med_implant/               # Medical implants information
│   ├── med_physical_exams_questions/ # Physical exam questions
│   ├── med_decision_guide/        # Clinical decision support
│   ├── med_facts_checker/         # Fact checking tool
│   ├── med_myths_checker/         # Medical myth debunking
│   ├── med_terms_extractor/       # Medical term extraction
│   ├── med_topic/                 # Medical topics
│   ├── synthetic_case_report/     # Synthetic case generation
│   ├── surgical_tool_info/        # Surgical tools reference
│   └── medical_dictionary.py      # Medical term definitions
│
├── phyexams/                      # Physical examination modules
│   ├── exam_*.py                  # 26+ specialized exam modules
│   └── exam_specifications.py     # Exam data structures
│
├── mental_health/                 # Mental health assessment
│   ├── mental_health_assessment.py  # Assessment logic
│   ├── mental_health_report.py      # Report generation
│   └── mental_health_chat.py        # Chat interface
│
├── diagnostics/                   # Diagnostic tools
│   ├── medical_devices/           # Medical devices database
│   └── medical_tests/             # Medical tests information
│
├── sane_interview/                # Interview modules
│   └── sane_interview.py          # Interview logic
│
├── utils/                         # Utility modules
│   ├── cli_base.py                # Base classes for CLI modules
│   ├── error_handler.py           # Error handling utilities
│   ├── output_formatter.py        # Output formatting
│   ├── privacy_compliance.py      # Privacy/compliance utilities
│   ├── storage_config.py          # Storage configuration
│   ├── error_recovery.py          # Error recovery patterns
│   └── [other utilities]
│
├── tests/                         # Test suite
│   ├── test_cli_modules.py
│   ├── test_integration.py
│   └── [other tests]
│
├── medkit_exceptions.py           # Custom exception classes
├── __init__.py                    # Package initialization
├── __main__.py                    # CLI entry point
│
├── DOCUMENTATION/
│   ├── README.md (this file)
│   ├── ARCHITECTURE.md
│   ├── GETTING_STARTED.md
│   ├── DEVELOPMENT.md
│   ├── CONTRIBUTING.md
│   ├── DEPLOYMENT.md
│   ├── API.md
│   ├── CLASS_REFERENCE.md
│   ├── CLI_REFERENCE.md
│   ├── QUICK_REFERENCE.md
│   ├── TROUBLESHOOTING.md
│   ├── FAQ.md
│   ├── PERFORMANCE.md
│   └── CODE_STYLE_GUIDE.md
│
└── [Module-specific READMEs in each subdirectory]
```

## System Architecture at a Glance

### Module Organization

MedKit is organized into six major module categories:

1. **Drug Module**: Handles medicine information, interactions, and comparisons
2. **Medical Module**: Comprehensive medical information across specialties
3. **Physical Exams Module**: 26+ specialized physical examination tools
4. **Mental Health Module**: Assessment, detection, and reporting tools
5. **Diagnostics Module**: Medical devices and tests databases
6. **Interview Module**: Structured interview frameworks

### Technology Stack

- **Language**: Python 3.8+
- **LLM Integration**: LiteClient (custom wrapper around litellm)
- **Data Validation**: Pydantic for structured data models
- **CLI Framework**: argparse for command-line interfaces
- **Formatting**: Rich for console output formatting
- **Logging**: Python logging with centralized configuration

### Design Patterns

- **Base Classes**: `BaseCLI`, `BaseGenerator`, `BasePromptBuilder` eliminate code duplication
- **Exception Handling**: Custom exception hierarchy in `medkit_exceptions.py`
- **Structured Output**: Pydantic models for all data structures
- **Error Recovery**: Automatic retry logic and graceful degradation

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API keys for language models (see [GETTING_STARTED.md](./GETTING_STARTED.md))

### Quick Start

```bash
# 1. Clone the repository
cd /path/to/MedKit

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run a simple command
python -m medkit drug medicine -i "aspirin"

# 4. View help
python -m medkit --help
```

For detailed setup instructions, see [GETTING_STARTED.md](./GETTING_STARTED.md).

## Key Concepts

### CLI Modules

Each module follows a consistent CLI pattern:

```bash
python -m medkit <module> <submodule> [options]
```

Example:
```bash
python -m medkit drug medicine --herb ginger --output output.json
python -m medkit medical disease_info --disease diabetes
python -m medkit phyexams exam_depression_screening --patient-id P123
```

### Structured Data

Most outputs are structured using Pydantic models:

```python
from medical.herbal_info.herbal_info_models import HerbalInfo

# Results are automatically serializable to JSON
result: HerbalInfo = generate_herbal_info("ginger")
result.save("output.json")
```

### Error Handling

Consistent exception hierarchy for error handling:

```python
from medkit_exceptions import MedKitError, ValidationError, LLMError

try:
    result = generate_medicine_info("aspirin")
except ValidationError as e:
    # Handle invalid input
    pass
except LLMError as e:
    # Handle LLM-specific errors
    pass
except MedKitError as e:
    # Handle general MedKit errors
    pass
```

## Features by Module

### Drug Module
- Medicine information and pharmacology
- Drug-drug interaction checking
- Drug-food interaction checking
- Drug-disease information
- Similar medicine finder
- Medicine comparison tool

### Medical Module (20+ specialized modules)
- Disease information and management
- Anatomical information
- Medical procedures
- Surgical information
- Medical specialties
- Herbal medicine information
- Medical FAQs
- Medical history tracking
- Medical implants database
- Physical exam question generation
- Clinical decision guidance
- Medical fact checking
- Medical myth debunking
- Medical term extraction
- Synthetic case report generation
- Surgical tools reference

### Physical Exams Module (26+ exam modules)
Specialized modules for examining:
- Depression screening
- Abstract reasoning
- Arithmetic calculation
- Attention span
- Blood vessels
- Breast and axillae
- Emotional stability
- Head and neck
- Judgement assessment
- Lymphatic system
- Memory and cognition
- Musculoskeletal system
- Nutrition and growth
- Skin, hair, and nails
- Writing ability
- And 10+ more specialized exams

### Mental Health Module
- Depression screening (PHQ-9)
- Generalized anxiety screening (GAD-7)
- Symptom detection
- Mental health reporting
- Chat-based assessment interface

### Diagnostics Module
- Medical devices database
- Medical tests information

## Contributing

MedKit welcomes contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Development guidelines
- Code style standards
- Testing requirements
- Submission process

## License

See LICENSE file for details.

## Support

- **Issues**: Submit bugs and feature requests via GitHub Issues
- **Documentation**: See the docs/ directory for detailed guides
- **FAQ**: Check [FAQ.md](./FAQ.md) for common questions

## Additional Resources

- **Module Documentation**: Each module has its own README.md
- **API Reference**: See [API.md](./API.md) for public API details
- **CLI Commands**: See [CLI_REFERENCE.md](./CLI_REFERENCE.md) for all commands
- **Troubleshooting**: See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues
- **Performance Tips**: See [PERFORMANCE.md](./PERFORMANCE.md) for optimization

## Architecture Overview

For a detailed understanding of:
- System architecture and module relationships
- Data flow and integration points
- Base classes and patterns
- Exception hierarchy

See [ARCHITECTURE.md](./ARCHITECTURE.md).

## Development

To set up a development environment:

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install development dependencies
pip install -r requirements-dev.txt

# 3. Run tests
pytest tests/

# 4. Format code
black .
flake8 .

# 5. Build documentation
See DEVELOPMENT.md for details
```

For more details, see [DEVELOPMENT.md](./DEVELOPMENT.md).

## Roadmap

Future enhancements planned:
- REST API layer
- Web dashboard for information browsing
- Extended medical imaging support
- Enhanced AI model integration options
- Clinical workflow integration

---

**Last Updated**: January 25, 2026
**Version**: 1.0
**Status**: Active Development
