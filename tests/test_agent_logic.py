import pytest
import os
import json
from unittest.mock import patch, MagicMock
from app.ArticleReviewer.article_reviewer import ArticleReviewer, ArticleReviewModel
from app.FAQGenerator.faq_generator import FAQGenerator, FAQInput, FAQ, FAQResponse, DataExporter
from lite.config import ModelConfig

@pytest.fixture
def article_reviewer():
    return ArticleReviewer(ModelConfig(model="gpt-4"))

@pytest.fixture
def faq_generator():
    return FAQGenerator(ModelConfig(model="gpt-4"))

def test_article_reviewer_review(article_reviewer):
    with patch("app.ArticleReviewer.article_reviewer.LiteClient.generate_text") as mock_gen:
        mock_review = ArticleReviewModel(
            score=80,
            summary="Good",
            total_issues=1,
            deletions=[{"line_number": 1, "content": "bad", "reason": "why", "severity": "low"}],
            modifications=[],
            insertions=[]
        )
        mock_gen.return_value = mock_review
        
        result = article_reviewer.review("some text")
        assert result.score == 80
        assert len(result.deletions) == 1

def test_article_reviewer_save_print(article_reviewer, tmp_path):
    review = ArticleReviewModel(score=90, summary="Excellent", total_issues=0, deletions=[], modifications=[], insertions=[])
    
    # Test print
    article_reviewer.print_review(review)
    
    # Test save
    out_dir = str(tmp_path / "out")
    path = article_reviewer.save_review(review, output_dir=out_dir)
    assert os.path.exists(path)

def test_faq_input_validation(tmp_path):
    # Valid
    FAQInput(input_source="Topic", num_faqs=5, difficulty="simple")
    
    # Invalid topic length
    with pytest.raises(ValueError, match="Topic must be 2-100 characters"):
        FAQInput(input_source="A", num_faqs=5, difficulty="simple")
    
    # Invalid num_faqs
    with pytest.raises(ValueError, match="Number of FAQs must be between 1 and 100"):
        FAQInput(input_source="Topic", num_faqs=0, difficulty="simple")

def test_faq_generator_file_read(faq_generator, tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("content")
    content = faq_generator._read_content_file(str(f))
    assert content == "content"
    
    # Non-existent file
    with pytest.raises(ValueError, match="Not a valid file"):
        faq_generator._read_content_file("nonexistent")

def test_faq_generator_generate(faq_generator):
    with patch("app.FAQGenerator.faq_generator.LiteClient.generate_text") as mock_gen:
        mock_faqs = [FAQ(question="What is Python?", answer="A language", difficulty="simple")]
        mock_gen.return_value = FAQResponse(topic="Python", difficulty="simple", num_faqs=1, faqs=mock_faqs)
        
        faq_input = FAQInput(input_source="Python", num_faqs=1, difficulty="simple")
        result = faq_generator.generate_text(faq_input)
        
        assert len(result) == 1
        assert result[0].question == "What is Python?"

def test_faq_data_exporter(tmp_path):
    faqs = [FAQ(question="Q1?", answer="A1 is long enough", difficulty="simple")]

    faq_input = FAQInput(input_source="Topic", num_faqs=1, difficulty="simple", output_dir=str(tmp_path))
    
    path = DataExporter.export_to_json(faqs, faq_input)
    assert os.path.exists(path)
    with open(path) as f:
        data = json.load(f)
    assert data["metadata"]["source"] == "Topic"
    assert len(data["faqs"]) == 1
