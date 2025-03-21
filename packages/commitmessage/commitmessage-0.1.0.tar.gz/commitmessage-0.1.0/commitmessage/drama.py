def drama_commit(message, category, intensity):
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
    
    match category.lower():
        case 'feature':
            if intensity==1:
                return 'Check out this new feature! '+ message
            if intensity==2:
                return 'Wow! Check out this amazing new feature! '+message
            return 'WOOOOOOOOO!!!! THIS NEW FEATURE IS AMAZING!!!!! '+message.upper()+'!!!!'
        
        case 'fix':
            if intensity==1:
                return 'I fixed a bug! '+message
            if intensity==2:
                return 'Yay! Squashed a bug! '+message
            return 'A BUG HAS BEEN ERADICATED!!!!! '+message.upper()+'!!!!'
        
        case 'docs':
            if intensity==1:
                return 'Made some documentation improvements! '+message
            if intensity==2:
                return 'Spruced up the documentation! Check it out! '+message
            return 'OUR DOCUMENTATION IS SO MUCH BETTER NOW THANKS TO ME!!!! '+message.upper()+'!!!!'
        
        case 'refactor':
            if intensity==1:
                return 'Refactored some code! '+message
            if intensity==2:
                return 'Check out this refactored code! '+message
            return 'I CANT BELIEVE HOW MUCH BETTER THIS REFACTORED CODE IS!!!!! '+message.upper()+'!!!!'
        
        case 'test':
            if intensity==1:
                return 'Added some new tests! '+message
            if intensity==2:
                return 'Improved our coverage with some new tests! '+message
            return 'OUR CODE IS COVERED NOW THANKS TO THESE TESTS!!!! '+message.upper()+'!!!!'
        
        case _:
            raise ValueError("Category must be one of the following: feature, fix docs, refactor, test")