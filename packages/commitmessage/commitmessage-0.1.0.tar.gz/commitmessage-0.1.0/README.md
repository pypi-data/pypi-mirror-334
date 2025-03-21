# Python Package Exercise

## Team loaded-package

### Members
* [Brian Zou](https://github.com/brianzou03)
* [Johnny Ding](https://github.com/yd2960)
* [Cyryl Zhang](https://github.com/nstraightbeam)
* [Josh Lavroff](https://github.com/joshlavroff)

### Product Vision Statement

CommitMessageGenerator is a fun Python package to generate creative, funny, or themed git commit messages!

### User Stories
1. As a developer, I want to add relevant emojis to my commit messages so that the type of change is immediately visible.
2. As a team lead, I want to style our commit messages in a fun theme (like pirate or superhero) to make our repository activity more engaging.
3. As a project manager, I want commit messages to be more descriptive and creative so that our changelog is more interesting to read.
4. As a developer working on multiple projects, I want to easily transform ordinary commit messages into memorable ones without spending time thinking of creative text.
5. As a new team member, I want to quickly understand what kind of changes a commit contains through visual cues like emojis.
6. As a developer giving a presentation, I want to show an entertaining git log that will engage my audience.
7. As an open source contributor, I want to create dramatic commit messages to highlight the importance of my contributions.

### Development environment setup

Create Virtual environment and activate
```
python3 -m venv venv
source venv/bin/activate
```

Install pipenv
```
pip install pipenv
```

Install and run unit tests
```
pipenv install pytest
pytest
```

### PyPi Package

Clean setup twine

```
pip install --upgrade pip setuptools wheel twine build
rm -rf dist/ build/ *.egg-info
```

Build and publish to PyPi
```
pip install --upgrade build
python -m build

pipenv install build twine
pipenv run python -m build
pipenv run twine upload dist/*
```

### Link to PyPI website


### How to run
```
pip install commitmessage
```

### Package contents


#### drama.py
This function dramatizes commit messages by adding exaggerated excitement based on the type of commit (feature, fix, docs, refactor, test) and an intensity level (1-3).
Higher intensity levels make the messages louder and more enthusiastic.


#### emoji.py
Enhances commit messages by adding relevant emojis based on the commit category.
The intensity parameter determines how many emojis are added.
Covers a broad range of categories, including feature, fix, docs, refactor, test, style, chore, and more.


#### haiku.py
Transforms commit messages into haikus.
Uses a theme (nature, tech, or emotion) to generate a poetic commit message.
Optionally incorporates filenames that were changed.


#### style.py
Converts commit messages into fun, thematic styles such as pirate, superhero, medieval, sci-fi, noir, and western.
Uses a strength parameter (1-3) to determine the intensity of the transformation.
Replaces key words in the message with thematic equivalents and adds an appropriate prefix.


### Unit testing
Each unit test file corresponds to an individual file.
* test_drama.py -> drama.py
* test_emoji.py -> emoji.py
* test_haiku.py -> haiku.py
* test_style.py -> style.py


### Environment variables
We don't have any exclusive environment variables for this project
Nor do we have a .env file