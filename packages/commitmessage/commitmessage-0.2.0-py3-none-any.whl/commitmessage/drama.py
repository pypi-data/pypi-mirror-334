def drama_commit(message, category='feature', intensity=1):
    """
    Turn boring commit messages into dramatic ones based on category and with variable intensity.
    
    Args:
        message (str): Original commit message
        category (str): Type of commit (feature, fix, docs, refactor, test)
        intensity (int): How dramatic to make the message (1-3)
        
    Returns:
        str: Dramatized commit message
    """
    if not isinstance(message, str) or not message:
        raise ValueError("Commit message must be a non-empty string")
    
    if not isinstance(intensity, int) or intensity < 1 or intensity > 3:
        raise ValueError("Intensity must be between 1 and 3")
    
    category_lower = category.lower()
    
    if category_lower == 'feature':
        if intensity == 1:
            return 'Check out this new feature! ' + message
        elif intensity == 2:
            return 'Wow! Check out this amazing new feature! ' + message
        else:
            return 'WOOOOOOOOO!!!! THIS NEW FEATURE IS AMAZING!!!!! ' + message.upper() + '!!!!'
    
    elif category_lower == 'fix':
        if intensity == 1:
            return 'I fixed a bug! ' + message
        elif intensity == 2:
            return 'Yay! Squashed a bug! ' + message
        else:
            return 'A BUG HAS BEEN ERADICATED!!!!! ' + message.upper() + '!!!!'
    
    elif category_lower == 'docs':
        if intensity == 1:
            return 'Made some documentation improvements! ' + message
        elif intensity == 2:
            return 'Spruced up the documentation! Check it out! ' + message
        else:
            return 'OUR DOCUMENTATION IS SO MUCH BETTER NOW THANKS TO ME!!!! ' + message.upper() + '!!!!'
    
    elif category_lower == 'refactor':
        if intensity == 1:
            return 'Refactored some code! ' + message
        elif intensity == 2:
            return 'Check out this refactored code! ' + message
        else:
            return 'I CANT BELIEVE HOW MUCH BETTER THIS REFACTORED CODE IS!!!!! ' + message.upper() + '!!!!'
    
    elif category_lower == 'test':
        if intensity == 1:
            return 'Added some new tests! ' + message
        elif intensity == 2:
            return 'Improved our coverage with some new tests! ' + message
        else:
            return 'OUR CODE IS COVERED NOW THANKS TO THESE TESTS!!!! ' + message.upper() + '!!!!'
    
    else:
        raise ValueError("Category must be one of the following: feature, fix, docs, refactor, test")
