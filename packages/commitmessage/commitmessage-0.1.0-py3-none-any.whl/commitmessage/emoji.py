def emoji_commit(message, category="feature", intensity=1):
    """
    Add relevant emojis to commit messages based on category and intensity.
    
    Args:
        message (str): Original commit message
        category (str): Type of commit (feature, fix, docs, refactor, test, style, chore)
        intensity (int): Number of emojis to add (1-3)
        
    Returns:
        str: Emoji-enhanced commit message
    """
    if not isinstance(message, str) or not message:
        raise ValueError("Commit message must be a non-empty string")
    
    if not isinstance(intensity, int) or intensity < 1 or intensity > 3:
        raise ValueError("Intensity must be between 1 and 3")
    
    # Category-to-emoji mapping
    emoji_map = {
        "feature": ["✨", "🚀", "🎉"],
        "fix": ["🐛", "🔧", "🩹"],
        "docs": ["📚", "📝", "📄"],
        "refactor": ["♻️", "🔨", "🧹"],
        "test": ["🧪", "✅", "🔍"],
        "style": ["💅", "🎨", "✂️"],
        "chore": ["🔧", "🧰", "🧹"],
        "perf": ["⚡", "🏎️", "⏱️"],
        "ci": ["👷", "🤖", "🔄"],
        "build": ["📦", "🔨", "🏗️"],
        "security": ["🔒", "🛡️", "🔐"]
    }
    
    # Default to feature if category not found
    category = category.lower()
    emojis = emoji_map.get(category, emoji_map["feature"])
    selected_emojis = emojis[:intensity]
    
    # Add emojis to message
    emoji_prefix = " ".join(selected_emojis) + " "
    return emoji_prefix + message