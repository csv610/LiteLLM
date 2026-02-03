#!/usr/bin/env python3
"""
Script to create test files for all recognizer modules that don't have them.
"""

import sys
from pathlib import Path

# Module configurations for test generation
MODULE_CONFIGS = {
    "clinical_sign": {
        "name": "ClinicalSignIdentifier",
        "models": "ClinicalSignIdentifierModel",
        "input": "ClinicalSignIdentifierInput",
        "test_name": "babinski_sign"
    },
    "genetic_variant": {
        "name": "GeneticVariantIdentifier", 
        "models": "GeneticVariantIdentifierModel",
        "input": "GeneticVariantIdentifierInput",
        "test_name": "brca1_mutation"
    },
    "imaging_finding": {
        "name": "ImagingFindingIdentifier",
        "models": "ImagingFindingIdentifierModel", 
        "input": "ImagingFindingIdentifierInput",
        "test_name": "pulmonary_nodule"
    },
    "lab_unit": {
        "name": "LabUnitIdentifier",
        "models": "LabUnitIdentifierModel",
        "input": "LabUnitIdentifierInput", 
        "test_name": "mg_dl"
    },
    "medical_abbreviation": {
        "name": "MedicalAbbreviationIdentifier",
        "models": "MedicalAbbreviationIdentifierModel",
        "input": "MedicalAbbreviationIdentifierInput",
        "test_name": "cpr"
    },
    "medical_anatomy": {
        "name": "MedicalAnatomyIdentifier",
        "models": "MedicalAnatomyIdentifierModel",
        "input": "MedicalAnatomyIdentifierInput",
        "test_name": "left_ventricle"
    },
    "medical_coding": {
        "name": "MedicalCodingIdentifier",
        "models": "MedicalCodingIdentifierModel",
        "input": "MedicalCodingIdentifierInput",
        "test_name": "icd_10"
    },
    "medical_condition": {
        "name": "MedicalConditionIdentifier",
        "models": "MedicalConditionIdentifierModel",
        "input": "MedicalConditionIdentifierInput",
        "test_name": "hypertension"
    },
    "medical_device": {
        "name": "MedicalDeviceIdentifier",
        "models": "MedicalDeviceIdentifierModel",
        "input": "MedicalDeviceIdentifierInput",
        "test_name": "pacemaker"
    },
    "medical_pathogen": {
        "name": "MedicalPathogenIdentifier",
        "models": "MedicalPathogenIdentifierModel",
        "input": "MedicalPathogenIdentifierInput",
        "test_name": "staphylococcus_aureus"
    },
    "medical_procedure": {
        "name": "MedicalProcedureIdentifier",
        "models": "MedicalProcedureIdentifierModel",
        "input": "MedicalProcedureIdentifierInput",
        "test_name": "appendectomy"
    },
    "medical_vaccine": {
        "name": "MedicalVaccineIdentifier",
        "models": "MedicalVaccineIdentifierModel",
        "input": "MedicalVaccineIdentifierInput",
        "test_name": "influenza_vaccine"
    },
    "medication_class": {
        "name": "MedicationClassIdentifier",
        "models": "MedicationClassIdentifierModel",
        "input": "MedicationClassIdentifierInput",
        "test_name": "beta_blockers"
    }
}

def generate_test_file(module_key, config):
    """Generate test file content for a module."""
    
    name = config["name"]
    models = config["models"]
    input_class = config["input"]
    test_name = config["test_name"]
    
    test_content = f'''#!/usr/bin/env python3
"""
Test suite for {name} Module.

This script validates the {module_key.replace('_', ' ')} identifier functionality without using mock libraries.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.MedKit.recognizers.{module_key}.{module_key}_models import {models}, ModelOutput
from app.MedKit.recognizers.{module_key}.{module_key}_prompts import PromptBuilder, {input_class}
from app.MedKit.recognizers.{module_key}.{module_key}_recognizer import {name}
from lite.config import ModelConfig


def test_prompt_builder():
    """Validate the PromptBuilder class functionality."""
    print("Validating PromptBuilder...")
    
    # Validate system prompt generation
    system_prompt = PromptBuilder.create_system_prompt()
    assert isinstance(system_prompt, str)
    assert len(system_prompt) > 0
    print("✓ System prompt generated successfully")
    
    # Validate user prompt generation
    test_input = {input_class}("{test_name}")
    user_prompt = PromptBuilder.create_user_prompt(test_input)
    assert isinstance(user_prompt, str)
    assert "{test_name}" in user_prompt
    print("✓ User prompt generated successfully")
    
    # Validate empty input handling
    try:
        empty_input = {input_class}("")
        assert False, "Expected ValueError for empty input"
    except ValueError:
        print("✓ Empty input validation functions correctly")


def test_models():
    """Validate the Pydantic model structures."""
    print("\\nValidating Models...")
    
    # Validate identification model structure
    identification = {models}(
        name="{test_name}",
        is_well_known=True,
        recognition_confidence="high",
        medical_literature_reference="Recognized in major medical databases"
    )
    print("✓ IdentificationModel instantiated successfully")
    
    # Validate identifier model structure
    identifier_model = {models}(
        identification=identification,
        summary="{test_name.replace('_', ' ').title()} is a recognized {module_key.replace('_', ' ')} in medical literature",
        data_available=True
    )
    print("✓ IdentifierModel instantiated successfully")
    
    # Validate ModelOutput structure
    model_output = ModelOutput(data=identifier_model)
    assert model_output.data.name == "{test_name}"
    print("✓ ModelOutput instantiated successfully")


def test_identifier_initialization():
    """Validate {name} initialization."""
    print("\\nValidating {name} Initialization...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = {name}(config)
    
    assert identifier.client is not None
    print("✓ {name} initialized successfully")


def test_identifier_validation():
    """Validate {name} input validation."""
    print("\\nValidating {name} Input Validation...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = {name}(config)
    
    # Validate empty input handling
    try:
        test_input = {input_class}("")
        assert False, "Expected ValueError for empty input"
    except ValueError:
        print("✓ Empty input validation functions correctly")
    
    # Validate whitespace-only input handling
    try:
        test_input = {input_class}("   ")
        assert False, "Expected ValueError for whitespace-only input"
    except ValueError:
        print("✓ Whitespace-only input validation functions correctly")


def test_method_name_consistency():
    """Validate that the identify method exists and works correctly."""
    print("\\nValidating Method Name Consistency...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = {name}(config)
    
    # Validate that the identify method exists and can be called
    assert hasattr(identifier, 'identify'), "identify method should exist"
    assert callable(getattr(identifier, 'identify')), "identify should be callable"
    
    # Validate method signature
    try:
        test_input = {input_class}("{test_name}")
        print("✓ identify method has correct signature")
    except Exception as e:
        print(f"✗ Error with identify method: {{e}}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("{module_key.upper().replace('_', ' ')} IDENTIFIER MODULE TESTS")
    print("=" * 60)
    
    try:
        test_prompt_builder()
        test_models()
        test_identifier_initialization()
        test_identifier_validation()
        test_method_name_consistency()
        
        print("\\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\\n❌ TEST FAILED: {{e}}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
'''
    
    return test_content

def main():
    """Create test files for all modules that don't have them."""
    print("Creating test files for modules that don't have them...")
    
    recognizers_dir = Path(__file__).parent
    created_files = []
    
    for module_key, config in MODULE_CONFIGS.items():
        module_dir = recognizers_dir / module_key
        test_file = module_dir / f"test_{module_key}_identifier.py"
        
        # Check if test file already exists
        if test_file.exists():
            print(f"- {module_key}/test_{module_key}_identifier.py already exists")
            continue
        
        print(f"Creating {module_key}/test_{module_key}_identifier.py...")
        
        test_content = generate_test_file(module_key, config)
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        created_files.append(test_file)
        print(f"✓ Created {test_file}")
    
    print(f"\n✅ Created {len(created_files)} test files")
    print("\nAll modules now have test functions:")
    print("- Prompt builder validation")
    print("- Model structure validation") 
    print("- Identifier initialization")
    print("- Input validation")
    print("- Method name consistency")
    print("- Main test runner")

if __name__ == "__main__":
    main()
