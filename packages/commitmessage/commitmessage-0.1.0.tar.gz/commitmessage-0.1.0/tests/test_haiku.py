import pytest
from commitmessage.haiku import haiku_commit

def test_haiku_basic_structure():
    """Test that haiku has correct structure (3 lines)."""
    result = haiku_commit("Fix login bug")
    lines = result.split("\n")
    assert len(lines) == 3
    assert len(lines[0]) > 0
    assert len(lines[1]) > 0
    assert len(lines[2]) > 0

def test_haiku_tech_theme():
    """Test haiku with tech theme."""
    result = haiku_commit("Update API endpoint", theme="tech")
    assert result.split("\n")[0].startswith("Update API endpoint")
    
    # Check that at least one tech term appears in the haiku
    tech_terms = ["code", "bit", "byte", "file", "data", "function", 
                  "loop", "script", "class", "object", "method", "server"]
    assert any(term in result.lower() for term in tech_terms)

def test_haiku_with_files():
    """Test haiku with files_changed parameter."""
    result = haiku_commit(
        "Refactor user model", 
        files_changed=["models/user.py", "controllers/user_controller.py"], 
        theme="tech"
    )
    assert "Refactor user model" in result.split("\n")[0]
    assert "user" in result.lower() or "models" in result.lower()

def test_haiku_nature_theme():
    """Test haiku with nature theme."""
    result = haiku_commit("Add login feature", theme="nature")
    assert result.split("\n")[0].startswith("Add login feature")
    
    # Check that at least one nature term appears in the haiku
    nature_terms = ["leaf", "tree", "wind", "stream", "moon", "sun", 
                    "star", "rain", "cloud", "mountain", "ocean", "flower"]
    assert any(term in result.lower() for term in nature_terms)

def test_haiku_emotion_theme():
    """Test haiku with emotion theme."""
    result = haiku_commit("Fix critical bug", theme="emotion")
    assert result.split("\n")[0].startswith("Fix critical bug")
    
    # Check that at least one emotion term appears in the haiku
    emotion_terms = ["joy", "pain", "dream", "hope", "fear", "peace", 
                     "heart", "soul", "mind", "spirit", "smile", "tear"]
    assert any(term in result.lower() for term in emotion_terms)

def test_haiku_empty_message():
    """Test haiku_commit with empty message."""
    with pytest.raises(ValueError):
        haiku_commit("")

def test_haiku_invalid_files_parameter():
    """Test haiku_commit with invalid files parameter."""
    with pytest.raises(ValueError):
        haiku_commit("Test message", files_changed="not_a_list")