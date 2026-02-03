#!/usr/bin/env python3
"""
Script to generate short, accurate, and objective README files for all recognizers.
"""

import sys
from pathlib import Path

# Module configurations
MODULES = {
    "medical_symptom": {
        "name": "Medical Symptom Identifier",
        "entity": "symptom",
        "cli": "medical_symptom_cli.py"
    },
    "medical_test": {
        "name": "Medical Test Identifier", 
        "entity": "medical test",
        "cli": "medical_test_cli.py"
    },
    "medical_specialty": {
        "name": "Medical Specialty Identifier",
        "entity": "medical specialty",
        "cli": "medical_specialty_cli.py"
    },
    "medical_supplement": {
        "name": "Medical Supplement Identifier",
        "entity": "medical supplement",
        "cli": "medical_supplement_cli.py"
    },
    "medical_vaccine": {
        "name": "Medical Vaccine Identifier",
        "entity": "medical vaccine",
        "cli": "medical_vaccine_cli.py"
    },
    "medical_procedure": {
        "name": "Medical Procedure Identifier",
        "entity": "medical procedure",
        "cli": "medical_procedure_cli.py"
    },
    "medical_pathogen": {
        "name": "Medical Pathogen Identifier",
        "entity": "medical pathogen",
        "cli": "medical_pathogen_cli.py"
    },
    "medical_device": {
        "name": "Medical Device Identifier",
        "entity": "medical device",
        "cli": "medical_device_cli.py"
    },
    "medical_condition": {
        "name": "Medical Condition Identifier",
        "entity": "medical condition",
        "cli": "medical_condition_cli.py"
    },
    "medical_coding": {
        "name": "Medical Coding Identifier",
        "entity": "medical coding system",
        "cli": "medical_coding_cli.py"
    },
    "medical_abbreviation": {
        "name": "Medical Abbreviation Identifier",
        "entity": "medical abbreviation",
        "cli": "medical_abbreviation_cli.py"
    },
    "imaging_finding": {
        "name": "Imaging Finding Identifier",
        "entity": "imaging finding",
        "cli": "imaging_finding_cli.py"
    },
    "genetic_variant": {
        "name": "Genetic Variant Identifier",
        "entity": "genetic variant",
        "cli": "genetic_variant_cli.py"
    },
    "lab_unit": {
        "name": "Lab Unit Identifier",
        "entity": "laboratory unit",
        "cli": "lab_unit_cli.py"
    },
    "clinical_sign": {
        "name": "Clinical Sign Identifier",
        "entity": "clinical sign",
        "cli": "clinical_sign_cli.py"
    },
    "medication_class": {
        "name": "Medication Class Identifier",
        "entity": "medication class",
        "cli": "medication_class_cli.py"
    }
}

def generate_short_readme(module_key, config):
    """Generate short, accurate, and objective README content."""
    
    entity = config["entity"]
    cli_file = config["cli"]
    name = config["name"]
    
    # Capitalize first letter for title
    entity_title = entity[0].upper() + entity[1:] if entity else entity
    
    readme_content = f"""# {name}

Identifies whether a given name is a recognized {entity} in medical literature.

## Purpose

Quick identification filter before calling expensive LLMs to minimize hallucinations and computational costs.

## Usage

```bash
python {cli_file} "example {entity.replace(' ', '_')}"
```

## Output

```json
{{
  "identification": {{
    "name": "Example {entity_title}",
    "is_well_known": true,
    "recognition_confidence": "high",
    "medical_literature_reference": "Recognized in major medical databases and literature"
  }},
  "summary": "Example {entity_title} is a recognized {entity} in medical literature",
  "data_available": true
}}
```

## Installation

```bash
cd /Users/csv610/Projects/LiteLLM
pip install -r requirements.txt
```

## Testing

```bash
python test_{module_key}_identifier.py
```

## Disclaimer

For identification purposes only. Not a substitute for professional medical advice.
"""
    
    return readme_content

def main():
    """Generate short README files for all recognizers."""
    print("Generating short, accurate, and objective README files...")
    
    recognizers_dir = Path(__file__).parent
    updated_files = []
    
    for module_key, config in MODULES.items():
        module_dir = recognizers_dir / module_key
        readme_file = module_dir / "README.md"
        
        print(f"Creating {module_key}/README.md...")
        
        readme_content = generate_short_readme(module_key, config)
        
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        updated_files.append(readme_file)
        print(f"✓ Created {readme_file}")
    
    print(f"\n✅ Generated {len(updated_files)} short README files")
    print("\nAll README files now:")
    print("- Are short and concise")
    print("- Focus on the core objective")
    print("- Provide accurate usage examples")
    print("- Include clear output format")
    print("- Have essential installation/testing info")
    print("- Include appropriate disclaimer")

if __name__ == "__main__":
    main()
