import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from lite.lite_chat import LiteChat
from lite.config import ModelConfig, ChatConfig, ModelInput

@pytest.fixture
def model_config():
    return ModelConfig(model="gpt-4", temperature=0.7)

@pytest.fixture
def chat_config(tmp_path):
    return ChatConfig(max_history=4, auto_save=True, save_dir=str(tmp_path))

@pytest.fixture
def lite_chat(model_config, chat_config):
    return LiteChat(model_config=model_config, chat_config=chat_config)

def test_lite_chat_initialization(lite_chat, model_config):
    assert lite_chat.model_config == model_config
    assert lite_chat.max_history == 4
    assert lite_chat.auto_save is True
    assert lite_chat.conversation_history == []

def test_lite_chat_initialization_odd_history():
    chat_config = ChatConfig(max_history=5)
    chat = LiteChat(chat_config=chat_config)
    assert chat.max_history == 4

def test_add_message_to_history(lite_chat):
    lite_chat.add_message_to_history("user", "hello")
    assert len(lite_chat.conversation_history) == 1
    assert lite_chat.conversation_history[0] == {"role": "user", "content": "hello"}

def test_history_trimming(lite_chat):
    # max_history is 4
    lite_chat.add_message_to_history("user", "1")
    lite_chat.add_message_to_history("assistant", "2")
    lite_chat.add_message_to_history("user", "3")
    lite_chat.add_message_to_history("assistant", "4")
    assert len(lite_chat.conversation_history) == 4
    
    lite_chat.add_message_to_history("user", "5")
    # Should pop 1 and 2
    assert len(lite_chat.conversation_history) == 3
    assert lite_chat.conversation_history[0]["content"] == "3"

def test_history_trimming_single_edge_case():
    chat_config = ChatConfig(max_history=0)
    chat = LiteChat(chat_config=chat_config)
    chat.add_message_to_history("user", "1")
    assert len(chat.conversation_history) == 0

def test_create_message_basic(lite_chat):
    model_input = ModelInput(user_prompt="test prompt")
    messages = lite_chat.create_message(model_input)
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "test prompt"

def test_create_message_empty_prompt(lite_chat):
    with pytest.raises(ValueError, match="user_prompt cannot be empty"):
        model_input = ModelInput(user_prompt="")
        lite_chat.create_message(model_input)

@patch("lite.lite_chat.ImageUtils.encode_to_base64")
def test_create_message_with_image(mock_encode, lite_chat):
    mock_encode.return_value = "base64data"
    model_input = ModelInput(user_prompt="what is this?", image_path="test.jpg")
    messages = lite_chat.create_message(model_input)
    assert len(messages) == 1
    content = messages[0]["content"]
    assert isinstance(content, list)
    assert content[0]["text"] == "what is this?"
    assert content[1]["image_url"]["url"] == "base64data"

@patch("lite.lite_chat.completion")
def test_generate_text_success(mock_completion, lite_chat):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "assistant response"
    mock_completion.return_value = mock_response
    
    model_input = ModelInput(user_prompt="hello")
    response = lite_chat.generate_text(model_input)
    
    assert response == "assistant response"
    assert len(lite_chat.conversation_history) == 2
    assert lite_chat.conversation_history[1]["role"] == "assistant"
    assert os.path.exists(lite_chat.conversation_file)

def test_generate_text_no_config():
    chat = LiteChat()
    model_input = ModelInput(user_prompt="hi")
    with pytest.raises(ValueError, match="ModelConfig must be provided"):
        chat.generate_text(model_input)

@patch("lite.lite_chat.completion")
def test_generate_text_error(mock_completion, lite_chat):
    mock_completion.side_effect = Exception("API Error")
    model_input = ModelInput(user_prompt="hello")
    response = lite_chat.generate_text(model_input)
    assert "Error: API Error" in response

@patch("lite.lite_chat.completion")
def test_generate_text_vision_error(mock_completion, lite_chat):
    mock_completion.side_effect = Exception("Vision API failed")
    # Trigger image-path logic
    lite_chat.current_image_path = "test.jpg"
    model_input = ModelInput(user_prompt="what is this?")
    
    with patch("lite.lite_chat.ImageUtils.encode_to_base64", return_value="b64"):
        response = lite_chat.generate_text(model_input)
        assert "Error: Vision API failed" in response

def test_reset_conversation(lite_chat):
    lite_chat.add_message_to_history("user", "hi")
    lite_chat.reset_conversation()
    assert lite_chat.conversation_history == []
    assert lite_chat.current_image_path is None

def test_format_content_list():
    content = [{"type": "text", "text": "hello"}, {"type": "image_url"}]
    formatted = LiteChat._format_content(content)
    assert formatted == "hello"

def test_format_content_list_no_text():
    content = [{"type": "other"}]
    formatted = LiteChat._format_content(content)
    assert "other" in formatted

def test_format_content_complex_list():
    content = [
        {"type": "text", "text": "desc"},
        {"type": "image_url", "image_url": {"url": "..."}}
    ]
    formatted = LiteChat._format_content(content)
    assert formatted == "desc"

def test_format_content_string():
    assert LiteChat._format_content("hello") == "hello"

def test_add_message_to_history_content(lite_chat):
    # Test that it adds content correctly
    content = [{"type": "text", "text": "hi"}]
    lite_chat.add_message_to_history("user", content)
    assert lite_chat.conversation_history[-1]["content"] == content

def test_save_conversation(lite_chat, tmp_path):
    lite_chat.add_message_to_history("user", "hello")
    lite_chat.add_message_to_history("assistant", "hi there")
    lite_chat.save_conversation()
    
    assert lite_chat.conversation_file is not None
    assert os.path.exists(lite_chat.conversation_file)
    content = Path(lite_chat.conversation_file).read_text()
    assert "User:** hello" in content
    assert "Assistant:** hi there" in content

def test_save_conversation_with_list_content(lite_chat, tmp_path):
    # Simulate vision content
    content = [{"type": "text", "text": "look at this"}, {"type": "image_url"}]
    lite_chat.add_message_to_history("user", content)
    lite_chat.add_message_to_history("assistant", "nice")
    lite_chat.save_conversation()
    
    content_text = Path(lite_chat.conversation_file).read_text()
    assert "look at this" in content_text

def test_get_conversation_history(lite_chat):
    lite_chat.add_message_to_history("user", "hi")
    history = lite_chat.get_conversation_history()
    assert len(history) == 1
    # Check it's a copy
    history.append({"role": "assistant", "content": "bye"})
    assert len(lite_chat.conversation_history) == 1
