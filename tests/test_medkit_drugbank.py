import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from app.MedKit.drug.medicine.drugbank.drugbank_medicine import DrugBankMedicine
from app.MedKit.drug.medicine.drugbank.drugbank_medicine_models import MedicineInfo
from lite.config import ModelConfig

@pytest.fixture
def db_medicine():
    return DrugBankMedicine(ModelConfig(model="gpt-4"))

def test_drugbank_medicine_generate_basic(db_medicine):
    with patch("app.MedKit.drug.medicine.drugbank.drugbank_medicine.LiteClient.generate_text") as mock_gen:
        mock_gen.return_value = "Aspirin is a common medicine."
        result = db_medicine.generate_text("Aspirin")
        assert result == "Aspirin is a common medicine."
        assert db_medicine.medicine_name == "Aspirin"

def test_drugbank_medicine_generate_structured(db_medicine):
    with patch("app.MedKit.drug.medicine.drugbank.drugbank_medicine.LiteClient.generate_text") as mock_gen:
        mock_info = MagicMock(spec=MedicineInfo)
        mock_gen.return_value = mock_info
        result = db_medicine.generate_text("Aspirin", structured=True)
        assert result == mock_info

def test_drugbank_medicine_generate_empty(db_medicine):
    with pytest.raises(ValueError, match="Medicine name cannot be empty"):
        db_medicine.generate_text("")

def test_drugbank_medicine_save(db_medicine, tmp_path):
    db_medicine.medicine_name = "Test Drug"
    result = "Some info"
    path = db_medicine.save(result, tmp_path)
    assert "Test_Drug_medicine_info" in path.name
    assert path.exists()

def test_drugbank_medicine_save_no_name(db_medicine, tmp_path):
    with pytest.raises(ValueError, match="No medicine name information available"):
        db_medicine.save("info", tmp_path)

def test_drugbank_medicine_sanitize(db_medicine):
    assert db_medicine._sanitize_filename("Aspirin / 500mg") == "Aspirin_500mg"
    assert db_medicine._sanitize_filename("") == "medicine"
