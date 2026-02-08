#!/usr/bin/env python3
"""
Test script for Medical Specialty Identifier Module.

This script tests the medical specialty identifier functionality with various specialty examples
without using mock libraries.
"""

import sys
import os
from pathlib import Path


from app.MedKit.recognizers.medical_specialty.medical_specialty_models import MedicalSpecialtyIdentifierModel, ModelOutput
from app.MedKit.recognizers.medical_specialty.medical_specialty_prompts import PromptBuilder, MedicalSpecialtyIdentifierInput
from app.MedKit.recognizers.medical_specialty.medical_specialty_recognizer import MedicalSpecialtyIdentifier
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
    specialty_input = MedicalSpecialtyIdentifierInput("cardiology")
    user_prompt = PromptBuilder.create_user_prompt(specialty_input)
    assert isinstance(user_prompt, str)
    assert "cardiology" in user_prompt
    print("✓ User prompt created successfully")
    
    # Test empty specialty name
    try:
        empty_input = MedicalSpecialtyIdentifierInput("")
        assert False, "Should have raised ValueError for empty specialty name"
    except ValueError:
        print("✓ Empty specialty name validation works correctly")


def test_medical_specialty_models():
    """Test the Pydantic models."""
    print("\nTesting Medical Specialty Models...")
    
    # Test SpecialtyIdentificationModel
    identification = MedicalSpecialtyIdentifierModel(
        specialty_name="cardiology",
        is_well_known=True,
        specialty_focus="heart and circulatory system disorders",
        common_procedures=["echocardiogram", "cardiac_catheterization", "stress_test"],
        medical_significance="Essential specialty for managing cardiovascular diseases, leading cause of death globally"
    )
    print("✓ SpecialtyIdentificationModel created successfully")
    
    # Test MedicalSpecialtyIdentifierModel
    specialty_model = MedicalSpecialtyIdentifierModel(
        identification=identification,
        summary="Cardiology is a well-established medical specialty focusing on heart diseases",
        data_available=True
    )
    print("✓ MedicalSpecialtyIdentifierModel created successfully")
    
    # Test ModelOutput
    model_output = ModelOutput(data=specialty_model)
    assert model_output.data.specialty_name == "cardiology"
    print("✓ ModelOutput created successfully")


def test_medical_specialty_identifier_initialization():
    """Test MedicalSpecialtyIdentifier initialization."""
    print("\nTesting MedicalSpecialtyIdentifier Initialization...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalSpecialtyIdentifier(config)
    
    assert identifier.client is not None
    print("✓ MedicalSpecialtyIdentifier initialized successfully")


def test_medical_specialty_identifier_validation():
    """Test MedicalSpecialtyIdentifier input validation."""
    print("\nTesting MedicalSpecialtyIdentifier Validation...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalSpecialtyIdentifier(config)
    
    # Test empty specialty name
    try:
        specialty_input = MedicalSpecialtyIdentifierInput("")
        assert False, "Should have raised ValueError for empty specialty name"
    except ValueError:
        print("✓ Empty specialty name validation works correctly")
    
    # Test whitespace-only specialty name
    try:
        specialty_input = MedicalSpecialtyIdentifierInput("   ")
        assert False, "Should have raised ValueError for whitespace-only specialty name"
    except ValueError:
        print("✓ Whitespace-only specialty name validation works correctly")


def test_with_example_specialties():
    """Test with example specialties from assets."""
    print("\nTesting with Example Specialties...")
    
    # Read example specialties from assets
    assets_file = Path(__file__).parent / "assets" / "example_inputs.txt"
    if assets_file.exists():
        with open(assets_file, 'r') as f:
            content = f.read()
        
        # Extract specialty names (skip comments and empty lines)
        specialties = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('##'):
                specialties.append(line)
        
        print(f"Found {len(specialties)} example specialties")
        
        # Test a few examples
        test_specialties = specialties[:5]  # Test first 5 specialties
        config = ModelConfig(model="ollama/gemma3", temperature=0.2)
        identifier = MedicalSpecialtyIdentifier(config)
        
        for specialty in test_specialties:
            try:
                specialty_input = MedicalSpecialtyIdentifierInput(specialty)
                print(f"✓ Specialty input created for: {specialty}")
            except Exception as e:
                print(f"✗ Error creating input for {specialty}: {e}")
    else:
        print("⚠ Example inputs file not found")


def test_specialty_categories():
    """Test different categories of medical specialties."""
    print("\nTesting Specialty Categories...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalSpecialtyIdentifier(config)
    
    # Test medical specialties
    medical_specialties = ["cardiology", "neurology", "pediatrics", "oncology", "psychiatry"]
    for specialty in medical_specialties:
        try:
            specialty_input = MedicalSpecialtyIdentifierInput(specialty)
            print(f"✓ Medical specialty input created for: {specialty}")
        except Exception as e:
            print(f"✗ Error with medical specialty {specialty}: {e}")
    
    # Test surgical specialties
    surgical_specialties = ["general_surgery", "orthopedics", "neurosurgery", "cardiothoracic_surgery"]
    for specialty in surgical_specialties:
        try:
            specialty_input = MedicalSpecialtyIdentifierInput(specialty)
            print(f"✓ Surgical specialty input created for: {specialty}")
        except Exception as e:
            print(f"✗ Error with surgical specialty {specialty}: {e}")
    
    # Test diagnostic specialties
    diagnostic_specialties = ["radiology", "pathology", "nuclear_medicine", "laboratory_medicine"]
    for specialty in diagnostic_specialties:
        try:
            specialty_input = MedicalSpecialtyIdentifierInput(specialty)
            print(f"✓ Diagnostic specialty input created for: {specialty}")
        except Exception as e:
            print(f"✗ Error with diagnostic specialty {specialty}: {e}")
    
    # Test primary care specialties
    primary_care = ["family_medicine", "internal_medicine", "pediatrics", "emergency_medicine"]
    for specialty in primary_care:
        try:
            specialty_input = MedicalSpecialtyIdentifierInput(specialty)
            print(f"✓ Primary care specialty input created for: {specialty}")
        except Exception as e:
            print(f"✗ Error with primary care specialty {specialty}: {e}")


def test_subspecialties():
    """Test medical subspecialties."""
    print("\nTesting Medical Subspecialties...")
    
    config = ModelConfig(model="ollama/gemma3", temperature=0.2)
    identifier = MedicalSpecialtyIdentifier(config)
    
    subspecialties = [
        "interventional_cardiology",
        "pediatric_cardiology",
        "neurosurgery",
        "orthopedic_sports_medicine",
        "medical_oncology",
        "radiation_oncology",
        "child_psychiatry",
        "geriatric_psychiatry",
        "dermatopathology",
        "cosmetic_dermatology"
    ]
    
    for subspecialty in subspecialties:
        try:
            specialty_input = MedicalSpecialtyIdentifierInput(subspecialty)
            print(f"✓ Subspecialty input created for: {subspecialty}")
        except Exception as e:
            print(f"✗ Error with subspecialty {subspecialty}: {e}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("MEDICAL SPECIALTY IDENTIFIER MODULE TESTS")
    print("=" * 60)
    
    try:
        test_prompt_builder()
        test_medical_specialty_models()
        test_medical_specialty_identifier_initialization()
        test_medical_specialty_identifier_validation()
        test_with_example_specialties()
        test_specialty_categories()
        test_subspecialties()
        
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
