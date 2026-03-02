import pytest
from unittest.mock import patch, MagicMock
from feynman_tutor import FeynmanTutor

@pytest.fixture
def mock_completion():
    with patch('feynman_tutor.completion') as mock:
        yield mock

def test_tutor_initialization():
    tutor = FeynmanTutor("quantum physics", "beginner")
    assert tutor.topic == "quantum physics"
    assert tutor.level == "beginner"
    assert tutor.is_convinced is False
    assert len(tutor.messages) == 4

def test_get_initial_explanation(mock_completion):
    mock_completion.return_value = {
        "choices": [{"message": {"content": "Initial explanation."}}]
    }
    tutor = FeynmanTutor("topic", "level")
    explanation = tutor.get_initial_explanation()
    
    assert explanation == "Initial explanation."
    assert len(tutor.history) == 1
    assert tutor.history[0]["question"] == "Initial explanation."
    assert tutor.history[0]["response"] is None

def test_refine_explanation(mock_completion):
    # Setup: initial explanation already given
    tutor = FeynmanTutor("topic", "level")
    tutor.history = [{"question": "Initial question", "response": None}]
    
    # Mock for refine_explanation (asking for next step)
    # And mock for _update_summary (called inside refine_explanation)
    mock_completion.side_effect = [
        {"choices": [{"message": {"content": "Next question."}}]}, # Response for refine_explanation
        {"choices": [{"message": {"content": "Summary of progress."}}]} # Response for _update_summary
    ]
    
    next_question = tutor.refine_explanation("I think I get it.")
    
    assert next_question == "Next question."
    assert tutor.history[0]["response"] == "I think I get it."
    assert len(tutor.history) == 2
    assert tutor.history[1]["question"] == "Next question."
    assert tutor.summary == "Summary of progress."

def test_convinced_logic(mock_completion):
    mock_completion.side_effect = [
        {"choices": [{"message": {"content": "Well done! [CONVINCED]"}}]}, # Response for refine_explanation
        {"choices": [{"message": {"content": "Summary."}}]} # Response for _update_summary
    ]
    
    tutor = FeynmanTutor("topic", "level")
    tutor.history = [{"question": "Explain X", "response": None}]
    
    tutor.refine_explanation("User feedback")
    
    assert tutor.is_convinced is True
    # The [CONVINCED] tag should be stripped
    assert tutor.messages[-1]["content"] == "Well done!"

def test_error_handling(mock_completion):
    mock_completion.side_effect = Exception("API error")
    
    tutor = FeynmanTutor("topic", "level")
    response = tutor.get_initial_explanation()
    
    assert "🚨 Error communicating with the tutor" in response
