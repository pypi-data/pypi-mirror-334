import pytest
from commitmessage import *

def test_emoji_feature_intensity_1():
    """Test emoji_commit with feature category and intensity 1."""
    result = emoji_commit("Add new login page", "feature", 1)
    assert "✨" in result
    assert "Add new login page" in result
    assert result.count("✨") == 1

def test_emoji_fix_intensity_2():
    """Test emoji_commit with fix category and intensity 2."""
    result = emoji_commit("Fix critical bug", "fix", 2)
    assert "🐛" in result
    assert "🔧" in result
    assert "Fix critical bug" in result

def test_emoji_docs_intensity_3():
    """Test emoji_commit with docs category and intensity 3."""
    result = emoji_commit("Update documentation", "docs", 3)
    assert "📚" in result
    assert "📝" in result
    assert "📄" in result
    assert "Update documentation" in result

def test_emoji_invalid_intensity():
    """Test emoji_commit with invalid intensity."""
    with pytest.raises(ValueError):
        emoji_commit("Test message", "feature", 0)
    
    with pytest.raises(ValueError):
        emoji_commit("Test message", "feature", 4)

def test_emoji_empty_message():
    """Test emoji_commit with empty message."""
    with pytest.raises(ValueError):
        emoji_commit("", "feature", 1)

def test_emoji_unknown_category_defaults_to_feature():
    """Test emoji_commit with unknown category defaults to feature category."""
    result = emoji_commit("Unknown category", "unknown", 1)
    assert "✨" in result
    assert "Unknown category" in result