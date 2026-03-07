from unittest.mock import patch

from articles_search_sl import display_articles


@patch("articles_search_sl.st")
def test_display_articles_empty(mock_st):
    display_articles([])
    mock_st.info.assert_called_with("No valid articles found.")


@patch("articles_search_sl.st")
def test_display_articles_success(mock_st):
    articles = [
        {"title": "T1", "authors": "A1", "journal": "J1", "year": "2023", "pmid": "P1"}
    ]
    display_articles(articles)
    mock_st.markdown.assert_called()
    call_args = mock_st.markdown.call_args[0][0]
    assert "T1" in call_args
    assert "A1" in call_args
    assert "J1" in call_args
    assert "2023" in call_args
    assert "PMID: P1" in call_args
