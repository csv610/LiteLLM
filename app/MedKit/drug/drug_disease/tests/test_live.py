import os

import pytest
from app.MedKit.drug.drug_disease.nonagentic.drug_disease_interaction import DrugDiseaseInteraction
from app.MedKit.drug.drug_disease.nonagentic.drug_disease_interaction_prompts import DrugDiseaseInput
from lite.config import ModelConfig

# Skip live tests by default unless LIVE_TEST environment variable is set
LIVE_TEST = os.environ.get("LIVE_TEST", "false").lower() == "true"

@pytest.mark.skipif(not LIVE_TEST, reason="LIVE_TEST environment variable not set")
def test_live_interaction_unstructured():
    """Live test using the default model (ollama/gemma3)."""
    model_config = ModelConfig(model="ollama/gemma3", temperature=0.0)
    analyzer = DrugDiseaseInteraction(model_config)
    
    input_config = DrugDiseaseInput(
        medicine_name="Ibuprofen",
        condition_name="Kidney Disease",
        condition_severity="moderate"
    )
    
    result = analyzer.generate_text(input_config, structured=False)
    
    assert result is not None
    assert result.markdown is not None
    assert len(result.markdown) > 0
    assert "ibuprofen" in result.markdown.lower()
    assert "kidney" in result.markdown.lower()

@pytest.mark.skipif(not LIVE_TEST, reason="LIVE_TEST environment variable not set")
def test_live_interaction_structured():
    """Live test using the default model (ollama/gemma3) with structured output."""
    model_config = ModelConfig(model="ollama/gemma3", temperature=0.0)
    analyzer = DrugDiseaseInteraction(model_config)
    
    input_config = DrugDiseaseInput(
        medicine_name="Metformin",
        condition_name="Renal Impairment",
        condition_severity="severe"
    )
    
    result = analyzer.generate_text(input_config, structured=True)
    
    assert result is not None
    assert result.data is not None
    assert result.data.data_availability.data_available is True
    assert result.data.interaction_details.medicine_name.lower() == "metformin"
    assert "renal" in result.data.interaction_details.condition_name.lower()
