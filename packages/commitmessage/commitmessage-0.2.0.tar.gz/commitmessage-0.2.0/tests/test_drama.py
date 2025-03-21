import pytest
from commitmessage.drama import drama_commit

def test_drama_feature_intensity_1():
    """Test drama_commit with feature category and intensity 1."""
    result = drama_commit("Add new login page", "feature", 1)
    assert "Check out this new feature!" in result
    assert "Add new login page" in result

def test_drama_feature_intensity_2():
    """Test drama_commit with feature category and intensity 2."""
    result = drama_commit("Add new login page", "feature", 2)
    assert "Wow! Check out this amazing new feature!" in result
    assert "Add new login page" in result

def test_drama_feature_intensity_3():
    """Test drama_commit with feature category and intensity 3."""
    result = drama_commit("Add new login page", "feature", 3)
    assert "WOOOOOOOOO" in result
    assert "ADD NEW LOGIN PAGE" in result
    assert result.count("!") == 13

def test_drama_invalid_intensity():
    """Test drama_commit with invalid intensity."""
    with pytest.raises(ValueError):
        drama_commit("Test message", "feature", 0)

    with pytest.raises(ValueError):
        drama_commit("Test message", "feature", 4)

def test_drama_empty_message():
    """Test drama_commit with empty message."""
    with pytest.raises(ValueError):
        drama_commit("", "feature", 1)

def test_drama_unknown_category():
    """Test drama_commit with unknown category defaults to feature category."""
    with pytest.raises(ValueError):
        drama_commit("Unknown category", "unknown", 1)