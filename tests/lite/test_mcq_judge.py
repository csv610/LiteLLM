import pytest
from unittest.mock import patch, MagicMock
from lite.lite_mcq_client import LiteMCQClient, MCQInput, MultipleChoiceAnswer, MultipleChoiceSolverResponse, CorrectOption
from lite.lite_response_judge import ResponseJudge, UserInput, EvaluationModel, CriteriaScores, ModelConfig

@pytest.fixture
def mcq_client():
    return LiteMCQClient()

@pytest.fixture
def judge():
    config = ModelConfig(model="gpt-4")
    return ResponseJudge(config)

def test_mcq_client_solve_success(mcq_client):
    with patch("lite.lite_mcq_client.LiteClient.generate_text") as mock_gen:
        answer = MultipleChoiceAnswer(
            question="What is 2+2?",
            correct_options=[CorrectOption(key="B", value="4")],
            reasoning="Basic math",
            confidence=1.0
        )
        mock_gen.return_value = MultipleChoiceSolverResponse(answer=answer)
        
        mcq_input = MCQInput(question="What is 2+2?", options=["3", "4", "5"])
        result = mcq_client.solve(mcq_input)
        
        assert result.question == "What is 2+2?"
        assert result.correct_options[0].value == "4"
        assert mock_gen.called

def test_mcq_client_solve_with_images(mcq_client):
    with patch("lite.lite_mcq_client.LiteClient.generate_text") as mock_gen:
        mcq_input = MCQInput(
            question="Which image?", 
            options=["1", "2"], 
            image_paths=["a.jpg"],
            context="some context"
        )
        mcq_client.solve(mcq_input)
        
        # Check that prompt contains context and image note
        model_input = mock_gen.call_args[1]["model_input"]
        assert "Context:" in model_input.user_prompt
        assert "1 image(s) are provided" in model_input.user_prompt
        assert model_input.image_paths == ["a.jpg"]

def test_mcq_client_solve_error(mcq_client):
    with patch("lite.lite_mcq_client.LiteClient.generate_text", side_effect=Exception("API Error")):
        mcq_input = MCQInput(question="q", options=["a"])
        with pytest.raises(RuntimeError, match="Error solving question"):
            mcq_client.solve(mcq_input)

def test_mcq_format_options(mcq_client):
    # Dict options
    opts_dict = {"1": "One", "2": "Two"}
    formatted = mcq_client._format_options(opts_dict)
    assert "1: One" in formatted
    assert "2: Two" in formatted
    
    # List options
    opts_list = ["First", "Second"]
    formatted_list = mcq_client._format_options(opts_list)
    assert "A: First" in formatted_list
    assert "B: Second" in formatted_list

def test_judge_evaluate_success(judge):
    with patch("lite.lite_response_judge.LiteClient.generate_text") as mock_gen:
        scores = CriteriaScores(accuracy=1.0, completeness=1.0, relevance=1.0, clarity=1.0)
        eval_model = EvaluationModel(
            criteria=scores,
            overall_score=1.0,
            is_correct=True,
            reasoning="Perfect",
            feedback="None"
        )
        mock_gen.return_value = eval_model
        
        user_input = UserInput(model_response="4", user_prompt="2+2", ground_truth="4")
        result = judge.evaluate(user_input)
        
        assert result.overall_score == 1.0
        assert result.is_correct is True
        assert "2+2" in mock_gen.call_args[1]["model_input"].user_prompt

def test_judge_init_error():
    with pytest.raises(TypeError, match="requires a ModelConfig instance"):
        ResponseJudge("not a config")

def test_judge_evaluate_invalid_input(judge):
    with pytest.raises(TypeError, match="requires a UserInput instance"):
        judge.evaluate("not a user input")
    
    with pytest.raises(ValueError, match="model_response must not be empty"):
        judge.evaluate(UserInput(model_response=""))

def test_prompt_builder_ground_truth_context():
    from lite.lite_response_judge import PromptBuilder
    ui = UserInput(model_response="r", user_prompt="p", ground_truth="g", context="c")
    prompt = PromptBuilder.build_user_prompt(ui)
    assert "### Ground Truth:" in prompt
    assert "### Context:" in prompt
