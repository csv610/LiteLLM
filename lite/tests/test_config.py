from lite.config import ModelConfig, ModelInput
import pytest

def test_model_config_default():
    config = ModelConfig(model="gpt-4")
    assert config.model == "gpt-4"
    assert config.temperature == 0.7

def test_model_input_validation():
    # Should fail if both prompt and images are missing
    with pytest.raises(ValueError, match="user_prompt cannot be empty"):
        ModelInput(user_prompt="")

def test_model_input_valid():
    inp = ModelInput(user_prompt="hello")
    assert inp.user_prompt == "hello"
    assert inp.system_prompt is None
