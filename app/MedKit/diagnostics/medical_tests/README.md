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
from lite.config import ModelConfig
from pathlib import Path

# Generate test information
model_config = ModelConfig(model="ollama/gemma3", temperature=0.7)
generator = MedicalTestInfoGenerator(model_config)
test_info = generator.generate_text("blood glucose test")

# View the results
print(test_info)

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
python medical_test_info_cli.py -i "test name" [-d "output_directory"]
```

### Arguments

- `-i, --test` (required): The name of the medical test to generate information for
- `-d, --output-dir` (optional): Directory for output files (default: outputs)
- `-m, --model` (optional): Model to use for generation (default: ollama/gemma3)
- `-v, --verbosity` (optional): Logging verbosity level 0-4 (default: 2)
- `-s, --structured` (optional): Use structured output format (default: False)

## Configuration

The generator uses `ModelConfig` from the LiteLLM framework:

```python
from lite.config import ModelConfig

# Standard configuration
model_config = ModelConfig(
    model="ollama/gemma3",
    temperature=0.7
)

# Use with the generator
generator = MedicalTestInfoGenerator(model_config)
```

### Available Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | str | `"ollama/gemma3"` | LLM model to use for generation |
| `temperature` | float | `0.7` | Sampling temperature (0.0-2.0) |

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
