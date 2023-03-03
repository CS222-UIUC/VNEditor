from enum import Enum
from utils.args_utils import Args

DEFAULT = Args.DEFAULT


class MusicSignal(Enum):
    """
    enumerate define for music signal, for PLAY, it has to come with a music resource to be played
    """

    Keep = 1
    Pause = 2
    Next = 3
    PLAY = 4


class Music:
    def __init__(self, res_name: str = DEFAULT, signal: MusicSignal = MusicSignal.Keep):
        """
        constructor for Music, for PLAY signal, it must specify a resources to be played

        @param res_name: the name for music resources
        @param signal: signal for current frame music
        """
        self.res_name: str = res_name
        self.signal: MusicSignal = signal
