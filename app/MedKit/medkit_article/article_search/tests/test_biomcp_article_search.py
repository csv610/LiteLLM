import pytest
import json
from unittest.mock import MagicMock, patch
from article_search.biomcp_article_search import MedicalArticleSearch

@pytest.fixture
def searcher():
    return MedicalArticleSearch()

def test_search_articles_empty_disease(searcher):
    assert searcher.search_articles("") == []
    assert searcher.search_articles("   ") == []

@patch('subprocess.run')
def test_search_articles_success(mock_run, searcher):
    # Mock JSON output of biomcp
    mock_data = [
        {
            "pmid": "12345",
            "title": "Test Article",
            "journal": "Test Journal",
            "date": "2024-01-01",
            "authors": ["Author A", "Author B"]
        }
    ]
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout=json.dumps(mock_data)
    )

    articles = searcher.search_articles("diabetes")
    
    assert len(articles) == 1
    assert articles[0]['title'] == "Test Article"
    assert articles[0]['pmid'] == "12345"
    assert articles[0]['authors'] == "Author A, Author B"
    assert articles[0]['year'] == "2024"

@patch('subprocess.run')
def test_search_articles_error(mock_run, searcher):
    # Mock error from biomcp
    mock_run.return_value = MagicMock(
        returncode=1,
        stderr="Error message"
    )

    with pytest.raises(Exception, match="Error running biomcp command"):
        searcher.search_articles("diabetes")

def test_get_article_citations(searcher):
    searcher.articles = [
        {
            'title': 'T1',
            'authors': ['A1', 'A2'],
            'journal': 'J1',
            'date': '2023-01-01',
            'pmid': 'P1'
        },
        {
            'title': 'T2',
            'authors': ['A3'],
            'journal': 'J2',
            'date': '2022',
            'pmid': 'P2'
        }
    ]
    # Update articles with extracted details
    for art in searcher.articles:
        art.update(searcher.extract_article_details(art))
        
    citations = searcher.get_article_citations()
    assert len(citations) == 2
    assert "1. T1, A1, A2. J1, 2023. PMID: P1" == citations[0]
    assert "2. T2, A3. J2, 2022. PMID: P2" == citations[1]

def test_get_article_count(searcher):
    searcher.articles = [{}, {}]
    assert searcher.get_article_count() == 2
