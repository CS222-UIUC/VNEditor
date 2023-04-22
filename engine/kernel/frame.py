"""
frame component for frame
"""
import os
from typing import Optional
from pydantic import BaseModel

from module.config_manager import ConfigLoader

from kernel.component.background import Background
from kernel.component.character import (
    Character,
    CharacterPosition,
    CharacterPositionModal,
)
from kernel.component.dialogue import Dialogue
from kernel.component.music import Music, MusicSignal
from kernel.component.action import Action
from kernel.component.meta import FrameMeta

from utils.file_utils import check_file_valid, abs_dir


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


class FrameInfo:
    def __init__(self, fid: int, meta: FrameMeta):
        self.fid: int = fid
        self.meta: FrameMeta = meta


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
            meta: FrameMeta,
            action: Optional[Action] = None,
    ):
        """
        constructor for frame class

        @param fid: frame id, should be unique
        @param background: background
        @param chara: character
        @param music: music
        @param dialog: dialogue
        @param meta: frame metadata
        @param action: action

        """
        super().__init__(fid, action)
        self.meta = meta
        self.background: Background = background
        self.chara: list[Character] = chara
        self.music: Music = music
        self.dialog: Dialogue = dialog


class FrameChecker:
    """
    frame checker class

    """

    def __init__(self, project_dir: str, config: ConfigLoader):
        self.__project_dir = project_dir
        self.__bg_base_dir = os.path.join(
            self.__project_dir, config.resources()["background_dir"]
        )
        self.__music_base_dir = os.path.join(
            self.__project_dir, config.resources()["music_dir"]
        )
        self.__chara_base_dir = os.path.join(
            self.__project_dir, config.resources()["character_dir"]
        )

    def check(self, frame: BasicFrame) -> list[bool, Optional[str]]:
        """
        entry for frame check, register your own checker there

        @param frame: frame to be checked
        @return: status

        """
        if isinstance(frame, Frame):
            return self.__check_frame(frame)

        # add your own checker here !

        return [False, None]

    def __check_frame(self, frame: Frame) -> list[bool, Optional[str]]:
        """
        Frame Checker

        @param frame: frame to check
        @return: status

        """
        bg_res = frame.background.res_name
        music_res = frame.music.res_name
        music_status = frame.music.signal
        dialogue_character = frame.dialog.character

        # check if contain conflict in input
        for character in frame.chara:
            chara_position = character.position
            chara_res = character.res_name

            if chara_position is not None and chara_res is None:
                return [
                    False,
                    "character position cannot be defined is not given character",
                ]

        if music_res is None and music_status == MusicSignal.PLAY:
            return [False, "music resources have to specified when status set to play"]

        # check if input resources valid or not
        if not check_file_valid(abs_dir(self.__bg_base_dir, bg_res)):
            return [False, f"Background resource '{bg_res}' cannot find"]

        for character in frame.chara:
            chara_res = character.res_name
            if chara_res is not None:
                if not check_file_valid(abs_dir(self.__chara_base_dir, chara_res)):
                    return [False, f"Character resource '{chara_res}' cannot find"]

        if music_res is not None:
            if not check_file_valid(abs_dir(self.__music_base_dir, music_res)):
                return [False, f"Music resource '{bg_res}' cannot find"]

        if music_res and music_status == MusicSignal.PLAY:
            if not check_file_valid(abs_dir(self.__music_base_dir, music_res)):
                return [False, f"Music resources '{music_res}' cannot find"]

        if dialogue_character is not None:
            if not check_file_valid(
                    abs_dir(self.__chara_base_dir, dialogue_character.res_name)
            ):
                return [
                    False,
                    f"Character resource {dialogue_character.res_name} cannot find",
                ]

        return [True, None]


class FrameModel(BaseModel):
    """
    class for frame model

    """

    background: str
    chara: list
    chara_pos: list[CharacterPositionModal]
    music: str
    music_signal: MusicSignal
    dialog: str
    dialog_character: str
    name: str

    def to_frame(self) -> Frame:
        """
        convert the frame model to frame instance

        @return: frame instance

        """
        background = Background(res_name=self.background)
        chara = []
        dialogue = Dialogue(
            dialogue=self.dialog, character=Character(self.dialog_character)
        )
        for idx, cur in enumerate(self.chara):
            chara.append(
                Character(
                    res_name=cur,
                    position=CharacterPosition(
                        self.chara_pos[idx].x, self.chara_pos[idx].y
                    ),
                )
            )
        music = Music(res_name=self.music, signal=self.music_signal)
        meta = FrameMeta(self.name)
        return Frame(
            fid=BasicFrame.VOID_FRAME_ID,
            background=background,
            chara=chara,
            dialog=dialogue,
            music=music,
            meta=meta,
        )


def frame_to_model(frame: Frame):
    """
    convert frame to frame model

    @param frame: the frame to be convert
    @return: frame model instance

    """
    background = frame.background.res_name
    chara = [i.res_name for i in frame.chara]
    chara_pos = []
    for cur_chara in frame.chara:
        cur_chara_position_modal = CharacterPositionModal()
        cur_chara_position_modal.x = cur_chara.position.x
        cur_chara_position_modal.y = cur_chara.position.y
        chara_pos.append(cur_chara_position_modal)
    music_signal = frame.music.signal
    music = frame.music.res_name
    dialog = frame.dialog.dialogue
    name = frame.meta.name

    if frame.dialog.character is None:
        dialog_character = None
    else:
        dialog_character = frame.dialog.character.res_name

    if background is None:
        background = ""
    if music is None:
        music = ""
    if dialog is None:
        dialog = ""
    if dialog_character is None:
        dialog_character = ""
    return FrameModel(
        background=background,
        chara=chara,
        chara_pos=chara_pos,
        music=music,
        music_signal=music_signal,
        dialog=dialog,
        dialog_character=dialog_character,
        name=name,
    )
