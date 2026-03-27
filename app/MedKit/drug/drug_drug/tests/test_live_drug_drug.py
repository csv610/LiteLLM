import os

import pytest
from drug_drug_interaction import DrugDrugInteractionGenerator
from drug_drug_interaction_prompts import DrugDrugInput
from lite.config import ModelConfig

# Set model from environment or use a common default
MODEL = os.getenv("LITE_MODEL", "openai/gpt-4o-mini")

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY") and not os.getenv("LITE_MODEL"), reason="No API key or model configured for live tests")
class TestLiveDrugDrug:
    @pytest.fixture
    def drug_drug_generator(self):
        model_config = ModelConfig(model=MODEL, temperature=0.2)
        return DrugDrugInteractionGenerator(model_config)

    def test_live_generate_unstructured(self, drug_drug_generator):
        user_input = DrugDrugInput(
            medicine1="Metformin",
            medicine2="Lisinopril",
            age=50
        )
        
        result = drug_drug_generator.generate_text(user_input, structured=False)
        
        assert result.markdown is not None
        assert len(result.markdown) > 0
        assert "Metformin" in result.markdown or "Lisinopril" in result.markdown

    def test_live_generate_structured(self, drug_drug_generator):
        user_input = DrugDrugInput(
            medicine1="Ibuprofen",
            medicine2="Aspirin",
            age=40
        )
        
        result = drug_drug_generator.generate_text(user_input, structured=True)
        
        assert result.data is not None
        assert result.data.data_availability.data_available is True
        assert result.data.interaction_details is not None
        assert "Ibuprofen" in result.data.interaction_details.drug1_name or "Ibuprofen" in result.data.interaction_details.drug2_name
