"""
Unit tests for post_generator module
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from src.post_generator import generate_linkedin_post
from src.user_config import UserConfig


class TestGenerateLinkedInPost:
    """Test cases for generate_linkedin_post function"""

    @pytest.fixture
    def sample_article(self):
        """Fixture for sample article data"""
        return {
            "source": {"name": "TechCrunch"},
            "author": "Jane Smith",
            "title": "The Future of AI in Healthcare",
            "description": "Exploring how artificial intelligence is revolutionizing medical diagnostics",
            "url": "https://example.com/article",
            "urlToImage": "https://example.com/image.jpg",
            "publishedAt": "2024-01-15T10:00:00Z",
            "content": "Full article content about AI in healthcare...",
        }

    @pytest.fixture
    def sample_user_config(self):
        """Fixture for user configuration"""
        return UserConfig(
            post_style="Professional tone with emojis, 3-4 paragraphs", sample_posts=""
        )

    @patch("src.post_generator.ChatGroq")
    @patch.dict(
        os.environ,
        {"GROQ_API_KEY": "test_key", "GROQ_MODEL": "llama-3.3-70b-versatile"},
    )
    def test_generate_post_success(
        self, mock_chatgroq, sample_article, sample_user_config
    ):
        """Test successful post generation"""
        # Mock the LLM response
        mock_llm_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "🚀 Exciting developments in AI healthcare!\n\nThis article highlights...\n\n#AI #Healthcare"
        # The chain uses () to call, so we mock __call__ which returns the response
        mock_llm_instance.return_value = mock_response
        mock_chatgroq.return_value = mock_llm_instance

        # Generate post
        post = generate_linkedin_post(sample_article, sample_user_config)

        # Assertions
        assert isinstance(post, str)
        assert len(post) > 0
        assert (
            post
            == "🚀 Exciting developments in AI healthcare!\n\nThis article highlights...\n\n#AI #Healthcare"
        )
        mock_chatgroq.assert_called_once()

    @patch("src.post_generator.ChatGroq")
    @patch.dict(
        os.environ,
        {"GROQ_API_KEY": "test_key", "GROQ_MODEL": "llama-3.3-70b-versatile"},
    )
    def test_generate_post_with_sample_posts(self, mock_chatgroq, sample_article):
        """Test post generation with few-shot examples"""
        user_config = UserConfig(
            post_style="Casual and engaging",
            sample_posts="Sample post 1\n\nSample post 2",
        )

        mock_llm_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Generated post with style"
        mock_llm_instance.return_value = mock_response
        mock_chatgroq.return_value = mock_llm_instance

        post = generate_linkedin_post(sample_article, user_config)

        assert isinstance(post, str)
        assert len(post) > 0

    @patch("src.post_generator.ChatGroq")
    @patch.dict(
        os.environ,
        {"GROQ_API_KEY": "test_key", "GROQ_MODEL": "llama-3.3-70b-versatile"},
    )
    def test_generate_post_with_no_description(self, mock_chatgroq, sample_user_config):
        """Test post generation when article has no description"""
        article = {
            "source": {"name": "Example"},
            "title": "Test Article",
            "description": None,
            "url": "https://example.com",
        }

        mock_llm_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Generated post"
        mock_llm_instance.return_value = mock_response
        mock_chatgroq.return_value = mock_llm_instance

        post = generate_linkedin_post(article, sample_user_config)

        assert isinstance(post, str)
        assert post == "Generated post"

    @patch("src.post_generator.ChatGroq")
    @patch.dict(
        os.environ,
        {"GROQ_API_KEY": "test_key", "GROQ_MODEL": "llama-3.3-70b-versatile"},
    )
    def test_generate_post_exception_handling(
        self, mock_chatgroq, sample_article, sample_user_config
    ):
        """Test fallback behavior when LLM call fails"""
        mock_chatgroq.side_effect = Exception("API Error")

        post = generate_linkedin_post(sample_article, sample_user_config)

        # Should return fallback post
        assert isinstance(post, str)
        assert sample_article["title"] in post
        assert sample_article["source"]["name"].replace(" ", "") in post

    @patch("src.post_generator.ChatGroq")
    @patch.dict(
        os.environ,
        {"GROQ_API_KEY": "test_key", "GROQ_MODEL": "llama-3.3-70b-versatile"},
    )
    def test_generate_post_response_formats(
        self, mock_chatgroq, sample_article, sample_user_config
    ):
        """Test handling different response formats from LLM"""
        mock_llm_instance = MagicMock()
        mock_chatgroq.return_value = mock_llm_instance

        # Test with string response
        mock_llm_instance.return_value = "Direct string response"
        post = generate_linkedin_post(sample_article, sample_user_config)
        assert post == "Direct string response"

        # Test with dict response
        mock_llm_instance.return_value = {"content": "Dict response"}
        post = generate_linkedin_post(sample_article, sample_user_config)
        assert post == "Dict response"

    @patch("src.post_generator.ChatGroq")
    @patch.dict(os.environ, {}, clear=True)
    def test_generate_post_missing_env_vars(
        self, mock_chatgroq, sample_article, sample_user_config
    ):
        """Test behavior with missing environment variables"""
        # The function passes error messages as defaults, so it should still try to initialize
        mock_llm_instance = MagicMock()
        mock_chatgroq.return_value = mock_llm_instance
        mock_llm_instance.side_effect = Exception("Invalid API key")

        post = generate_linkedin_post(sample_article, sample_user_config)

        # Should return fallback post
        assert isinstance(post, str)
        assert sample_article["title"] in post


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
