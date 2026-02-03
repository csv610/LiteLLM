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
    """Test the PromptBuilder class."""
    print("Testing PromptBuilder...")
    
    # Read random example from assets
    example_disease = read_random_example_from_assets()
    
    # Test system prompt
    system_prompt = PromptBuilder.create_system_prompt()
    assert isinstance(system_prompt, str)
    assert len(system_prompt) > 0
    print("✓ System prompt created successfully")
    
    # Test user prompt
    disease_input = DiseaseIdentifierInput(example_disease)
    user_prompt = PromptBuilder.create_user_prompt(disease_input)
    assert isinstance(user_prompt, str)
    assert example_disease in user_prompt
    print("✓ User prompt created successfully")
    
    # Test empty disease name
    try:
        empty_input = DiseaseIdentifierInput("")
        assert False, "Should have raised ValueError for empty disease name"
    except ValueError:
        print("✓ Empty disease name validation works correctly")


def test_disease_identifier_models():
    """Test the Pydantic models."""
    print("\nTesting Disease Identifier Models...")
    
    # Read random example from assets
    example_disease = read_random_example_from_assets()
    
    # Test DiseaseIdentificationModel
    identification = DiseaseIdentifierModel(
        disease_name=example_disease,
        is_well_known=True,
        common_symptoms=["symptom1", "symptom2"],
        prevalence="Common",
        medical_significance="Significant"
    )
    print("✓ DiseaseIdentificationModel created successfully")
    
    # Test DiseaseIdentifierModel
    disease_model = DiseaseIdentifierModel(
        identification=identification,
        summary=f"{example_disease} is a well-known disease",
        data_available=True
    )
    print("✓ DiseaseIdentifierModel created successfully")
    
    # Test ModelOutput
    model_output = ModelOutput(data=disease_model)
    assert model_output.data.disease_name == example_disease
    print("✓ ModelOutput created successfully")


def test_disease_identifier_initialization():
    """Test DiseaseIdentifier initialization."""
    print("\nTesting DiseaseIdentifier Initialization...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = DiseaseIdentifier(config)
    
    assert identifier.client is not None
    print("✓ DiseaseIdentifier initialized successfully")


def test_disease_identifier_validation():
    """Test DiseaseIdentifier input validation."""
    print("\nTesting DiseaseIdentifier Validation...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = DiseaseIdentifier(config)
    
    # Test empty disease name
    try:
        # This should not raise an error as validation happens in the input model
        disease_input = DiseaseIdentifierInput("")
        assert False, "Should have raised ValueError for empty disease name"
    except ValueError:
        print("✓ Empty disease name validation works correctly")
    
    # Test whitespace-only disease name
    try:
        disease_input = DiseaseIdentifierInput("   ")
        assert False, "Should have raised ValueError for whitespace-only disease name"
    except ValueError:
        print("✓ Whitespace-only disease name validation works correctly")


def test_with_example_diseases():
    """Test with example diseases from assets."""
    print("\nTesting with Example Diseases...")
    
    # Read example diseases from assets
    assets_file = Path(__file__).parent / "assets" / "example_inputs.txt"
    if assets_file.exists():
        with open(assets_file, 'r') as f:
            content = f.read()
        
        # Extract disease names (skip comments and empty lines)
        diseases = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('##'):
                diseases.append(line)
        
        print(f"Found {len(diseases)} example diseases")
        
        # Test a few examples
        test_diseases = diseases[:5]  # Test first 5 diseases
        config = ModelConfig(model="ollama/gemma3", temperature=0.2)
        identifier = DiseaseIdentifier(config)
        
        for disease in test_diseases:
            try:
                disease_input = DiseaseIdentifierInput(disease)
                print(f"✓ Disease input created for: {disease}")
            except Exception as e:
                print(f"✗ Error creating input for {disease}: {e}")
    else:
        print("⚠ Example inputs file not found")


def main():
    """Run all tests."""
    print("=" * 60)
    print("DISEASE IDENTIFIER MODULE TESTS")
    print("=" * 60)
    
    try:
        test_prompt_builder()
        test_disease_identifier_models()
        test_disease_identifier_initialization()
        test_disease_identifier_validation()
        test_with_example_diseases()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
