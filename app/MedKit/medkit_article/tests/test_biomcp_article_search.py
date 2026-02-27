import pytest
from unittest.mock import MagicMock, patch
from biomcp_article_search import MedicalArticleSearch

@pytest.fixture
def searcher():
    return MedicalArticleSearch()

def test_search_articles_empty_disease(searcher):
    assert searcher.search_articles("") == []
    assert searcher.search_articles("   ") == []

@patch('subprocess.run')
def test_search_articles_success(mock_run, searcher):
    # Mock output of biomcp
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="""# Record 1
Pmid: 12345
Title: Test Article
Journal: Test Journal
Date: 2024-01-01
Authors: Author A, Author B
"""
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

def test_parse_articles(searcher):
    sample_output = """
# Record 1
Pmid: 1
Title: Title 1
Journal: Journal 1
Date: 2023-01-01
Authors: Author 1

# Record 2
Pmid: 2
Title: Title 2
Journal: Journal 2
Date: 2022
Authors: Author 2, Author 3
"""
    articles = searcher.parse_articles(sample_output)
    assert len(articles) == 2
    assert articles[0]['title'] == "Title 1"
    assert articles[1]['pmid'] == "2"
    assert articles[1]['year'] == "2022"

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
    citations = searcher.get_article_citations()
    assert len(citations) == 2
    assert "1. T1, A1, A2. J1, 2023. PMID: P1" == citations[0]
    assert "2. T2, A3. J2, 2022. PMID: P2" == citations[1]

def test_get_article_count(searcher):
    searcher.articles = [{}, {}]
    assert searcher.get_article_count() == 2
