import random

def haiku_commit(message, files_changed=None, theme="nature"):
    """
    Generate a haiku based on commit message and changed files.
    
    Args:
        message (str): Original commit message
        files_changed (list): List of files that were changed (optional)
        theme (str): Theme to incorporate (nature, tech, emotion)
        
    Returns:
        str: Commit message as a haiku
    """
    if not isinstance(message, str) or not message:
        raise ValueError("Commit message must be a non-empty string")
    
    if files_changed is not None and not isinstance(files_changed, list):
        raise ValueError("files_changed must be a list or None")
    
    # Theme-based word pools for haiku generation
    themes = {
        "nature": {
            "nouns": ["leaf", "tree", "wind", "stream", "moon", "sun", "star", "rain", "cloud", "mountain", "ocean", "flower"],
            "verbs": ["grows", "flows", "shines", "falls", "rises", "drifts", "floats", "breathes", "blooms", "whispers"],
            "adjectives": ["silent", "gentle", "bright", "dark", "flowing", "quiet", "tall", "soft", "wild", "peaceful"]
        },
        "tech": {
            "nouns": ["code", "bit", "byte", "file", "data", "function", "loop", "script", "class", "object", "method", "server"],
            "verbs": ["runs", "compiles", "executes", "builds", "processes", "links", "connects", "validates", "transforms", "calculates"],
            "adjectives": ["elegant", "complex", "clean", "efficient", "powerful", "swift", "secure", "robust", "flexible", "innovative"]
        },
        "emotion": {
            "nouns": ["joy", "pain", "dream", "hope", "fear", "peace", "heart", "soul", "mind", "spirit", "smile", "tear"],
            "verbs": ["soars", "aches", "yearns", "calms", "races", "rests", "dances", "weeps", "laughs", "sighs"],
            "adjectives": ["joyful", "peaceful", "anxious", "serene", "excited", "calm", "fierce", "gentle", "brave", "tender"]
        }
    }
    
    # Get theme words or default to tech
    theme_words = themes.get(theme.lower(), themes["tech"])
    
    # Extract keywords from message and files
    keywords = message.lower().split()
    if files_changed:
        for file in files_changed:
            keywords.extend(file.replace(".", " ").replace("/", " ").split())
    
    # First line (5 syllables)
    # Use beginning of commit message, truncated if necessary
    first_line = message[:20] if len(message) <= 20 else message[:17] + "..."
    
    # Second line (7 syllables)
    # Choose from theme-based patterns
    adj = random.choice(theme_words["adjectives"])
    noun = random.choice(theme_words["nouns"])
    verb = random.choice(theme_words["verbs"])
    
    second_line_patterns = [
        f"{adj} {noun} {verb} now",
        f"through {adj} {noun} we {verb}",
        f"{noun} {verb} like {adj} dreams"
    ]
    second_line = random.choice(second_line_patterns)
    
    # Third line (5 syllables)
    # Reference files if available, otherwise use theme-based ending
    if files_changed and len(files_changed) > 0:
        # Extract file name without extension or path
        file_ref = files_changed[0].split("/")[-1].split(".")[0]
        third_line = f"changes in {file_ref}"
    else:
        third_line_patterns = [
            f"code {random.choice(['grows', 'flows', 'glows'])} {adj}",
            f"{noun} {verb} {adj}",
            f"work {random.choice(['complete', 'continues', 'progresses'])}"
        ]
        third_line = random.choice(third_line_patterns)
    
    # Combine into haiku format
    return f"{first_line}\n{second_line}\n{third_line}"