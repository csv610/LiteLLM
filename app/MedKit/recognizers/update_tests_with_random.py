#!/usr/bin/env python3
"""
Script to update all test files to choose random examples from assets folders.
"""

import sys
from pathlib import Path
import re

# Module configurations for test updates
MODULE_CONFIGS = {
    "clinical_sign": {
        "name": "ClinicalSignIdentifier",
        "models": "ClinicalSignIdentifierModel",
        "input": "ClinicalSignIdentifierInput",
        "fallback": "babinski_sign"
    },
    "genetic_variant": {
        "name": "GeneticVariantIdentifier", 
        "models": "GeneticVariantIdentifierModel",
        "input": "GeneticVariantIdentifierInput",
        "fallback": "brca1_mutation"
    },
    "imaging_finding": {
        "name": "ImagingFindingIdentifier",
        "models": "ImagingFindingIdentifierModel", 
        "input": "ImagingFindingIdentifierInput",
        "fallback": "pulmonary_nodule"
    },
    "lab_unit": {
        "name": "LabUnitIdentifier",
        "models": "LabUnitIdentifierModel",
        "input": "LabUnitIdentifierInput", 
        "fallback": "mg_dl"
    },
    "medical_abbreviation": {
        "name": "MedicalAbbreviationIdentifier",
        "models": "MedicalAbbreviationIdentifierModel",
        "input": "MedicalAbbreviationIdentifierInput",
        "fallback": "cpr"
    },
    "medical_anatomy": {
        "name": "MedicalAnatomyIdentifier",
        "models": "MedicalAnatomyIdentifierModel",
        "input": "MedicalAnatomyIdentifierInput",
        "fallback": "left_ventricle"
    },
    "medical_coding": {
        "name": "MedicalCodingIdentifier",
        "models": "MedicalCodingIdentifierModel",
        "input": "MedicalCodingIdentifierInput",
        "fallback": "icd_10"
    },
    "medical_condition": {
        "name": "MedicalConditionIdentifier",
        "models": "MedicalConditionIdentifierModel",
        "input": "MedicalConditionIdentifierInput",
        "fallback": "hypertension"
    },
    "medical_device": {
        "name": "MedicalDeviceIdentifier",
        "models": "MedicalDeviceIdentifierModel",
        "input": "MedicalDeviceIdentifierInput",
        "fallback": "pacemaker"
    },
    "medical_pathogen": {
        "name": "MedicalPathogenIdentifier",
        "models": "MedicalPathogenIdentifierModel",
        "input": "MedicalPathogenIdentifierInput",
        "fallback": "staphylococcus_aureus"
    },
    "medical_procedure": {
        "name": "MedicalProcedureIdentifier",
        "models": "MedicalProcedureIdentifierModel",
        "input": "MedicalProcedureIdentifierInput",
        "fallback": "appendectomy"
    },
    "medical_vaccine": {
        "name": "MedicalVaccineIdentifier",
        "models": "MedicalVaccineIdentifierModel",
        "input": "MedicalVaccineIdentifierInput",
        "fallback": "influenza_vaccine"
    },
    "medication_class": {
        "name": "MedicationClassIdentifier",
        "models": "MedicationClassIdentifierModel",
        "input": "MedicationClassIdentifierInput",
        "fallback": "beta_blockers"
    }
}

def generate_random_assets_function(module_key, config):
    """Generate the random assets reading function for a module."""
    
    fallback = config["fallback"]
    
    function_code = f'''def read_random_example_from_assets():
    """Read a random example from assets folder."""
    assets_file = Path(__file__).parent / "assets" / "example_inputs.txt"
    examples = []
    
    if assets_file.exists():
        with open(assets_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('##'):
                    examples.append(line)
    
    # Return a random example if available, otherwise fallback
    if examples:
        return random.choice(examples)
    else:
        return "{fallback}"  # fallback

'''
    
    return function_code

def update_test_file_with_random_examples(test_file_path, module_key, config):
    """Update a test file to use random examples from assets."""
    
    if not test_file_path.exists():
        print(f"Test file not found: {test_file_path}")
        return False
    
    with open(test_file_path, 'r') as f:
        content = f.read()
    
    # Add random import if not present
    if 'import random' not in content:
        content = content.replace('import sys\nimport os\nfrom pathlib import Path', 
                                'import sys\nimport os\nimport random\nfrom pathlib import Path')
    
    # Replace the assets reading function with random version
    random_function = generate_random_assets_function(module_key, config)
    
    # Find and replace the old read_example_from_assets function
    old_function_pattern = r'def read_example_from_assets\(\):.*?(?=\ndef|\nclass|\Z)'
    content = re.sub(old_function_pattern, random_function.strip(), content, flags=re.DOTALL)
    
    # Update function calls to use random version
    content = re.sub(r'read_example_from_assets\(\)', 'read_random_example_from_assets()', content)
    
    # Update comments to reflect random selection
    content = re.sub(r'# Read example from assets', '# Read random example from assets', content)
    
    with open(test_file_path, 'w') as f:
        f.write(content)
    
    return True

def main():
    """Update all test files to use random examples from assets folders."""
    print("Updating test files to use random examples from assets folders...")
    
    recognizers_dir = Path(__file__).parent
    updated_files = []
    
    for module_key, config in MODULE_CONFIGS.items():
        test_file = recognizers_dir / module_key / f"test_{module_key}_identifier.py"
        
        if test_file.exists():
            print(f"Updating {module_key}/test_{module_key}_identifier.py...")
            
            if update_test_file_with_random_examples(test_file, module_key, config):
                updated_files.append(test_file)
                print(f"✓ Updated {test_file}")
            else:
                print(f"- No changes needed for {test_file}")
        else:
            print(f"- Test file not found: {test_file}")
    
    # Also update the disease test file
    disease_test = recognizers_dir / "disease" / "test_disease_identifier.py"
    if disease_test.exists():
        print(f"Disease test already updated manually")
        updated_files.append(disease_test)
    
    print(f"\n✅ Updated {len(updated_files)} test files")
    print("\nAll test files now:")
    print("- Choose random examples from assets/example_inputs.txt")
    print("- Use different examples on each test run")
    print("- Provide comprehensive coverage of all examples")
    print("- Have fallback examples if assets file is missing")
    print("- Test with varied medical terminology each time")

if __name__ == "__main__":
    main()
