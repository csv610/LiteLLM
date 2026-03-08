import os
import pytest
from pathlib import Path
from symptom_drugs import SymptomDrugs
from symptom_drugs_prompts import SymptomInput
from lite.config import ModelConfig

@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"),
    reason="Live tests require an API key"
)
@pytest.mark.live
class TestSymptomDrugsLive:
    
    @pytest.fixture
    def model_name(self):
        if os.getenv("OPENAI_API_KEY"):
            return "gpt-4o-mini"
        return "gemini/gemini-2.0-flash"

    @pytest.fixture
    def analyzer(self, model_name):
        config = ModelConfig(model=model_name, temperature=0.1)
        return SymptomDrugs(config)

    def test_live_generate_text_markdown(self, analyzer):
        config = SymptomInput(symptom_name="Insomnia")
        result = analyzer.generate_text(config, structured=False)
        
        assert result is not None
        assert isinstance(result, str)
        assert "Insomnia" in result or "insomnia" in result
        assert len(result) > 100

    def test_live_generate_text_structured(self, analyzer):
        config = SymptomInput(symptom_name="Fever")
        result = analyzer.generate_text(config, structured=True)
        
        assert result is not None
        # Check if it has some fields expected in SymptomDrugAnalysisModel
        assert hasattr(result, "symptom_name") or hasattr(result, "suggested_medications")

    def test_live_save_functionality(self, analyzer, tmp_path):
        config = SymptomInput(symptom_name="Cough")
        result = analyzer.generate_text(config, structured=False)
        output_path = analyzer.save(result, tmp_path)
        
        assert output_path.exists()
        assert "cough_drug_recommendations" in output_path.name.lower()
        assert output_path.stat().st_size > 0
