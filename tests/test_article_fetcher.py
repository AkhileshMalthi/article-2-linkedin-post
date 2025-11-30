"""
Unit tests for article_fetcher module
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.article_fetcher import fetch_articles_by_topic


class TestFetchArticlesByTopic:
    """Test cases for fetch_articles_by_topic function"""

    @patch("src.article_fetcher.NewsApiClient")
    @patch.dict(os.environ, {"NEWS_API_KEY": "test_api_key"})
    def test_fetch_articles_success(self, mock_newsapi_class):
        """Test successful article fetching"""
        # Mock the NewsApiClient and its response
        mock_newsapi = MagicMock()
        mock_newsapi_class.return_value = mock_newsapi

        mock_response = {
            "articles": [
                {
                    "source": {"name": "TechCrunch"},
                    "author": "John Doe",
                    "title": "AI Revolution in 2024",
                    "description": "How AI is changing the world",
                    "url": "https://example.com/article1",
                    "urlToImage": "https://example.com/image1.jpg",
                    "publishedAt": "2024-01-15T10:00:00Z",
                    "content": "Full article content...",
                }
            ]
        }
        mock_newsapi.get_everything.return_value = mock_response

        # Test the function
        articles = fetch_articles_by_topic("Technology", count=1)

        # Assertions
        assert len(articles) == 1
        assert articles[0]["title"] == "AI Revolution in 2024"
        assert articles[0]["source"]["name"] == "TechCrunch"
        mock_newsapi_class.assert_called_once_with(api_key="test_api_key")
        mock_newsapi.get_everything.assert_called_once()

    @patch("src.article_fetcher.NewsApiClient")
    @patch.dict(os.environ, {"NEWS_API_KEY": "test_api_key"})
    def test_fetch_articles_with_custom_count(self, mock_newsapi_class):
        """Test fetching a specific number of articles"""
        mock_newsapi = MagicMock()
        mock_newsapi_class.return_value = mock_newsapi

        mock_response = {
            "articles": [
                {"source": {"name": f"Source{i}"}, "title": f"Title{i}"}
                for i in range(5)
            ]
        }
        mock_newsapi.get_everything.return_value = mock_response

        articles = fetch_articles_by_topic("AI", count=5)

        assert len(articles) == 5
        call_args = mock_newsapi.get_everything.call_args
        assert call_args.kwargs["page_size"] == 5

    @patch.dict(os.environ, {}, clear=True)
    def test_fetch_articles_missing_api_key(self):
        """Test handling of missing API key"""
        # Should return mock data when API key is missing
        articles = fetch_articles_by_topic("Technology", count=3)

        # Should return mock/demo data
        assert len(articles) == 3
        assert "title" in articles[0]
        assert "Technology" in articles[0]["title"]

    @patch("src.article_fetcher.NewsApiClient")
    @patch.dict(os.environ, {"NEWS_API_KEY": "test_api_key"})
    def test_fetch_articles_api_exception(self, mock_newsapi_class):
        """Test handling of API exceptions"""
        mock_newsapi = MagicMock()
        mock_newsapi_class.return_value = mock_newsapi
        mock_newsapi.get_everything.side_effect = Exception("API Error")

        # Should return mock data on exception
        articles = fetch_articles_by_topic("Science", count=2)

        assert len(articles) == 2
        assert "Science" in articles[0]["title"]

    @patch("src.article_fetcher.NewsApiClient")
    @patch.dict(os.environ, {"NEWS_API_KEY": "test_api_key"})
    def test_fetch_articles_parameters(self, mock_newsapi_class):
        """Test that correct parameters are passed to API"""
        mock_newsapi = MagicMock()
        mock_newsapi_class.return_value = mock_newsapi
        mock_newsapi.get_everything.return_value = {"articles": []}

        fetch_articles_by_topic("Business", count=10)

        call_args = mock_newsapi.get_everything.call_args
        assert call_args.kwargs["q"] == "Business"
        assert call_args.kwargs["language"] == "en"
        assert call_args.kwargs["sort_by"] == "popularity"
        assert "from_param" in call_args.kwargs
        assert "to" in call_args.kwargs
        assert call_args.kwargs["page_size"] == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
