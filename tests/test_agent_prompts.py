import pytest
from app.ArticleReviewer.article_reviewer_prompts import PromptBuilder as ArticlePromptBuilder
from app.FAQGenerator.faq_generator_prompts import PromptBuilder as FAQPromptBuilder

def test_article_prompt_builder():
    prompt = ArticlePromptBuilder.create_review_prompt("test text")
    assert "test text" in prompt
    assert "PROOFREADING RULES" in prompt
    
    rules = ArticlePromptBuilder.get_proofreading_rules()
    assert "Grammar & Syntax" in rules
    
    cat_rules = ArticlePromptBuilder.get_rules_by_category("Consistency")
    assert "terminology" in cat_rules
    
    cats = ArticlePromptBuilder.get_all_categories()
    assert "Style & Clarity" in cats

def test_faq_prompt_builder_topic():
    builder = FAQPromptBuilder(num_faqs=3, difficulty="hard")
    prompt = builder.build_topic_prompt("Quantum Physics")
    assert "Quantum Physics" in prompt
    assert "3 frequently asked questions" in prompt
    assert "advanced topics" in prompt

def test_faq_prompt_builder_content():
    builder = FAQPromptBuilder(num_faqs=5, difficulty="research")
    prompt = builder.build_content_prompt("The study of cells...")
    assert "The study of cells..." in prompt
    assert "cutting-edge research" in prompt
    assert "RESEARCH-LEVEL FOCUS" in prompt

def test_faq_prompt_builder_default_desc():
    builder = FAQPromptBuilder(num_faqs=1, difficulty="unknown")
    assert "intermediate level" in builder.level_desc
