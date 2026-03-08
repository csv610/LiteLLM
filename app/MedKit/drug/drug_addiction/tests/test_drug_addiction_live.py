import os
import pytest
from pathlib import Path
from drug_addiction import DrugAddiction
from drug_addiction_prompts import DrugAddictionInput
from lite.config import ModelConfig

# Skip live tests if no API key is present
# Using GEMINI_API_KEY as a proxy for live environment availability
@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"),
    reason="Live tests require an API key (GEMINI_API_KEY or OPENAI_API_KEY)"
)
@pytest.mark.live
class TestDrugAddictionLive:
    
    @pytest.fixture
    def model_name(self):
        # Prefer OpenAI for reliability in this environment if Gemini has quota issues
        if os.getenv("OPENAI_API_KEY"):
            return "gpt-4o-mini"
        if os.getenv("GEMINI_API_KEY"):
            return "gemini/gemini-2.0-flash"
        return "gpt-4o-mini"

    @pytest.fixture
    def analyzer(self, model_name):
        config = ModelConfig(model=model_name, temperature=0.1)
        return DrugAddiction(config)

    def test_live_generate_text_markdown(self, analyzer):
        config = DrugAddictionInput(medicine_name="Caffeine")
        result = analyzer.generate_text(config, structured=False)
        
        assert result is not None
        assert result.markdown is not None
        assert "Caffeine" in result.markdown or "caffeine" in result.markdown
        assert len(result.markdown) > 100

    def test_live_generate_text_structured(self, analyzer):
        # Use a very common substance for high likelihood of correct structured response
        config = DrugAddictionInput(medicine_name="Nicotine")
        result = analyzer.generate_text(config, structured=True)
        
        assert result is not None
        assert result.data is not None
        assert result.data.addiction_details is not None
        assert "Nicotine" in result.data.addiction_details.medicine_name
        assert result.data.addiction_details.addiction_potential is not None
        assert len(result.data.addiction_details.withdrawal_symptoms) > 0

    def test_live_save_functionality(self, analyzer, tmp_path):
        config = DrugAddictionInput(medicine_name="Alcohol")
        result = analyzer.generate_text(config, structured=False)
        
        output_path = analyzer.save(result, tmp_path)
        
        assert output_path.exists()
        assert "alcohol" in output_path.name.lower()
        # Verify it saved something substantial
        assert output_path.stat().st_size > 0
