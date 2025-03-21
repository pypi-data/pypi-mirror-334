import random

def style_commit(message, style="pirate", strength=2):
    """
    Transform commit messages into various fun styles.
    
    Args:
        message (str): Original commit message
        style (str): Style theme (pirate, superhero, medieval, sci-fi, noir, western)
        strength (int): How strongly to apply the style (1-3)
        
    Returns:
        str: Styled commit message
    """
    if not isinstance(message, str) or not message:
        raise ValueError("Commit message must be a non-empty string")
    
    if not isinstance(strength, int) or strength < 1 or strength > 3:
        raise ValueError("Strength must be between 1 and 3")
    
    # Style templates with varying strength levels
    style_templates = {
        "pirate": {
            1: {
                "prefix": ["Yarr! ", "Ahoy! ", "Avast! "],
                "words": {"fix": "patch", "add": "hoist", "update": "upgrade", "remove": "maroon"}
            },
            2: {
                "prefix": ["Shiver me timbers! ", "Yo-ho-ho! ", "Ahoy, mateys! "],
                "words": {"fix": "repair the leaky", "add": "bring aboard", "update": "refit", "remove": "keelhaul"}
            },
            3: {
                "prefix": ["Arr, me hearties! ", "By Blackbeard's beard! ", "Prepare to be boarded! "],
                "words": {
                    "fix": "mend the vessel", 
                    "add": "plunder and stash", 
                    "update": "transform the seaworthy", 
                    "remove": "send to Davy Jones' locker"
                }
            }
        },
        "superhero": {
            1: {
                "prefix": ["Pow! ", "Zoom! ", "Bam! "],
                "words": {"fix": "rescue", "add": "power up with", "update": "enhance", "remove": "defeat"}
            },
            2: {
                "prefix": ["Kapow! ", "To the rescue! ", "Holy code change! "],
                "words": {"fix": "save the day by fixing", "add": "unleash", "update": "supercharge", "remove": "vanquish"}
            },
            3: {
                "prefix": ["WHAM! BAM! ", "With great power! ", "Up, up and away! "],
                "words": {
                    "fix": "swoop in and rescue", 
                    "add": "summon the power of", 
                    "update": "transform with incredible", 
                    "remove": "triumph over the villainous"
                }
            }
        },
        "medieval": {
            1: {
                "prefix": ["Hark! ", "Huzzah! ", "Behold! "],
                "words": {"fix": "mend", "add": "forge", "update": "enchant", "remove": "banish"}
            },
            2: {
                "prefix": ["Hear ye! ", "By the king's decree! ", "Onwards, brave knights! "],
                "words": {"fix": "restore honor to", "add": "bestow upon thee", "update": "transform by magic", "remove": "exile"}
            },
            3: {
                "prefix": ["By the old gods and the new! ", "For glory and honor! ", "In the name of the kingdom! "],
                "words": {
                    "fix": "heal the wounded", 
                    "add": "craft a legendary", 
                    "update": "cast a mighty spell on", 
                    "remove": "slay the fearsome"
                }
            }
        },
        "sci-fi": {
            1: {
                "prefix": ["Scanning... ", "Processing... ", "Analyzing... "],
                "words": {"fix": "repair", "add": "synthesize", "update": "upgrade", "remove": "delete"}
            },
            2: {
                "prefix": ["Initiating sequence... ", "Life signs detected... ", "Energy levels rising... "],
                "words": {"fix": "recalibrate", "add": "generate", "update": "enhance with quantum", "remove": "terminate"}
            },
            3: {
                "prefix": ["In a galaxy far, far away... ", "Space: the final frontier... ", "The future is now... "],
                "words": {
                    "fix": "reverse the polarity of", 
                    "add": "beam in from another dimension", 
                    "update": "evolve beyond version", 
                    "remove": "send into a black hole"
                }
            }
        },
        "noir": {
            1: {
                "prefix": ["The plot thickens. ", "It was a dark night. ", "The case unfolds. "],
                "words": {"fix": "clean up", "add": "uncover", "update": "investigate", "remove": "bury"}
            },
            2: {
                "prefix": ["The rain kept falling. ", "Shadows danced on the wall. ", "A whisper in the dark. "],
                "words": {"fix": "straighten out", "add": "bring to light", "update": "crack the case on", "remove": "make disappear"}
            },
            3: {
                "prefix": ["The city sleeps, but I don't. ", "Trouble's my business. ", "She walked in, code in her hand. "],
                "words": {
                    "fix": "solve the mystery of", 
                    "add": "reveal the secrets of", 
                    "update": "follow the trail of", 
                    "remove": "watch vanish into the night"
                }
            }
        },
        "western": {
            1: {
                "prefix": ["Howdy! ", "Yee-haw! ", "Giddyup! "],
                "words": {"fix": "patch up", "add": "rustle up", "update": "rework", "remove": "clear out"}
            },
            2: {
                "prefix": ["This town ain't big enough... ", "Draw, partner! ", "Saddle up, folks! "],
                "words": {"fix": "wrangle", "add": "round up", "update": "polish like new", "remove": "run outta town"}
            },
            3: {
                "prefix": ["In the wild, wild West... ", "There's a new sheriff in town... ", "Fastest code in the West... "],
                "words": {
                    "fix": "ride into town and fix", 
                    "add": "stake a claim on", 
                    "update": "transform faster than a tumbleweed", 
                    "remove": "send riding off into the sunset"
                }
            }
        }
    }
    
    # Get style template or default to pirate
    selected_style = style_templates.get(style.lower(), style_templates["pirate"])
    strength_level = selected_style.get(strength, selected_style[1])
    
    # Select a random prefix from the chosen style and strength
    prefix = random.choice(strength_level["prefix"])
    
    # Create base message for transformation
    styled_message = message.lower()
    
    # Replace common action words with style-specific versions
    for action, replacement in strength_level["words"].items():
        if action in styled_message:
            styled_message = styled_message.replace(action, replacement)
    
    # Apply style to final message
    final_message = prefix + styled_message[0].upper() + styled_message[1:]
    
    return final_message