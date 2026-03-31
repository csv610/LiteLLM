import json
import pytest
from unittest.mock import patch
import os

from ArticleReviewer.nonagentic.article_reviewer_models import DeleteModel, ModifyModel, InsertModel, ArticleReviewModel
from ArticleReviewer.nonagentic.article_reviewer_prompts import PromptBuilder
from ArticleReviewer.nonagentic.article_reviewer import ArticleReviewer
from lite.config import ModelConfig

# Test Models
def test_delete_model():
    data = {
        "line_number": 1,
        "content": "This is redundant.",
        "reason": "Redundancy",
        "severity": "low"
    }
    model = DeleteModel(**data)
    assert model.line_number == 1
    assert model.content == "This is redundant."
    assert model.severity == "low"

def test_modify_model():
    data = {
        "line_number": 5,
        "original_content": "The dog barked loud.",
        "suggested_modification": "The dog barked loudly.",
        "reason": "Adverb usage",
        "severity": "medium"
    }
    model = ModifyModel(**data)
    assert model.line_number == 5
    assert model.suggested_modification == "The dog barked loudly."

def test_insert_model():
    data = {
        "line_number": 10,
        "suggested_content": "In conclusion, testing is important.",
        "reason": "Missing conclusion",
        "section": "Conclusion",
        "severity": "high"
    }
    model = InsertModel(**data)
    assert model.section == "Conclusion"

def test_article_review_model():
    data = {
        "score": 85,
        "total_issues": 1,
        "summary": "Good article.",
        "deletions": [{"line_number": 1, "content": "X", "reason": "Y", "severity": "low"}],
        "modifications": [],
        "insertions": [],
        "proofreading_rules_applied": ["Grammar"]
    }
    model = ArticleReviewModel(**data)
    assert model.score == 85
    assert len(model.deletions) == 1

# Test PromptBuilder
def test_prompt_builder_create_prompt():
    article = "This is a test article."
    prompt = PromptBuilder.create_review_prompt(article)
    assert article in prompt
    assert "PROOFREADING RULES TO APPLY" in prompt
    assert "DELETION SUGGESTIONS" in prompt

def test_prompt_builder_rules():
    rules = PromptBuilder.get_proofreading_rules()
    assert "Grammar & Syntax" in rules
    assert "Style & Clarity" in rules
    
    categories = PromptBuilder.get_all_categories()
    assert "Grammar & Syntax" in categories

# Test ArticleReviewer
@pytest.fixture
def mock_lite_client():
    with patch('ArticleReviewer.nonagentic.article_reviewer.LiteClient') as mock:
        yield mock

def test_article_reviewer_init(mock_lite_client):
    reviewer = ArticleReviewer()
    assert reviewer.model_name == "ollama/gemma3"
    
    config = ModelConfig(model="gpt-4")
    reviewer = ArticleReviewer(model_config=config)
    assert reviewer.model_name == "gpt-4"

def test_article_reviewer_review(mock_lite_client):
    mock_instance = mock_lite_client.return_value
    review_data = {
        "score": 90,
        "total_issues": 2,
        "summary": "Great work.",
        "deletions": [
            {"line_number": 1, "content": "Extra word", "reason": "Redundant", "severity": "low"},
            {"line_number": 2, "content": " ", "reason": "Empty line", "severity": "low"} # Should be filtered
        ],
        "modifications": [
            {"line_number": 3, "original_content": "old", "suggested_modification": "new", "reason": "better", "severity": "medium"}
        ],
        "insertions": [],
        "proofreading_rules_applied": ["Style"]
    }
    mock_instance.generate_text.return_value = json.dumps(review_data)
    
    reviewer = ArticleReviewer()
    review = reviewer.review("Some article text")
    
    assert isinstance(review, ArticleReviewModel)
    assert review.score == 90
    assert len(review.deletions) == 1 # Empty line filtered
    assert review.total_issues == 2 # 1 deletion + 1 modification
    assert review.deletions[0].content == "Extra word"

def test_article_reviewer_review_object_response(mock_lite_client):
    mock_instance = mock_lite_client.return_value
    review_obj = ArticleReviewModel(
        score=95,
        total_issues=1,
        summary="Excellent work.",
        deletions=[
            DeleteModel(line_number=1, content="Extra", reason="Redundant", severity="low")
        ],
        modifications=[],
        insertions=[],
        proofreading_rules_applied=["Style"]
    )
    mock_instance.generate_text.return_value = review_obj
    
    reviewer = ArticleReviewer()
    review = reviewer.review("Some article text")
    
    assert isinstance(review, ArticleReviewModel)
    assert review.score == 95
    assert len(review.deletions) == 1
    assert review.total_issues == 1
    assert review.deletions[0].content == "Extra"

def test_article_reviewer_save_review(tmp_path):
    reviewer = ArticleReviewer()
    review = ArticleReviewModel(
        score=100, total_issues=0, summary="Perfect", 
        deletions=[], modifications=[], insertions=[], 
        proofreading_rules_applied=[]
    )
    
    # Test with output_filename
    out_file = tmp_path / "test_review.json"
    saved_path = reviewer.save_review(review, output_filename=str(out_file))
    assert os.path.exists(saved_path)
    with open(saved_path, 'r') as f:
        data = json.load(f)
        assert data["score"] == 100

    # Test with input_filename
    saved_path = reviewer.save_review(review, input_filename="my_article.txt")
    assert saved_path == os.path.join("outputs", "my_article_review.json")
    if os.path.exists(saved_path):
        os.remove(saved_path)

def test_article_reviewer_print_review(capsys):
    reviewer = ArticleReviewer()
    review = ArticleReviewModel(
        score=80, total_issues=1, summary="Fair", 
        deletions=[DeleteModel(line_number=1, content="Bad", reason="Why", severity="high")], 
        modifications=[], insertions=[], 
        proofreading_rules_applied=[]
    )
    reviewer.print_review(review)
    captured = capsys.readouterr()
    assert "ARTICLE REVIEW REPORT" in captured.out
    assert "Overall Score: 80/100" in captured.out
    assert "DELETIONS" in captured.out

# Test CLI functionality (article_reviewer_cli.py)
from ArticleReviewer.nonagentic.article_reviewer_cli import main

def test_cli_load_from_file(tmp_path):
    article_file = tmp_path / "article.txt"
    article_content = "This is a test article from a file."
    article_file.write_text(article_content)
    
    with patch('sys.argv', ['article_reviewer_cli.py', str(article_file)]), \
         patch('ArticleReviewer.nonagentic.article_reviewer_cli.cli') as mock_cli:
        main()
        mock_cli.assert_called_once()
        # The first argument to cli should be the content of the file
        assert mock_cli.call_args[0][0] == article_content
        # The fourth argument (input_filename) should be the file path
        assert mock_cli.call_args[0][3] == str(article_file)

def test_cli_load_from_json(tmp_path):
    article_file = tmp_path / "article.json"
    article_data = {"content": "Article from JSON"}
    article_file.write_text(json.dumps(article_data))
    
    with patch('sys.argv', ['article_reviewer_cli.py', str(article_file)]), \
         patch('ArticleReviewer.nonagentic.article_reviewer_cli.cli') as mock_cli:
        main()
        mock_cli.assert_called_once()
        assert mock_cli.call_args[0][0] == "Article from JSON"

def test_cli_direct_text():
    direct_text = "This is direct text"
    with patch('sys.argv', ['article_reviewer_cli.py', direct_text]), \
         patch('ArticleReviewer.nonagentic.article_reviewer_cli.cli') as mock_cli:
        main()
        mock_cli.assert_called_once()
        assert mock_cli.call_args[0][0] == direct_text
