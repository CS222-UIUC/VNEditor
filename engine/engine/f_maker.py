from engine.component.background import Background
from engine.component.character import Character
from engine.component.dialogue import Dialogue
from engine.component.music import Music
from engine.frame import Frame


class FrameMaker:
    def make(self, _type: type, **kwargs) -> Frame | None:
        """
        entry for frame check, register your own checker there,
        initialize frame id and action with VOID_FRAME_ID and
        VOID_FRAME_ID because they will be rewritten by engine

        @param _type: which type of frame to be added
        @return: status

        """
<<<<<<< HEAD
        if type(_type) == type(Frame):
=======
        if self.__is_type(_type, Frame):
>>>>>>> 70dad1d15cfc57f95f402403263021528a40be31
            return self.__make_frame(**kwargs)
        else:
            return None

    @staticmethod
<<<<<<< HEAD
=======
    def __is_type(type1: type, type2: type):
        return type(type1) == type(type2)

    @staticmethod
>>>>>>> 70dad1d15cfc57f95f402403263021528a40be31
    def __make_frame(
            background: Background,
            chara: list[Character],
            music: Music,
            dialog: Dialogue,
    ):
<<<<<<< HEAD

        return Frame(Frame.VOID_FRAME_ID, background, chara, music, dialog, Frame.VOID_ACTION)
=======
        return Frame(
            Frame.VOID_FRAME_ID, background, chara, music, dialog
        )
>>>>>>> 70dad1d15cfc57f95f402403263021528a40be31
