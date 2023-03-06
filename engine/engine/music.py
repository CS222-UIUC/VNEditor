"""
music component for frame
"""

from enum import Enum
from utils.args_utils import Args

DEFAULT = Args.DEFAULT


class MusicSignal(Enum):
    """
    enumerate define for music signal, for PLAY, it has to come with a music resource to be played
    """

    KEEP = 1
    PAUSE = 2
    NEXT = 3
    PLAY = 4


class Music:
    """
    music component in frame
    """

    def __init__(self, res_name: str = DEFAULT, signal: MusicSignal = MusicSignal.KEEP):
        """
        constructor for Music, for PLAY signal, it must specify a resources to be played

        @param res_name: the name for music resources
        @param signal: signal for current frame music
        """
        self.res_name: str = res_name
        self.signal: MusicSignal = signal

    def set_music(
        self, res_name: str = DEFAULT, signal: MusicSignal = MusicSignal.KEEP
    ):
        """
        setter for music resources

        @param res_name: the name for music resources
        @param signal: signal for current frame music
        @return:
        """
        self.res_name: str = res_name
        self.signal: MusicSignal = signal

    def get_music(self):
        """
        getter for music resources

        @return: music resources name, signal
        """
        return self.res_name, self.signal
