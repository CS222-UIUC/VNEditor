"""
dialogue component for frame
"""

from .character import Character


class Dialogue:
    """
    dialogue component in frame
    """

    def __init__(self, dialogue: str, character: Character = Character.VO):
        """
        constructor for character

        @param dialogue: dialogue text
        @param character: who speak it
        """
        self.dialogue = dialogue
        self.character = character

    def get_dialogue(self):
        """
        getter for dialogue

        @return:
        """
        return self.dialogue, self.character

    def set_dialogue(self, dialogue: str, character: Character = Character.VO):
        """
        setter for dialogue

        @param dialogue: new dialogue
        @param character: new character binding
        @return:
        """
        self.dialogue = dialogue
        self.character = character
