from unittest.mock import patch, MagicMock
from lite.lite_mcq_client import LiteMCQClient
from lite.config import MCQInput
from pydantic import BaseModel

# Mock output model
class MCQAnswer(BaseModel):
    answer: str
    reasoning: str

def test_mcq_input_validation():
    # Dict options
    inp = MCQInput(
        question="What is the capital of UK?",
        options={"A": "London", "B": "Paris"}
    )
    assert inp.question == "What is the capital of UK?"
    assert inp.options["A"] == "London"

@patch("lite.lite_client.completion")
def test_mcq_solve(mock_completion):
    mock_response = MagicMock()
    # Mock full MultipleChoiceSolverResponse structure
    content = {
        "answer": {
            "question": "What is the capital of Japan?",
            "correct_options": [{"key": "B", "value": "Tokyo"}],
            "reasoning": "Tokyo is the capital of Japan."
        }
    }
    import json
    mock_response.choices[0].message.content = json.dumps(content)
    mock_completion.return_value = mock_response
    
    client = LiteMCQClient(model="gpt-4")
    inp = MCQInput(
        question="What is the capital of Japan?",
        options=["Seoul", "Tokyo"]
    )
    
    # Solve uses generate_text internally which returns string or pydantic model 
    result = client.solve(inp)
    assert "Tokyo" in str(result)
