#!/usr/bin/env python3
"""
Script to update all test files to read examples from their assets folders.
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

def generate_assets_reading_function(module_key, config):
    """Generate the assets reading function for a module."""
    
    fallback = config["fallback"]
    input_class = config["input"]
    
    function_code = f'''def read_example_from_assets():
    """Read first example from assets folder."""
    assets_file = Path(__file__).parent / "assets" / "example_inputs.txt"
    example = "{fallback}"  # fallback
    
    if assets_file.exists():
        with open(assets_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('##'):
                    example = line
                    break
    
    return example

'''
    
    return function_code

def update_test_file_with_assets(test_file_path, module_key, config):
    """Update a test file to read examples from assets."""
    
    if not test_file_path.exists():
        print(f"Test file not found: {test_file_path}")
        return False
    
    with open(test_file_path, 'r') as f:
        content = f.read()
    
    # Add the assets reading function after imports
    assets_function = generate_assets_reading_function(module_key, config)
    
    # Find where to insert the function (after imports, before first test function)
    lines = content.split('\n')
    insert_index = 0
    
    for i, line in enumerate(lines):
        if line.startswith('def ') and 'test_' in line:
            insert_index = i
            break
    
    # Insert the assets reading function
    lines.insert(insert_index, assets_function)
    
    # Update test_prompt_builder function to use assets
    updated_content = '\n'.join(lines)
    
    # Replace hardcoded examples with assets reading
    # Pattern to find hardcoded examples in test_prompt_builder
    pattern = r'disease_input = DiseaseIdentifierInput\("([^"]+)"\)'
    replacement = f'example = read_example_from_assets()\n    disease_input = DiseaseIdentifierInput(example)'
    
    # More general pattern for any input class
    general_pattern = r'(\w+_input) = (\w+)\("([^"]+)"\)'
    general_replacement = r'example = read_example_from_assets()\n    \1 = \2(example)'
    
    # Apply replacements
    updated_content = re.sub(general_pattern, general_replacement, updated_content)
    
    # Update assertions to use the example variable
    updated_content = re.sub(r'assert "([^"]+)" in user_prompt', r'assert example in user_prompt', updated_content)
    
    # Update model tests to use assets as well
    model_pattern = r'identification = (\w+)\(\s*name="([^"]+)",'
    model_replacement = r'example = read_example_from_assets()\n    identification = \1(\n        name=example,'
    
    updated_content = re.sub(model_pattern, model_replacement, updated_content)
    
    # Update model assertions
    updated_content = re.sub(r'assert model_output\.data\.name == "([^"]+)"', r'assert model_output.data.name == example', updated_content)
    
    with open(test_file_path, 'w') as f:
        f.write(updated_content)
    
    return True

def main():
    """Update all test files to read examples from assets folders."""
    print("Updating test files to read examples from assets folders...")
    
    recognizers_dir = Path(__file__).parent
    updated_files = []
    
    for module_key, config in MODULE_CONFIGS.items():
        test_file = recognizers_dir / module_key / f"test_{module_key}_identifier.py"
        
        if test_file.exists():
            print(f"Updating {module_key}/test_{module_key}_identifier.py...")
            
            if update_test_file_with_assets(test_file, module_key, config):
                updated_files.append(test_file)
                print(f"✓ Updated {test_file}")
            else:
                print(f"- No changes needed for {test_file}")
        else:
            print(f"- Test file not found: {test_file}")
    
    # Also update the disease test file
    disease_test = recognizers_dir / "disease" / "test_disease_identifier.py"
    if disease_test.exists():
        print(f"Updating disease/test_disease_identifier.py...")
        # This was already updated manually
        updated_files.append(disease_test)
        print(f"✓ {disease_test} already updated")
    
    print(f"\n✅ Updated {len(updated_files)} test files")
    print("\nAll test files now:")
    print("- Read examples from assets/example_inputs.txt")
    print("- Use real medical terminology from assets")
    print("- Have fallback examples if assets file is missing")
    print("- Test with actual domain-specific examples")

if __name__ == "__main__":
    main()
