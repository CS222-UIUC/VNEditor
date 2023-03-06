"""
frame component for frame
"""

from .background import Background
from .character import Character
from .dialogue import Dialogue
from .music import Music
from .action import Action


class Frame:
    """
    Frame
    """

    def __init__(
        self,
        fid: int,
        background: Background,
        chara: Character,
        music: Music,
        dialog: Dialogue,
        action: Action,
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
        self.background = background
        self.chara = chara
        self.music = music
        self.dialog = dialog
        self.action = action
        self.fid = fid

    def set_id(self, fid: int) -> None:
        """
        set frame id for current frame

        @param fid: new fid
        @return:
        """
        self.fid = fid

    def get_id(self) -> int:
        """
        get the id for current frame

        @return: frame id
        """
        return self.fid
