import pytest
from pathlib import Path
from PIL import Image
from lite.vision.validation import is_valid_dimensions
from lite.config import ChatConfig, ModelConfig

def test_is_valid_dimensions_exception(tmp_path):
    # Create a corrupted image file
    corrupt = tmp_path / "corrupt.jpg"
    corrupt.write_text("not an image")
    assert is_valid_dimensions(corrupt) is False

def test_chat_config_custom():
    config = ChatConfig(max_history=10, auto_save=False)
    assert config.max_history == 10
    assert config.auto_save is False

from dataclasses import asdict

def test_model_config_serialization():
    config = ModelConfig(model="gpt-4")
    data = asdict(config)
    assert data["model"] == "gpt-4"
    assert "temperature" in data
