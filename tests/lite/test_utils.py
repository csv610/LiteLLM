import pytest
import logging
import os
from pathlib import Path
from pydantic import BaseModel
from lite.utils.print_response import print_response, print_simple_result
from lite.utils.save_response import save_model_response
from lite.logging_config import configure_logging

class MockModel(BaseModel):
    name: str
    age: int
    tags: list[str] = []

def test_print_response_none(capsys):
    print_response(None)
    captured = capsys.readouterr()
    assert "No result to display" in captured.out

def test_print_response_model(capsys):
    model = MockModel(name="test", age=25, tags=["a", "b"])
    print_response(model, title="Test Model")
    captured = capsys.readouterr()
    assert "=== TEST MODEL ===" in captured.out
    assert "NAME:" in captured.out
    assert "test" in captured.out
    assert "AGE:" in captured.out
    assert "25" in captured.out
    assert "TAGS:" in captured.out
    assert "1. a" in captured.out
    assert "2. b" in captured.out

def test_print_response_dict(capsys):
    data = {"info": {"key": "val"}, "list": []}
    print_response(data)
    captured = capsys.readouterr()
    assert "INFO:" in captured.out
    assert "Key: val" in captured.out
    assert "(empty)" in captured.out

def test_print_simple_result(capsys):
    print_simple_result("just a string")
    captured = capsys.readouterr()
    assert "just a string" in captured.out
    
    print_simple_result({"k": "v"}, title="Simple Dict")
    captured = capsys.readouterr()
    assert "=== SIMPLE DICT ===" in captured.out
    assert "k: v" in captured.out

def test_save_model_response_pydantic(tmp_path):
    model = MockModel(name="save_test", age=30)
    output = tmp_path / "test_model"
    saved_path = save_model_response(model, output)
    assert saved_path.suffix == ".json"
    assert saved_path.exists()
    import json
    with open(saved_path) as f:
        data = json.load(f)
    assert data["name"] == "save_test"

def test_save_model_response_str(tmp_path):
    content = "# Markdown Content"
    output = tmp_path / "test_doc"
    saved_path = save_model_response(content, output)
    assert saved_path.suffix == ".md"
    assert saved_path.read_text() == content

def test_save_model_response_invalid():
    with pytest.raises(ValueError, match="Unsupported model type"):
        save_model_response(123, "wont_save")

def test_configure_logging(tmp_path):
    log_file = tmp_path / "test.log"
    # Test with verbosity
    configure_logging(log_file=str(log_file), verbosity=4)
    logger = logging.getLogger("test_logger")
    assert logger.root.level == logging.DEBUG
    
    # Test console enable
    configure_logging(log_file=str(log_file), enable_console=True)
    assert any(isinstance(h, logging.StreamHandler) for h in logging.getLogger().handlers)

    # Test path normalization logic (not absolute)
    configure_logging(log_file="test_norm.log")
    # Clean up the created logs dir if possible, or just verify it doesn't crash
