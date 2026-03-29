import json
import pytest
from unittest.mock import MagicMock, patch
from object_guesser_game import ObjectGuesserGame

def mock_generate_text(model_input):
    system_prompt = model_input.system_prompt
    user_prompt = model_input.user_prompt
    
    if "State Management" in system_prompt:
        if "Is it a fruit?" in user_prompt and "USER: yes" in user_prompt:
            return json.dumps({
                "properties": {"is_fruit": "yes"},
                "category": "fruit",
                "excluded_objects": []
            })
        else:
            return json.dumps({
                "properties": {},
                "category": None,
                "excluded_objects": []
            })
    
    elif "Strategy Agent" in system_prompt:
        if '"is_fruit": "yes"' in user_prompt:
            return json.dumps({
                "action": "MAKE_GUESS",
                "content": "apple"
            })
        else:
            return json.dumps({
                "action": "ASK_QUESTION",
                "content": "Is it a fruit?"
            })
            
    elif "Extraction Agent" in system_prompt:
        if "USER: yes" in user_prompt:
            return json.dumps({
                "user_sentiment": "yes",
                "is_guess": True,
                "guessed_object": "apple"
            })
        else:
            return json.dumps({
                "user_sentiment": "no",
                "is_guess": False,
                "guessed_object": None
            })
            
    return json.dumps({"error": "Unknown prompt type"})

def test_game_success_apple():
    """Test a successful game run for 'apple'."""
    game = ObjectGuesserGame(model="mock-model")
    game.client.generate_text = MagicMock(side_effect=mock_generate_text)
    
    # Mock input to answer "yes" to "Is it a fruit?" and then "yes" to "Is it a apple?"
    with patch('builtins.input', side_effect=["yes", "yes"]):
        success = game.play()
    
    assert success is True
    assert game.question_count == 1 # 1 question + 1 guess (guess turn count doesn't increment if successful?)
    # Wait, looking at the code:
    # Question count increments for ASK_QUESTION.
    # For MAKE_GUESS:
    # if extraction["user_sentiment"] == "yes": return True
    # else: self.question_count += 1
    # So if it guesses correctly, question_count remains at 1. Correct.

def test_game_failure_max_questions():
    """Test a game run that exceeds max questions."""
    game = ObjectGuesserGame(model="mock-model", max_questions=2)
    game.client.generate_text = MagicMock(side_effect=mock_generate_text)
    
    # Strategy agent will always return ASK_QUESTION "Is it a fruit?"
    # and User will always answer "no".
    with patch('builtins.input', side_effect=["no", "no", "no"]):
        success = game.play()
        
    assert success is False
    assert game.question_count == 2
