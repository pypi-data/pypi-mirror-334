"""
A simple text wrapping tool
"""

# Supports only in Python 3.8+

from .txtwrap import (
    version,
    LOREM_IPSUM_W, LOREM_IPSUM_S, LOREM_IPSUM_P,
    mono, word, wrap, align, fillstr, printwrap,
    shorten
)

__version__ = version
__author__ = 'azzammuhyala'
__license__ = 'MIT'
__all__ = [
    'LOREM_IPSUM_W',
    'LOREM_IPSUM_S',
    'LOREM_IPSUM_P',
    'mono',
    'word',
    'wrap',
    'align',
    'fillstr',
    'printwrap',
    'shorten'
]