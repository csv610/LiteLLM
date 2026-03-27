import os

import pytest
from drugs_comparison import DrugsComparison, DrugsComparisonInput
from lite.config import ModelConfig


@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"),
    reason="Live tests require an API key"
)
@pytest.mark.live
class TestDrugsComparisonLive:
    
    @pytest.fixture
    def model_name(self):
        if os.getenv("OPENAI_API_KEY"):
            return "gpt-4o-mini"
        return "gemini/gemini-2.0-flash"

    @pytest.fixture
    def analyzer(self, model_name):
        config = ModelConfig(model=model_name, temperature=0.1)
        return DrugsComparison(config)

    def test_live_generate_text_markdown(self, analyzer):
        config = DrugsComparisonInput(medicine1="Aspirin", medicine2="Ibuprofen")
        result = analyzer.generate_text(config, structured=False)
        
        assert result is not None
        assert isinstance(result, str)
        assert "Aspirin" in result or "aspirin" in result
        assert "Ibuprofen" in result or "ibuprofen" in result
        assert len(result) > 100

    def test_live_generate_text_structured(self, analyzer):
        config = DrugsComparisonInput(medicine1="Acetaminophen", medicine2="Naproxen")
        result = analyzer.generate_text(config, structured=True)
        
        assert result is not None
        assert hasattr(result, "medicine1_clinical")
        assert "Acetaminophen" in result.medicine1_clinical.medicine_name
        assert "Naproxen" in result.medicine2_clinical.medicine_name

    def test_live_save_functionality(self, analyzer, tmp_path):
        config = DrugsComparisonInput(medicine1="Amlodipine", medicine2="Lisinopril")
        result = analyzer.generate_text(config, structured=False)
        
        output_path = analyzer.save(result, tmp_path)
        
        assert output_path.exists()
        assert "amlodipine_vs_lisinopril" in output_path.name.lower()
        assert output_path.stat().st_size > 0
