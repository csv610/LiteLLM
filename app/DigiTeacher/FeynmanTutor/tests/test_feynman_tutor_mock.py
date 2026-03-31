import pytest
from unittest.mock import patch
from DigiTeacher.FeynmanTutor.feynman_tutor import FeynmanTutorQuestionGenerator, ModelConfig

@pytest.fixture
def mock_client():
    with patch('DigiTeacher.FeynmanTutor.feynman_tutor.LiteClient') as mock:
        instance = mock.return_value
        yield instance

def test_tutor_initialization():
    with patch('DigiTeacher.FeynmanTutor.feynman_tutor.LiteClient'):
        config = ModelConfig("quantum physics", "beginner")
        tutor = FeynmanTutorQuestionGenerator(config)
        assert tutor.config.topic == "quantum physics"
        assert tutor.config.level == "beginner"
        assert tutor.is_convinced is False
        assert len(tutor.messages) == 4

def test_start_tutoring(mock_client):
    mock_client.completion.return_value = {
        "choices": [{"message": {"content": "Initial question."}}]
    }
    config = ModelConfig("topic", "level")
    tutor = FeynmanTutorQuestionGenerator(config)
    question = tutor.start_tutoring()
    
    assert question == "Initial question."
    assert len(tutor.history) == 1
    assert tutor.history[0]["question"] == "Initial question."
    assert tutor.history[0]["response"] is None

def test_process_student_response(mock_client):
    # Setup: initial question already given
    config = ModelConfig("topic", "level")
    tutor = FeynmanTutorQuestionGenerator(config)
    tutor.history = [{"question": "Initial question", "response": None}]
    
    # Mock for process_student_response (asking for next step)
    # And mock for _update_summary (called inside process_student_response)
    mock_client.completion.side_effect = [
        {"choices": [{"message": {"content": "Next question."}}]}, # Response for process_student_response
        {"choices": [{"message": {"content": "Summary of progress."}}]} # Response for _update_summary
    ]
    
    next_question = tutor.process_student_response("I think I get it.")
    
    assert next_question == "Next question."
    assert tutor.history[0]["response"] == "I think I get it."
    assert len(tutor.history) == 2
    assert tutor.history[1]["question"] == "Next question."
    assert tutor.summary == "Summary of progress."

def test_convinced_logic(mock_client):
    mock_client.completion.side_effect = [
        {"choices": [{"message": {"content": "Well done! [CONVINCED]"}}]}, # Response for process_student_response
        {"choices": [{"message": {"content": "Summary."}}]} # Response for _update_summary
    ]
    
    config = ModelConfig("topic", "level")
    tutor = FeynmanTutorQuestionGenerator(config)
    tutor.history = [{"question": "Explain X", "response": None}]
    
    tutor.process_student_response("User feedback")
    
    assert tutor.is_convinced is True
    # The [CONVINCED] tag should be stripped
    assert tutor.messages[-1]["content"] == "Well done!"
    
    # Test guard logic: calling process_student_response again should return the completed message
    second_response = tutor.process_student_response("More feedback")
    assert "already complete" in second_response
    # Completion should NOT be called again
    assert mock_client.completion.call_count == 2 # 1 for process_student_response + 1 for _update_summary

def test_error_handling(mock_client):
    mock_client.completion.side_effect = Exception("API error")
    
    config = ModelConfig("topic", "level")
    tutor = FeynmanTutorQuestionGenerator(config)
    response = tutor.start_tutoring()
    
    assert "🚨 Error communicating with the tutor" in response
