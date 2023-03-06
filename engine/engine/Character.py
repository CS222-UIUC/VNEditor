"""
character component for frame
"""

from enum import Enum
from utils.args_utils import Args


class CharacterPosition(Enum):
    """
    Enumerate define character position:
    L2: most left
    L1: left
    M: middle
    R1: right
    R2: most right
    """

    L2 = 1
    L1 = 2
    M = 3
    R1 = 4
    R2 = 5


class Character:
    """
    character component in frame

    """

    VO = Args.DEFAULT  # voice over option

    def __init__(self, res_name: str = VO, position: CharacterPosition = Args.OPTIONAL):
        """
        constructor for character

        @param res_name: character file name, if leave none, default is voice over
        @param position: choose from 1, 2, 3, 4, the character position on stage
        """
        self.res_name: str = res_name
        self.position: CharacterPosition = position

    def get_character(self) -> str:
        """
        getter for character resources

        @return:
        """
        return self.res_name

    def set_character(self, res_name: str, position: CharacterPosition = Args.OPTIONAL):
        """
        setter for character
        @param res_name: new resources name
        @param position: new position for this character
        @return:
        """
        self.res_name = res_name
        self.position = position
