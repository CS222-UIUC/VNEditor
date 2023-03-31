"""
dialogue component for frame
"""

from typing import Optional
from .character import Character


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

        @return: dialogue string and character
        """
        return self.dialogue, self.character

    def set_dialogue(self, dialogue: str, character: Optional[Character] = None):
        """
        setter for dialogue

        @param dialogue: new dialogue
        @param character: new character binding
        @return:
        """
        self.dialogue = dialogue
        self.character = character
