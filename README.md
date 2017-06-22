# Code faster

Dactylo test are based on words or sentences but never on code. A programmer spends its time to type symbols. 
Code faster is a dactlylo test using your own code.

# Usage

`python3 ./codefaster.py base_directory`

# Misc

Codefaster doesn't need any additional library to work. But you can install `termcolor` to have a colored output.

# Config

```python

# The extension of the files to search.
FILE_EXT = ['py', 'c', 'css', 'cpp', 'h', 'hpp', 'hs', 'js', 'jsx', 'html',
            'ts']

# Logging Level, use the 'logging module' constants0
LOGGING_LEVEL = DEBUG

# Test duration. 
TIMEOUT = 60  # in seconds

# List of pattern you want to ignore.
# Here, line that contains """ (usually docstring) are ignored.
LINE_IGNORE_PATTERNS = [r'"""']
```
