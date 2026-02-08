#!/usr/bin/env python3
"""
Test script for Disease Identifier Module.

This script tests the disease identifier functionality without using mock libraries.
"""

import sys
import os
from pathlib import Path


from app.MedKit.recognizers.disease.disease_identifier_models import DiseaseIdentifierModel, ModelOutput
from app.MedKit.recognizers.disease.disease_identifier_prompts import PromptBuilder, DiseaseIdentifierInput
from app.MedKit.recognizers.disease.disease_recognizer import DiseaseIdentifier
from lite.config import ModelConfig


def test_prompt_builder():
    """Test the PromptBuilder class."""
    print("Testing PromptBuilder...")
    
    # Test system prompt
    system_prompt = PromptBuilder.create_system_prompt()
    assert isinstance(system_prompt, str)
    assert len(system_prompt) > 0
    print(" System prompt created successfully")
    
    # Test user prompt
    disease_input = DiseaseIdentifierInput("diabetes")
    user_prompt = PromptBuilder.create_user_prompt(disease_input)
    assert isinstance(user_prompt, str)
    assert "diabetes" in user_prompt
    print(" User prompt created successfully")
    
    # Test empty disease name
    try:
        empty_input = DiseaseIdentifierInput("")
        assert False, "Should have raised ValueError for empty disease name"
    except ValueError:
        print(" Empty disease name validation works correctly")


def test_disease_models():
    """Test the Pydantic models."""
    print("\nTesting Disease Models...")
    
    # Test DiseaseIdentificationModel
    identification = DiseaseIdentifierModel(
        disease_name="diabetes",
        is_well_known=True,
        common_symptoms=["increased_thirst", "frequent_urination", "fatigue"],
        prevalence="common",
        medical_significance="Major chronic disease affecting millions worldwide"
    )
    print(" DiseaseIdentificationModel created successfully")
    
    # Test DiseaseIdentifierModel
    disease_model = DiseaseIdentifierModel(
        identification=identification,
        summary="Diabetes is a well-known metabolic disorder",
        data_available=True
    )
    print(" DiseaseIdentifierModel created successfully")
    
    # Test ModelOutput
    model_output = ModelOutput(data=disease_model)
    assert model_output.data.disease_name == "diabetes"
    print(" ModelOutput created successfully")


