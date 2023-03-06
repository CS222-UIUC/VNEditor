"""
define of special arguments
"""
from enum import Enum


class Args(Enum):
    """
    general argument define
    """

    DEFAULT = 1
    OPTIONAL = 2
    NONE = 3


class STATUS(Enum):
    """
    status code for the engine class
    """

    FAIL = 0
    OK = 1
