import pytest
from commitmessage import *

def test_style_pirate_strength_1():
    """Test style_commit with pirate style and strength 1."""
    result = style_commit("Fix login bug", "pirate", 1)
    assert any(prefix in result for prefix in ["Yarr! ", "Ahoy! ", "Avast! "])
    assert "login bug" in result.lower()

def test_style_superhero_strength_2():
    """Test style_commit with superhero style and strength 2."""
    result = style_commit("Add new feature", "superhero", 2)
    assert any(prefix in result for prefix in ["Kapow! ", "To the rescue! ", "Holy code change! "])
    assert "feature" in result.lower()

def test_style_medieval_strength_3():
    """Test style_commit with medieval style and strength 3."""
    result = style_commit("Update user profile", "medieval", 3)
    assert any(prefix in result for prefix in ["By the old gods and the new! ", "For glory and honor! ", "In the name of the kingdom! "])
    assert "profile" in result.lower()

def test_style_action_word_replacement():
    """Test that action words are replaced appropriately."""
    result = style_commit("Fix login bug", "pirate", 2)
    assert "repair" in result.lower() or "leaky" in result.lower()
    assert "fix" not in result.lower()

def test_style_invalid_strength():
    """Test style_commit with invalid strength."""
    with pytest.raises(ValueError):
        style_commit("Test message", "pirate", 0)
    
    with pytest.raises(ValueError):
        style_commit("Test message", "pirate", 4)

def test_style_empty_message():
    """Test style_commit with empty message."""
    with pytest.raises(ValueError):
        style_commit("", "pirate", 1)

def test_style_unknown_style_defaults_to_pirate():
    """Test style_commit with unknown style defaults to pirate style."""
    result = style_commit("Fix login bug", "nonexistent", 1)
    assert any(prefix in result for prefix in ["Yarr! ", "Ahoy! ", "Avast! "])