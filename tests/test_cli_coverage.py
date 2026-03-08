import pytest
from unittest.mock import patch, MagicMock
from app.ArticleReviewer.article_reviewer_cli import main as article_main
from app.FAQGenerator.faq_generator_cli import main as faq_main

@patch("app.ArticleReviewer.article_reviewer_cli.ArticleReviewer")
@patch("argparse.ArgumentParser.parse_args")
def test_article_reviewer_cli_main(mock_args, mock_reviewer_class, tmp_path):
    mock_args.return_value = MagicMock(article="test text", model="gpt-4", output="out.json")
    mock_reviewer = mock_reviewer_class.return_value
    mock_reviewer.review.return_value = MagicMock()
    mock_reviewer.save_review.return_value = "out.json"
    
    article_main()
    
    mock_reviewer_class.assert_called_once()
    mock_reviewer.review.assert_called_with("test text")

@patch("app.ArticleReviewer.article_reviewer_cli.ArticleReviewer")
@patch("argparse.ArgumentParser.parse_args")
def test_article_reviewer_cli_file_input(mock_args, mock_reviewer_class, tmp_path):
    article_file = tmp_path / "article.txt"
    article_file.write_text("file content")
    mock_args.return_value = MagicMock(article=str(article_file), model=None, output=None)
    
    article_main()
    mock_reviewer_class.return_value.review.assert_called_with("file content")

@patch("app.FAQGenerator.faq_generator_cli.DataExporter")
@patch("app.FAQGenerator.faq_generator_cli.FAQGenerator")
@patch("argparse.ArgumentParser.parse_args")
def test_faq_generator_cli_main(mock_args, mock_gen_class, mock_exporter, tmp_path):
    mock_args.return_value = MagicMock(
        input_source="AI", 
        num_faqs=5, 
        difficulty="medium",
        model="gpt-4",
        temperature=0.7,
        output_dir=str(tmp_path)
    )
    mock_gen = mock_gen_class.return_value
    mock_gen.generate_text.return_value = ["FAQ 1"]
    mock_exporter.export_to_json.return_value = "faq.json"
    
    from app.FAQGenerator.faq_generator_cli import main as faq_main
    assert faq_main() == 0
    mock_gen_class.assert_called_once()

@patch("lite.lite_mcq_client.print_answer")
@patch("lite.lite_mcq_client.LiteMCQClient")
@patch("argparse.ArgumentParser.parse_args")
def test_lite_mcq_cli(mock_args, mock_mcq_class, mock_print):
    from lite.lite_mcq_client import MultipleChoiceAnswer, CorrectOption
    mock_args.return_value = MagicMock(
        question="What is 2+2?",
        options=["3", "4"],
        context=None,
        images=None,
        model="gpt-4",
        file=None
    )
    mock_mcq = mock_mcq_class.return_value
    mock_mcq.solve.return_value = MultipleChoiceAnswer(
        question="What is 2+2?",
        correct_options=[CorrectOption(key="B", value="4")],
        reasoning="Math",
        confidence=1.0
    )
    
    from lite.lite_mcq_client import main as mcq_main
    mcq_main()
    mock_mcq.solve.assert_called_once()

@patch("lite.lite_response_judge.ResponseJudge")
@patch("argparse.ArgumentParser.parse_args")
def test_lite_judge_cli(mock_args, mock_judge_class):
    from lite.lite_response_judge import EvaluationModel, CriteriaScores
    mock_args.return_value = MagicMock(
        prompt="2+2",
        response="4",
        ground_truth="4",
        model="gpt-4"
    )
    mock_judge = mock_judge_class.return_value
    
    # Use real Pydantic models
    scores = CriteriaScores(accuracy=1.0, completeness=1.0, relevance=1.0, clarity=1.0)
    eval_model = EvaluationModel(
        criteria=scores,
        overall_score=1.0,
        is_correct=True,
        reasoning="Correct"
    )
    mock_judge.evaluate.return_value = eval_model
    
    from lite.lite_response_judge import main as judge_main
    judge_main()
    mock_judge.evaluate.assert_called_once()

@patch("lite.lite_mcq_client.LiteMCQClient")
@patch("argparse.ArgumentParser.parse_args")
def test_lite_mcq_cli_file(mock_args, mock_mcq_class, tmp_path):
    from lite.lite_mcq_client import MultipleChoiceAnswer, CorrectOption
    q_file = tmp_path / "q.json"
    import json
    q_file.write_text(json.dumps({
        "question": "What is 1+1?",
        "options": ["1", "2"]
    }))
    
    mock_args.return_value = MagicMock(
        file=str(q_file),
        model="gpt-4",
        question=None,
        options=None
    )
    mock_mcq = mock_mcq_class.return_value
    mock_mcq.solve.return_value = MultipleChoiceAnswer(
        question="What is 1+1?",
        correct_options=[CorrectOption(key="B", value="2")],
        reasoning="Math",
        confidence=1.0
    )
    
    from lite.lite_mcq_client import main as mcq_main
    mcq_main()
    mock_mcq.solve.assert_called_once()

@patch("lite.lite_chat.input", create=True)
@patch("lite.lite_chat.LiteChat")
@patch("argparse.ArgumentParser.parse_args")
def test_lite_chat_cli(mock_args, mock_chat_class, mock_input, tmp_path):
    mock_args.return_value = MagicMock(
        model="gpt-4",
        temperature=0.7,
        max_history=10,
        auto_save=False,
        save_dir=str(tmp_path),
        image_path=None
    )
    # Simulate user typing 'exit' immediately
    mock_input.side_effect = ["exit"]
    
    from lite.lite_chat import cli
    cli()
    mock_chat_class.assert_called_once()
