"""
dialogue component for frame
"""

from .character import Character
from typing import Optional


class Dialogue:
    """
    dialogue component in frame
    """

    def __init__(self, dialogue: str, character: Optional[Character] = None):
        """
        constructor for character

        @param dialogue: dialogue text
        @param character: who speak it
        """
        self.dialogue: str = dialogue
        self.character: Character = character

    def get_dialogue(self):
        """
        getter for dialogue

        @return:
        """
        return self.dialogue, self.character

    def set_dialogue(self, dialogue: str, character: Character = Optional[Character]):
        """
        setter for dialogue

        @param dialogue: new dialogue
        @param character: new character binding
        @return:
        """
        self.dialogue = dialogue
        self.character = character
