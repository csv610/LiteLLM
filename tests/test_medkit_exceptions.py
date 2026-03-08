import pytest
from app.MedKit.utils.medkit_exceptions import (
    MedKitError, ValidationError, LLMError, FileIOError, ConfigurationError, MedKitImportError
)

def test_medkit_error_base():
    err = MedKitError("basic error", context="some context", original_exception=ValueError("original"))
    msg = str(err)
    assert "[MedKitError] basic error" in msg
    assert "Context: some context" in msg
    assert "Caused by: ValueError: original" in msg
    assert repr(err) == "MedKitError('basic error')"

def test_validation_error():
    err = ValidationError("invalid input")
    assert "[ValidationError] invalid input" in str(err)

def test_llm_error():
    err = LLMError("generation failed")
    assert "[LLMError] generation failed" in str(err)

def test_file_io_error():
    err = FileIOError("save failed")
    assert "[FileIOError] save failed" in str(err)

def test_configuration_error():
    err = ConfigurationError("missing config")
    assert "[ConfigurationError] missing config" in str(err)

def test_import_error():
    err = MedKitImportError("module not found")
    assert "[ImportError] module not found" in str(err)
