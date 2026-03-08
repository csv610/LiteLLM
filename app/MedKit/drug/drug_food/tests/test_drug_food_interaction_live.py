import pytest
import os
from pathlib import Path
from drug_food_interaction import DrugFoodInteraction
from drug_food_interaction_prompts import DrugFoodInput
from lite.config import ModelConfig
from drug_food_interaction_models import ModelOutput

# Skip live tests if no OpenAI API key is found
@pytest.mark.live
@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not found")
def test_generate_text_live_unstructured():
    # Use gpt-4o-mini as it's efficient and often has higher quotas
    model_config = ModelConfig(model="openai/gpt-4o-mini", temperature=0.1)
    analyzer = DrugFoodInteraction(model_config)
    
    user_input = DrugFoodInput(
        medicine_name="Aspirin",
        diet_type="Normal",
        age=30
    )
    
    result = analyzer.generate_text(user_input, structured=False)
    
    assert isinstance(result, ModelOutput)
    assert result.markdown is not None
    assert "aspirin" in result.markdown.lower()

@pytest.mark.live
@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not found")
def test_generate_text_live_structured():
    # Use gpt-4o-mini
    model_config = ModelConfig(model="openai/gpt-4o-mini", temperature=0.1)
    analyzer = DrugFoodInteraction(model_config)
    
    user_input = DrugFoodInput(
        medicine_name="Metformin",
        diet_type="Normal",
        age=50
    )
    
    result = analyzer.generate_text(user_input, structured=True)
    
    assert isinstance(result, ModelOutput)
    assert result.data is not None
    assert result.data.interaction_details.medicine_name.lower() == "metformin"
    assert result.data.data_availability.data_available is True
