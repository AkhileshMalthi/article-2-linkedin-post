"""
Unit tests for prompts module
"""

import pytest
from src.prompts import SYSTEM_TEMPLATE, USER_TEMPLATE, get_few_shot_examples
from src.user_config import UserConfig


class TestPromptTemplates:
    """Test cases for prompt templates"""

    def test_system_template_exists(self):
        """Test that SYSTEM_TEMPLATE is defined"""
        assert SYSTEM_TEMPLATE is not None
        assert isinstance(SYSTEM_TEMPLATE, str)
        assert len(SYSTEM_TEMPLATE) > 0

    def test_system_template_content(self):
        """Test SYSTEM_TEMPLATE contains expected content"""
        assert "LinkedIn" in SYSTEM_TEMPLATE
        assert "post" in SYSTEM_TEMPLATE.lower()

    def test_user_template_exists(self):
        """Test that USER_TEMPLATE is defined"""
        assert USER_TEMPLATE is not None
        assert isinstance(USER_TEMPLATE, str)
        assert len(USER_TEMPLATE) > 0

    def test_user_template_placeholders(self):
        """Test USER_TEMPLATE contains required placeholders"""
        assert "{title}" in USER_TEMPLATE
        assert "{source}" in USER_TEMPLATE
        assert "{description}" in USER_TEMPLATE
        assert "{style_preferences}" in USER_TEMPLATE
        assert "{few_shot_examples}" in USER_TEMPLATE

    def test_user_template_structure(self):
        """Test USER_TEMPLATE has proper structure"""
        assert "Title:" in USER_TEMPLATE
        assert "Source:" in USER_TEMPLATE
        assert "Description:" in USER_TEMPLATE
        assert "User Style Preferences:" in USER_TEMPLATE


class TestGetFewShotExamples:
    """Test cases for get_few_shot_examples function"""

    def test_with_empty_sample_posts(self):
        """Test get_few_shot_examples with empty sample_posts"""
        config = UserConfig(post_style="", sample_posts="")
        result = get_few_shot_examples(config)

        assert result == ""

    def test_with_sample_posts(self):
        """Test get_few_shot_examples with sample_posts"""
        sample = "Sample post 1\n\nSample post 2"
        config = UserConfig(sample_posts=sample)
        result = get_few_shot_examples(config)

        assert "Here are sample posts from the user for reference:" in result
        assert sample in result
        assert len(result) > len(sample)

    def test_with_single_sample_post(self):
        """Test get_few_shot_examples with single sample post"""
        sample = "Just one sample post"
        config = UserConfig(sample_posts=sample)
        result = get_few_shot_examples(config)

        assert sample in result
        assert "sample posts" in result.lower()

    def test_with_multiline_sample_posts(self):
        """Test get_few_shot_examples with multiline content"""
        sample = """Post 1: This is a great article!
        
I learned so much from this piece.

#Technology #Innovation

---

Post 2: Another example post here."""
        config = UserConfig(sample_posts=sample)
        result = get_few_shot_examples(config)

        assert sample in result
        assert "Post 1" in result
        assert "Post 2" in result

    def test_return_type(self):
        """Test that get_few_shot_examples always returns a string"""
        config1 = UserConfig(sample_posts="")
        config2 = UserConfig(sample_posts="Sample")

        assert isinstance(get_few_shot_examples(config1), str)
        assert isinstance(get_few_shot_examples(config2), str)

    def test_with_special_characters_in_samples(self):
        """Test handling of special characters in sample posts"""
        sample = "Post with emojis 🚀💡 and symbols @#$%"
        config = UserConfig(sample_posts=sample)
        result = get_few_shot_examples(config)

        assert sample in result
        assert "🚀" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
