# Surgical Tool Information Generator

A command-line tool that generates comprehensive information about surgical instruments and tools using structured language model prompting.

## Overview

The Surgical Tool Information Generator retrieves and formats detailed information about surgical instruments including descriptions, specifications, clinical applications, safety considerations, maintenance protocols, and handling techniques. The tool uses a large language model to synthesize information based on a system prompt designed to prioritize clinical accuracy and practical relevance.

## Important Medical Disclaimers

**This tool is for informational and educational purposes only.** It is not a substitute for professional medical training, manufacturer guidelines, or clinical expertise. Users should:

- Consult experienced surgeons and clinical staff before using any surgical tool
- Verify information with manufacturer specifications and product documentation
- Be aware that LLM-generated content may contain inaccuracies or incomplete information
- Understand that actual instrument specifications and sterilization requirements vary by manufacturer
- Always follow institutional protocols and regulatory requirements for surgical instrument use
- Refer to established surgical training programs and credentialed mentors for hands-on instruction
- Report any safety concerns to supervisors and hospital quality/safety departments

The information generated reflects the training data and methodology of the underlying language model and should not be considered definitive, complete, or a replacement for official manufacturer guidelines and clinical training.

## Installation

### Requirements

- Python 3.8+
- LiteClient and related dependencies from the parent project
- Rich library for formatted console output

### Setup

```bash
cd surgical_tool_info
pip install -r requirements.txt
```

## Usage

### Basic Command

Generate information for a single surgical tool:

```bash
python surgical_tool_info_cli.py -i scalpel
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--tool` | `-i` | **Required.** Name of the surgical tool | — |
| `--output` | `-o` | Path to save output JSON file | Auto-generated |
| `--output-dir` | `-d` | Directory for output files | `outputs` |
| `--model` | `-m` | Language model to use | `ollama/gemma3` |
| `--verbosity` | `-v` | Logging level (0-4) | `2` |

### Examples

Save to a specific file:
```bash
python surgical_tool_info_cli.py -i "surgical forceps" -o forceps_info.json
```

Use a different model:
```bash
python surgical_tool_info_cli.py -i retractor -m "ollama/llama2"
```

Increase logging verbosity:
```bash
python surgical_tool_info_cli.py -i "needle holder" -v 4
```

Save to a custom directory:
```bash
python surgical_tool_info_cli.py -i "tissue clamp" -d /path/to/outputs
```

## Features

- **Comprehensive Tool Documentation**: Generates detailed information covering basics, specifications, operational characteristics, safety features, handling techniques, and clinical applications
- **Structured Output**: Results are returned as `SurgicalToolInfo` objects with standardized fields
- **JSON Export**: Save results to files for reference, training, or documentation purposes
- **Formatted Console Output**: Results displayed in organized panels using Rich for readability
- **Configurable Logging**: Multiple verbosity levels for debugging and production use
- **System Prompting**: Uses role-based system prompts to guide accurate, clinically-relevant information generation

## Code Architecture

### Core Components

**`SurgicalToolInfoGenerator`** - Main class for information generation
- Initializes with language model configuration
- Validates tool inputs
- Generates comprehensive surgical tool information
- Handles file output and logging

**Prompt Functions**
- `create_system_prompt()`: Defines the LLM's role as a surgical instrument specialist
- `create_user_prompt(tool)`: Creates structured queries requesting specific information categories

**Output Functions**
- `save()`: Exports results to JSON files with proper directory creation

**CLI Entry Point**
- `app_cli()`: Handles argument parsing, logging configuration, and orchestrates the generation workflow
- `get_user_arguments()`: Parses command-line arguments with validation

## Output Format

The tool generates a `SurgicalToolInfo` object with comprehensive sections (see `surgical_tool_info_models.py` for complete schema):

```json
{
  "tool_basics": {
    "tool_name": "...",
    "alternative_names": "...",
    "tool_category": "...",
    "surgical_specialties": "...",
    "instrument_family": "..."
  },
  "tool_purpose": {
    "primary_purpose": "...",
    "surgical_applications": "...",
    "anatomical_targets": "...",
    "tissue_types": "...",
    "unique_advantages": "..."
  },
  "physical_specifications": {
    "dimensions": "...",
    "weight": "...",
    "material_composition": "...",
    "finish_type": "...",
    "blade_or_tip_specifications": "...",
    "handle_design": "...",
    "sterility_type": "..."
  },
  "operational_characteristics": {
    "cutting_or_grasping_force": "...",
    "actuation_mechanism": "...",
    "precision_level": "...",
    "engagement_depth": "...",
    "working_distance": "..."
  },
  "safety_features": {
    "safety_mechanisms": "...",
    "slip_resistance": "...",
    "wear_considerations": "...",
    "maximum_safe_force": "...",
    "emergency_protocols": "..."
  },
  "preparation": {
    "inspection_requirements": "...",
    "cleaning_protocols": "...",
    "sterilization_requirements": "...",
    "storage_requirements": "..."
  },
  "intraoperative_use": {
    "positioning_in_field": "...",
    "handling_technique": "...",
    "hand_position_requirements": "...",
    "common_movements": "...",
    "ergonomic_considerations": "..."
  },
  "discomfort_risks_and_complications": {
    "surgeon_fatigue_factors": "...",
    "common_handling_errors": "...",
    "tissue_damage_risks": "...",
    "cross_contamination_risks": "..."
  },
  "maintenance_and_care": {
    "post_operative_cleaning": "...",
    "lubrication_schedule": "...",
    "inspection_frequency": "...",
    "wear_indicators": "...",
    "expected_lifespan": "..."
  },
  "sterilization_and_disinfection": {
    "approved_sterilization_methods": "...",
    "incompatible_sterilization": "...",
    "reprocessing_manufacturer_protocols": "..."
  },
  "alternatives_and_comparisons": {
    "similar_alternative_tools": "...",
    "advantages_over_alternatives": "...",
    "when_to_use_this_tool": "...",
    "complementary_tools": "..."
  },
  "historical_context": {
    "invention_history": "...",
    "evolution_timeline": "...",
    "clinical_evidence": "...",
    "current_status": "..."
  },
  "specialty_specific_considerations": {
    "general_surgery_specific": "...",
    "orthopedic_specific": "...",
    "cardiac_specific": "...",
    "neurosurgery_specific": "...",
    "vascular_specific": "...",
    "laparoscopic_considerations": "...",
    "robotic_integration": "..."
  },
  "training_and_certification": {
    "training_requirements": "...",
    "proficiency_indicators": "...",
    "common_learning_mistakes": "...",
    "skill_development_timeline": "...",
    "mentoring_best_practices": "..."
  },
  "regulatory_and_standards": {
    "fda_classification": "...",
    "fda_status": "...",
    "iso_standards": "...",
    "quality_certifications": "..."
  },
  "cost_and_procurement": {
    "single_use_cost": "...",
    "reusable_initial_cost": "...",
    "lifecycle_cost": "...",
    "vendor_options": "...",
    "inventory_recommendations": "..."
  },
  "educational_content": {
    "plain_language_explanation": "...",
    "key_takeaways": "...",
    "common_misconceptions": "...",
    "patient_communication": "..."
  }
}
```

## Logging

Logs are written to `surgical_tool_info.log` in the working directory.

Verbosity levels:
- `0`: CRITICAL only
- `1`: ERROR messages
- `2`: WARNING messages (default)
- `3`: INFO messages
- `4`: DEBUG messages (verbose)

## Limitations

1. **Model Dependency**: Output quality depends on the underlying language model's training data and capabilities
2. **Knowledge Cutoff**: LLM training data has a cutoff date; recent innovations may not be included
3. **No Clinical Validation**: Generated information is not reviewed by surgeons or clinical experts
4. **Manufacturer Variation**: Instruments from different manufacturers may have different specifications and handling requirements
5. **Incomplete Information**: Specialized or newer instruments may have limited coverage in training data
6. **Regulatory Changes**: Medical device regulations and standards evolve; information may become outdated
7. **Context Limitations**: Cannot account for institution-specific protocols or customized instrument configurations

## Best Practices

- Use this tool as a reference and educational aid, not as a replacement for formal training
- Always cross-reference with current manufacturer specifications and institutional guidelines
- Consult with experienced clinical staff and surgical mentors for hands-on training
- Keep records of generation dates for audit and reference purposes
- Update information periodically as surgical techniques and instruments evolve
- Follow your institution's credentialing and competency assessment requirements
- Report any discrepancies between generated information and official guidelines

## Related Files

- `surgical_tool_info_models.py` - Pydantic models for structured tool information
- `surgical_tool_info.log` - Log file (auto-generated)
- `common_surgical_instruments_module.pdf` - Reference documentation

## License

See parent project LICENSE file.
