import os

import pytest
from lite.config import ModelConfig
from medicine_info import MedicineInfoGenerator


@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"),
    reason="Live tests require an API key"
)
@pytest.mark.live
class TestMedicineInfoLive:
    
    @pytest.fixture
    def model_name(self):
        if os.getenv("OPENAI_API_KEY"):
            return "gpt-4o-mini"
        return "gemini/gemini-2.0-flash"

    @pytest.fixture
    def generator(self, model_name):
        config = ModelConfig(model=model_name, temperature=0.1)
        return MedicineInfoGenerator(config)

    def test_live_generate_text_markdown(self, generator):
        result = generator.generate_text("Ibuprofen", structured=False)
        
        assert result is not None
        assert isinstance(result, str)
        assert "Ibuprofen" in result or "ibuprofen" in result
        assert len(result) > 100

    def test_live_generate_text_structured(self, generator):
        result = generator.generate_text("Metformin", structured=True)
        
        assert result is not None
        # Check if it has some fields expected in MedicineInfoModel
        assert hasattr(result, "medicine_name") or hasattr(result, "clinical_pharmacology")

    def test_live_save_functionality(self, generator, tmp_path):
        result = generator.generate_text("Lisinopril", structured=False)
        output_path = tmp_path / "lisinopril.md"
        saved_path = generator.save(result, output_path)
        
        assert saved_path.exists()
        assert saved_path.stat().st_size > 0
