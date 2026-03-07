import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from unittest.mock import patch, MagicMock
from medical.surgical_tray.surgical_tray_info import SurgicalTrayGenerator
from lite.config import ModelConfig
from medical.surgical_tray.surgical_tray_info_models import (
    SurgicalTrayModel, ModelOutput, TrayInstrument
)

@pytest.fixture
def mock_lite_client():
    with patch('medical.surgical_tray.surgical_tray_info.LiteClient') as mock:
        yield mock

def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = SurgicalTrayGenerator(config)
    assert generator.model_config == config

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalTrayGenerator(config)
    mock_output = ModelOutput(markdown="Tray info", tray_data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text("Appendectomy")
    assert result.markdown == "Tray info"
    assert generator.target == "Appendectomy"

def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = SurgicalTrayGenerator(config)
    with pytest.raises(ValueError, match="Surgery name cannot be empty"):
        generator.generate_text("")

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalTrayGenerator(config)
    
    mock_data = SurgicalTrayModel(
        surgery_name="Appendectomy",
        specialty="General Surgery",
        instruments=[
            TrayInstrument(name="Scalpel", quantity=1, category="Cutting", reason="Incision")
        ],
        sterilization_method="Autoclave",
        setup_instructions="Open tray on sterile field"
    )
    
    mock_output = ModelOutput(tray_data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text("Appendectomy", structured=True)
    assert result.tray_data.surgery_name == "Appendectomy"

@patch('medical.surgical_tray.surgical_tray_info.save_model_response')
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalTrayGenerator(config)
    mock_output = ModelOutput(markdown="Info")
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    generator.generate_text("Appendectomy")
    generator.save(mock_output, Path("/tmp"))
    
    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("appendectomy")
