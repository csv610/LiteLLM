# Medical Test Information Generator

## Why This Matters

Medical tests are ordered billions of times annually, yet patients and clinicians often lack accessible, standardized information about what these tests measure, how to prepare, and how to interpret results. This gap leads to:

- **Patient anxiety** from unclear test procedures and expectations
- **Clinical inefficiency** from repeated basic questions about common tests
- **Medical errors** from improper test preparation or result interpretation
- **Healthcare costs** from cancelled tests due to preparation failures

The Medical Test Information Generator addresses these problems by providing instant, comprehensive documentation for medical tests that serves both clinical decision support and patient education needs.

## Overview

Generate medical test documentation using structured data models and the MedKit AI client with schema-aware prompting.

This module creates detailed information about medical tests and diagnostics for clinicians and patient education, standardizing access to critical medical testing information.

## Quick Start

```python
from medical_test_info import MedicalTestInfoGenerator
from pathlib import Path

# Generate test information
generator = MedicalTestInfoGenerator()
test_info = generator.generate_text("blood glucose test")

# Access different sections
print(test_info.test_name)
print(test_info.test_purpose.primary_purpose)
print(test_info.results_information.normal_range)

# Generate and save to file
test_info = generator.generate_text("complete blood count")
saved_path = generator.save(test_info, Path("outputs/"))  # Directory, not file path
```

## Common Uses

1. Generate patient education about upcoming tests
2. Provide clinical reference for test interpretation
3. Create test preparation instructions
4. Understand normal and abnormal values
5. Support clinical decision making
6. Create test ordering guidance for clinicians

## Coverage Areas

- Test identification and names
- Purpose and indications
- When tests are ordered
- Preparation requirements
- Sample collection methods
- Test procedures and techniques
- Normal and abnormal values
- Clinical interpretation
- Complications and risks
- Cost and availability

## Command Line Interface

```bash
python medical_test_info_cli.py -i "test name" [-o "output_path"]
```

### Arguments

- `-i, --test` (required): The name of the medical test to generate information for
- `-o, --output` (optional): The path to save the output JSON file

## Configuration

The generator uses a `Config` class with the following options:

- `enable_cache`: Enable/disable caching of results (default: True)
- `verbosity`: Logging level (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG)
- `db_path`: Path to LMDB storage database

## Output

Generated test information is saved as JSON and includes:

- Test name and alternative names
- Purpose and clinical use
- Test indications and when it is ordered
- Sample requirements and collection procedures
- Test methodology and technology
- Normal reference ranges and result interpretation
- Preparatory requirements and restrictions
- Risks, benefits, and limitations
- Cost and availability information
- Results interpretation and follow-up actions
