#!/usr/bin/env python3
"""
Test script for Disease Identifier Module.

This script tests the disease identifier functionality with various disease examples
without using mock libraries.
"""

import sys
import os
import random
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from app.MedKit.recognizers.disease.disease_identifier_models import DiseaseIdentifierModel, ModelOutput
from app.MedKit.recognizers.disease.disease_identifier_prompts import PromptBuilder, DiseaseIdentifierInput
from app.MedKit.recognizers.disease.disease_recognizer import DiseaseIdentifier
from lite.config import ModelConfig


def read_random_example_from_assets():
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
        return "diabetes_mellitus"  # fallback


def test_prompt_builder():
    """Validate the PromptBuilder class functionality."""
    print("Validating PromptBuilder...")
    
    # Read random example from assets
    example_disease = read_random_example_from_assets()
    
    # Validate system prompt generation
    system_prompt = PromptBuilder.create_system_prompt()
    assert isinstance(system_prompt, str)
    assert len(system_prompt) > 0
    print("✓ System prompt generated successfully")
    
    # Validate user prompt generation
    disease_input = DiseaseIdentifierInput(example_disease)
    user_prompt = PromptBuilder.create_user_prompt(disease_input)
    assert isinstance(user_prompt, str)
    assert example_disease in user_prompt
    print("✓ User prompt generated successfully")
    
    # Validate empty disease name handling
    try:
        empty_input = DiseaseIdentifierInput("")
        assert False, "Expected ValueError for empty disease name"
    except ValueError:
        print("✓ Empty disease name validation functions correctly")


def test_disease_identifier_models():
    """Validate the Pydantic model structures."""
    print("\nValidating Disease Identifier Models...")
    
    # Read random example from assets
    example_disease = read_random_example_from_assets()
    
    # Validate DiseaseIdentificationModel structure (corrected for focused objective)
    identification = DiseaseIdentifierModel(
        disease_name=example_disease,
        is_well_known=True,
        recognition_confidence="high",
        medical_literature_reference="Recognized in major medical databases"
    )
    print("✓ DiseaseIdentificationModel instantiated successfully")
    
    # Validate DiseaseIdentifierModel structure
    disease_model = DiseaseIdentifierModel(
        identification=identification,
        summary=f"{example_disease} is a recognized disease in medical literature",
        data_available=True
    )
    print("✓ DiseaseIdentifierModel instantiated successfully")
    
    # Validate ModelOutput structure
    model_output = ModelOutput(data=disease_model)
    assert model_output.data.disease_name == example_disease
    print("✓ ModelOutput instantiated successfully")


def test_disease_identifier_initialization():
    """Validate DiseaseIdentifier initialization."""
    print("\nValidating DiseaseIdentifier Initialization...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = DiseaseIdentifier(config)
    
    assert identifier.client is not None
    print("✓ DiseaseIdentifier initialized successfully")


def test_method_name_consistency():
    """Validate that the identify method exists and works correctly."""
    print("\nValidating Method Name Consistency...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = DiseaseIdentifier(config)
    
    # Validate that the identify method exists and can be called
    assert hasattr(identifier, 'identify'), "identify method should exist"
    assert callable(getattr(identifier, 'identify')), "identify should be callable"
    
    # Validate method signature
    try:
        example_disease = read_random_example_from_assets()
        result = identifier.identify(example_disease)
        print("✓ identify method has correct signature")
    except Exception as e:
        print(f"✗ Error with identify method: {e}")
        raise


def test_disease_identifier_validation():
    """Validate DiseaseIdentifier input validation."""
    print("\nValidating DiseaseIdentifier Input Validation...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = DiseaseIdentifier(config)
    
    # Validate empty disease name handling
    try:
        disease_input = DiseaseIdentifierInput("")
        assert False, "Expected ValueError for empty disease name"
    except ValueError:
        print("✓ Empty disease name validation functions correctly")
    
    # Validate whitespace-only disease name handling
    try:
        disease_input = DiseaseIdentifierInput("   ")
        assert False, "Expected ValueError for whitespace-only disease name"
    except ValueError:
        print("✓ Whitespace-only disease name validation functions correctly")


def test_with_example_diseases():
    """Validate with random example diseases from assets."""
    print("\nValidating with Example Diseases...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = DiseaseIdentifier(config)
    
    # Validate multiple random examples
    for i in range(3):
        example_disease = read_random_example_from_assets()
        
        try:
            # Validate input creation
            disease_input = DiseaseIdentifierInput(example_disease)
            assert disease_input.name == example_disease
            print(f"✓ Test {i+1}: Input created for {example_disease}")
            
            # Validate actual identification
            result = identifier.identify(example_disease)
            assert result is not None
            assert hasattr(result, 'data')
            print(f"✓ Test {i+1}: Successfully identified {example_disease}")
            
        except Exception as e:
            print(f"✗ Test {i+1}: Error with {example_disease}: {e}")
            raise  # Re-raise to fail the test


def main():
    """Run all validations."""
    print("=" * 60)
    print("DISEASE IDENTIFIER MODULE VALIDATIONS")
    print("=" * 60)
    
    try:
        test_prompt_builder()
        test_disease_identifier_models()
        test_disease_identifier_initialization()
        test_method_name_consistency()
        test_disease_identifier_validation()
        test_with_example_diseases()
        
        print("\n" + "=" * 60)
        print("ALL VALIDATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
