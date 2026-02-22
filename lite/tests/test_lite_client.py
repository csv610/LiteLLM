import pytest
from unittest.mock import patch, MagicMock
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from pydantic import BaseModel

class SampleResponse(BaseModel):
    answer: str

def test_lite_client_init():
    config = ModelConfig(model="gpt-4")
    client = LiteClient(model_config=config)
    assert client.model_config.model == "gpt-4"

def test_create_message_text_only():
    model_input = ModelInput(user_prompt="hello", system_prompt="be nice")
    messages = LiteClient.create_message(model_input)
    
    assert len(messages) == 2
    assert messages[0] == {"role": "system", "content": "be nice"}
    assert messages[1]["role"] == "user"
    assert messages[1]["content"][0]["text"] == "hello"

@patch("lite.lite_client.ImageUtils.encode_to_base64")
def test_create_message_with_image(mock_encode):
    mock_encode.return_value = "data:image/jpeg;base64,mockdata"
    model_input = ModelInput(user_prompt="describe", image_path="test.jpg")
    messages = LiteClient.create_message(model_input)
    
    assert len(messages) == 1
    content = messages[0]["content"]
    assert content[0]["text"] == "describe"
    assert content[1]["type"] == "image_url"
    assert content[1]["image_url"]["url"] == "data:image/jpeg;base64,mockdata"

@patch("lite.lite_client.completion")
def test_generate_text_simple(mock_completion):
    # Mock litellm response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Paris"
    mock_completion.return_value = mock_response
    
    config = ModelConfig(model="gpt-4")
    client = LiteClient(model_config=config)
    model_input = ModelInput(user_prompt="What is the capital of France?")
    
    result = client.generate_text(model_input)
    assert result == "Paris"
    mock_completion.assert_called_once()

@patch("lite.lite_client.completion")
def test_generate_text_structured(mock_completion):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '{"answer": "London"}'
    mock_completion.return_value = mock_response
    
    config = ModelConfig(model="gpt-4")
    client = LiteClient(model_config=config)
    model_input = ModelInput(user_prompt="Capital of UK?", response_format=SampleResponse)
    
    result = client.generate_text(model_input)
    assert isinstance(result, SampleResponse)
    assert result.answer == "London"
