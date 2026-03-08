import os
import pytest
from pathlib import Path
from similar_drugs import SimilarDrugs
from similar_drugs_models import SimilarDrugsConfig
from lite.config import ModelConfig

@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"),
    reason="Live tests require an API key"
)
@pytest.mark.live
class TestSimilarDrugsLive:
    
    @pytest.fixture
    def model_name(self):
        if os.getenv("OPENAI_API_KEY"):
            return "gpt-4o-mini"
        return "gemini/gemini-2.0-flash"

    @pytest.fixture
    def finder(self, model_name):
        model_config = ModelConfig(model=model_name, temperature=0.1)
        similar_drugs_config = SimilarDrugsConfig(verbosity=0)
        return SimilarDrugs(similar_drugs_config, model_config)

    def test_live_find_markdown(self, finder):
        result = finder.find("Aspirin", structured=False)
        
        assert result is not None
        assert isinstance(result, str)
        assert "Aspirin" in result or "aspirin" in result
        assert len(result) > 100

    def test_live_find_structured(self, finder):
        result = finder.find("Ibuprofen", structured=True)
        
        assert result is not None
        # Check if it has some fields expected in SimilarMedicinesResult
        assert hasattr(result, "medicine_name") or hasattr(result, "similar_medicines")
