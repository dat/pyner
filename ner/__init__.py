#!/usr/bin/env python

"""Python wrapper for the Stanford NER.
@author Dat Hoang
@date March 2011"""


from .client import (
    SocketNER,
    HttpNER,
)

from .exceptions import (
    NERError,
)


__version__ = '0.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = [
    'SocketNER',
    'HttpNER',
    'NERError',
]
