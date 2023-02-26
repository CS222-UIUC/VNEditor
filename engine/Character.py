from enum import Enum


class CharacterPosition(Enum):
    L2 = 1
    L1 = 2
    M = 3
    R1 = 4
    R2 = 5


class Character:
    def __init__(self, res_name: str, position: CharacterPosition):
        """
        constructor for character

        :param res_name: character file name
        :param position: choose from 1, 2, 3, 4, the character position on stage
        """
        self.res_name = res_name
        self.position = position
