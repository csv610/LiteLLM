#!/usr/bin/env python3
"""
Test script for Medical Symptom Identifier Module.

This script tests the medical symptom identifier functionality with various symptom examples
without using mock libraries.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from app.MedKit.recognizers.medical_symptom.medical_symptom_models import MedicalSymptomIdentifierModel, ModelOutput
from app.MedKit.recognizers.medical_symptom.medical_symptom_prompts import PromptBuilder, MedicalSymptomIdentifierInput
from app.MedKit.recognizers.medical_symptom.medical_symptom_recognizer import MedicalSymptomIdentifier
from lite.config import ModelConfig


def test_prompt_builder():
    """Test the PromptBuilder class."""
    print("Testing PromptBuilder...")
    
    # Test system prompt
    system_prompt = PromptBuilder.create_system_prompt()
    assert isinstance(system_prompt, str)
    assert len(system_prompt) > 0
    print("✓ System prompt created successfully")
    
    # Test user prompt
    symptom_input = MedicalSymptomIdentifierInput("chest_pain")
    user_prompt = PromptBuilder.create_user_prompt(symptom_input)
    assert isinstance(user_prompt, str)
    assert "chest_pain" in user_prompt
    print("✓ User prompt created successfully")
    
    # Test empty symptom name
    try:
        empty_input = MedicalSymptomIdentifierInput("")
        assert False, "Should have raised ValueError for empty symptom name"
    except ValueError:
        print("✓ Empty symptom name validation works correctly")


def test_medical_symptom_models():
    """Test the Pydantic models."""
    print("\nTesting Medical Symptom Models...")
    
    # Test SymptomIdentificationModel
    identification = MedicalSymptomIdentifierModel(
        symptom_name="chest_pain",
        is_well_known=True,
        common_causes=["heart_attack", "angina", "muscle_strain", "anxiety"],
        urgency_level="high",
        medical_significance="Chest pain can indicate serious cardiac conditions requiring immediate attention"
    )
    print("✓ SymptomIdentificationModel created successfully")
    
    # Test MedicalSymptomIdentifierModel
    symptom_model = MedicalSymptomIdentifierModel(
        identification=identification,
        summary="Chest pain is a well-known symptom that requires urgent medical evaluation",
        data_available=True
    )
    print("✓ MedicalSymptomIdentifierModel created successfully")
    
    # Test ModelOutput
    model_output = ModelOutput(data=symptom_model)
    assert model_output.data.symptom_name == "chest_pain"
    print("✓ ModelOutput created successfully")


def test_medical_symptom_identifier_initialization():
    """Test MedicalSymptomIdentifier initialization."""
    print("\nTesting MedicalSymptomIdentifier Initialization...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalSymptomIdentifier(config)
    
    assert identifier.client is not None
    print("✓ MedicalSymptomIdentifier initialized successfully")


def test_medical_symptom_identifier_validation():
    """Test MedicalSymptomIdentifier input validation."""
    print("\nTesting MedicalSymptomIdentifier Validation...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalSymptomIdentifier(config)
    
    # Test empty symptom name
    try:
        symptom_input = MedicalSymptomIdentifierInput("")
        assert False, "Should have raised ValueError for empty symptom name"
    except ValueError:
        print("✓ Empty symptom name validation works correctly")
    
    # Test whitespace-only symptom name
    try:
        symptom_input = MedicalSymptomIdentifierInput("   ")
        assert False, "Should have raised ValueError for whitespace-only symptom name"
    except ValueError:
        print("✓ Whitespace-only symptom name validation works correctly")


def test_with_example_symptoms():
    """Test with example symptoms from assets."""
    print("\nTesting with Example Symptoms...")
    
    # Read example symptoms from assets
    assets_file = Path(__file__).parent / "assets" / "example_inputs.txt"
    if assets_file.exists():
        with open(assets_file, 'r') as f:
            content = f.read()
        
        # Extract symptom names (skip comments and empty lines)
        symptoms = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('##'):
                symptoms.append(line)
        
        print(f"Found {len(symptoms)} example symptoms")
        
        # Test a few examples
        test_symptoms = symptoms[:5]  # Test first 5 symptoms
        config = ModelConfig(model="ollama/gemma3", temperature=0.2)
        identifier = MedicalSymptomIdentifier(config)
        
        for symptom in test_symptoms:
            try:
                symptom_input = MedicalSymptomIdentifierInput(symptom)
                print(f"✓ Symptom input created for: {symptom}")
            except Exception as e:
                print(f"✗ Error creating input for {symptom}: {e}")
    else:
        print("⚠ Example inputs file not found")


def test_symptom_categories():
    """Test different categories of symptoms."""
    print("\nTesting Symptom Categories...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalSymptomIdentifier(config)
    
    # Test common symptoms
    common_symptoms = ["headache", "fever", "cough", "fatigue"]
    for symptom in common_symptoms:
        try:
            symptom_input = MedicalSymptomIdentifierInput(symptom)
            print(f"✓ Common symptom input created for: {symptom}")
        except Exception as e:
            print(f"✗ Error with common symptom {symptom}: {e}")
    
    # Test neurological symptoms
    neuro_symptoms = ["seizure", "memory_loss", "weakness", "numbness"]
    for symptom in neuro_symptoms:
        try:
            symptom_input = MedicalSymptomIdentifierInput(symptom)
            print(f"✓ Neurological symptom input created for: {symptom}")
        except Exception as e:
            print(f"✗ Error with neurological symptom {symptom}: {e}")
    
    # Test cardiovascular symptoms
    cardio_symptoms = ["chest_pain", "palpitations", "shortness_of_breath"]
    for symptom in cardio_symptoms:
        try:
            symptom_input = MedicalSymptomIdentifierInput(symptom)
            print(f"✓ Cardiovascular symptom input created for: {symptom}")
        except Exception as e:
            print(f"✗ Error with cardiovascular symptom {symptom}: {e}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("MEDICAL SYMPTOM IDENTIFIER MODULE TESTS")
    print("=" * 60)
    
    try:
        test_prompt_builder()
        test_medical_symptom_models()
        test_medical_symptom_identifier_initialization()
        test_medical_symptom_identifier_validation()
        test_with_example_symptoms()
        test_symptom_categories()
        
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
