from Background import Background
from Branch import BranchTree
from Character import Character
from Dialogue import Dialogue
from Music import Music
from Action import Action


class Frame:
    """
    Frame
    """

    def __init__(
        self,
        fid: int,
        bg: Background,
        chara: Character,
        music: Music,
        dialog: Dialogue,
        action: Action,
    ):
        self.bg = bg
        self.chara = chara
        self.music = music
        self.dialog = dialog
        self.action = action
        self.fid = fid

    def set_id(self, id: int):
        self.fid = id

    def get_id(self):
        return self.fid
