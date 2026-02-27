import pytest
from unittest.mock import patch, MagicMock
from article_cli import main
import json
import io
from contextlib import redirect_stdout

@patch('article_cli.MedicalArticleSearch')
def test_cli_search_text_output(mock_search_class):
    # Setup mock
    mock_searcher = MagicMock()
    mock_search_class.return_value = mock_searcher
    mock_searcher.search_articles.return_value = [
        {
            'title': 'Test Title',
            'journal': 'Test Journal',
            'date': '2024-01-01',
            'pmid': '12345',
            'doi': '10.1234/5678',
            'authors': 'Author A, Author B'
        }
    ]

    with patch('sys.argv', ['article_cli.py', 'search', 'diabetes']):
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        output = f.getvalue()
        
    assert "Found 1 articles for 'diabetes'" in output
    assert "Test Title" in output
    assert "PMID: 12345" in output

@patch('article_cli.MedicalArticleSearch')
def test_cli_search_json_output(mock_search_class):
    # Setup mock
    mock_searcher = MagicMock()
    mock_search_class.return_value = mock_searcher
    articles = [
        {
            'title': 'Test Title',
            'journal': 'Test Journal',
            'date': '2024-01-01',
            'pmid': '12345',
            'doi': '10.1234/5678'
        }
    ]
    mock_searcher.search_articles.return_value = articles

    with patch('sys.argv', ['article_cli.py', 'search', 'diabetes', '--json']):
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        output = f.getvalue()
        
    parsed_output = json.loads(output)
    assert len(parsed_output) == 1
    assert parsed_output[0]['title'] == 'Test Title'

@patch('article_cli.MedicalArticleSearch')
def test_cli_cite_output(mock_search_class):
    # Setup mock
    mock_searcher = MagicMock()
    mock_search_class.return_value = mock_searcher
    mock_searcher.search_articles.return_value = [{}] # Just to make it not empty
    mock_searcher.get_article_citations.return_value = ["1. Citation 1", "2. Citation 2"]

    with patch('sys.argv', ['article_cli.py', 'cite', 'diabetes']):
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        output = f.getvalue()
        
    assert "Citations for 'diabetes':" in output
    assert "1. Citation 1" in output
    assert "2. Citation 2" in output

@patch('article_cli.MedicalArticleSearch')
def test_cli_no_articles(mock_search_class):
    # Setup mock
    mock_searcher = MagicMock()
    mock_search_class.return_value = mock_searcher
    mock_searcher.search_articles.return_value = []

    with patch('sys.argv', ['article_cli.py', 'search', 'disease_x']):
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        output = f.getvalue()
        
    assert "No articles found for 'disease_x'." in output
