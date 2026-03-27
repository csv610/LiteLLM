import os

import pytest
from drugbank_medicine import DrugBankMedicine
from lite.config import ModelConfig


@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"),
    reason="Live tests require an API key"
)
@pytest.mark.live
class TestDrugBankMedicineLive:
    
    @pytest.fixture
    def model_name(self):
        if os.getenv("OPENAI_API_KEY"):
            return "gpt-4o-mini"
        return "gemini/gemini-2.0-flash"

    @pytest.fixture
    def fetcher(self, model_name):
        config = ModelConfig(model=model_name, temperature=0.1)
        return DrugBankMedicine(config)

    def test_live_generate_text_markdown(self, fetcher):
        result = fetcher.generate_text("Ibuprofen", structured=False)
        
        assert result is not None
        assert isinstance(result, str)
        assert "Ibuprofen" in result or "ibuprofen" in result
        assert len(result) > 100

    def test_live_generate_text_structured(self, fetcher):
        # Structured result for medicine info
        result = fetcher.generate_text("Metformin", structured=True)
        
        assert result is not None
        # Check if it has some fields expected in MedicineInfo
        # MedicineInfo is very large, so we just check it was returned as object
        assert hasattr(result, "pharmacology") or hasattr(result, "medicine_name")

    def test_live_save_functionality(self, fetcher, tmp_path):
        result = fetcher.generate_text("Lisinopril", structured=False)
        output_path = fetcher.save(result, tmp_path)
        
        assert output_path.exists()
        assert "lisinopril_medicine_info" in output_path.name.lower()
        assert output_path.stat().st_size > 0
