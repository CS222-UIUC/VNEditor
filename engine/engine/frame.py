"""
frame component for frame
"""

from typing import Optional
from engine.component.background import Background
from engine.component.character import Character
from engine.component.dialogue import Dialogue
from engine.component.music import Music
from engine.component.action import Action


class BasicFrame:
    """
    base modal for frame
    """
    VOID_FRAME_ID = -1  # indicate no frame

    def __init__(self, fid: int, action: Optional[Action] = None):
        self.fid: int = fid

        if action is None:
            action = Action(self.VOID_FRAME_ID, self.VOID_FRAME_ID)
        self.action = action


class Frame(BasicFrame):
    """
    a normal frame
    """

    def __init__(
            self,
            fid: int,
            background: Background,
            chara: list[Character],
            music: Music,
            dialog: Dialogue,
            action: Optional[Action] = None,
    ):
        """
        constructor for frame class

        @param fid: frame id, should be unique
        @param background: background
        @param chara: character
        @param music: music
        @param dialog: dialogue
        @param action: action
        """
        super().__init__(fid, action)
        self.background: Background = background
        self.chara: list[Character] = chara
        self.music: Music = music
        self.dialog: Dialogue = dialog
