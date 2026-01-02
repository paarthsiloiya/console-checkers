import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Console Checkers'
copyright = '2024, Console Checkers Team'
author = 'Console Checkers Team'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'shibuya'
html_static_path = ['_static']
