"""
Pytest configuration for Medical Entity Recognizers test suite.
"""

import pytest
from lite.config import ModelConfig


@pytest.fixture
def model_config():
    """Fixture providing a standard ModelConfig for tests."""
    return ModelConfig(model="ollama/gemma3", temperature=0.2)


@pytest.fixture
def test_entities():
    """Fixture providing test entities for various recognizers."""
    return {
        "drug": "Aspirin",
        "disease": "Hypertension",
        "anatomy": "heart",
        "vaccine": "MMR",
        "specialty": "Cardiology",
        "symptom": "chest pain",
        "procedure": "appendectomy",
        "pathogen": "Staphylococcus aureus",
        "clinical_sign": "Babinski sign",
    }
