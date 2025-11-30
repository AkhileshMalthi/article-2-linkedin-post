"""
Unit tests for user_config module
"""

import pytest
from src.user_config import UserConfig


class TestUserConfig:
    """Test cases for UserConfig class"""

    def test_init_default_values(self):
        """Test UserConfig initialization with default values"""
        config = UserConfig()

        assert config.post_style == ""
        assert config.sample_posts == ""

    def test_init_with_post_style(self):
        """Test UserConfig initialization with post_style"""
        config = UserConfig(post_style="Professional with emojis")

        assert config.post_style == "Professional with emojis"
        assert config.sample_posts == ""

    def test_init_with_sample_posts(self):
        """Test UserConfig initialization with sample_posts"""
        sample = "Sample post 1\n\nSample post 2"
        config = UserConfig(sample_posts=sample)

        assert config.post_style == ""
        assert config.sample_posts == sample

    def test_init_with_both_parameters(self):
        """Test UserConfig initialization with both parameters"""
        style = "Casual and engaging"
        sample = "Example post"
        config = UserConfig(post_style=style, sample_posts=sample)

        assert config.post_style == style
        assert config.sample_posts == sample

    def test_modify_post_style(self):
        """Test modifying post_style after initialization"""
        config = UserConfig()
        config.post_style = "New style"

        assert config.post_style == "New style"

    def test_modify_sample_posts(self):
        """Test modifying sample_posts after initialization"""
        config = UserConfig()
        config.sample_posts = "New sample"

        assert config.sample_posts == "New sample"

    def test_empty_strings(self):
        """Test handling of empty strings"""
        config = UserConfig(post_style="", sample_posts="")

        assert config.post_style == ""
        assert config.sample_posts == ""

    def test_long_text(self):
        """Test handling of long text content"""
        long_style = "A" * 1000
        long_sample = "B" * 2000
        config = UserConfig(post_style=long_style, sample_posts=long_sample)

        assert len(config.post_style) == 1000
        assert len(config.sample_posts) == 2000

    def test_special_characters(self):
        """Test handling of special characters"""
        special = "Style with 🚀 emojis & special chars!@#$%"
        config = UserConfig(post_style=special)

        assert config.post_style == special


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
