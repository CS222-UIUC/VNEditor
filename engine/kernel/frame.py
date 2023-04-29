"""
frame component for frame
"""
import os
from typing import Optional
from pydantic import BaseModel

from module.config_module import ConfigLoader

from kernel.component.background import Background
from kernel.component.character import Character
from kernel.component.dialogue import Dialogue
from kernel.component.music import Music, MusicSignal
from kernel.component.action import Action
from kernel.component.meta import FrameMeta
from kernel.component.image import ImageModel

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
    """
    contain the frame information, include fid and meta

    """

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
        character: list[Character],
        music: Music,
        dialog: Dialogue,
        meta: FrameMeta,
        action: Optional[Action] = None,
    ):
        """
        constructor for frame class

        @param fid: frame id, should be unique
        @param background: background
        @param character: character
        @param music: music
        @param dialog: dialogue
        @param meta: frame metadata
        @param action: action

        """
        super().__init__(fid, action)
        self.meta = meta
        self.background: Background = background
        self.character: list[Character] = character
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

        if music_res is None and music_status == MusicSignal.PLAY:
            return [False, "music resources have to specified when status set to play"]

        # check if input resources valid or not
        if not check_file_valid(abs_dir(self.__bg_base_dir, bg_res)):
            return [False, f"Background resource '{bg_res}' cannot find"]

        for character in frame.character:
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
    background_attr: ImageModel
    character: dict[str, ImageModel]
    music: Optional[str]
    music_signal: MusicSignal
    dialog: str
    dialog_character: Optional[str]
    name: str

    def to_frame(self) -> Frame:
        """
        convert the frame model to frame instance

        @return: frame instance

        """
        background = Background(res_name=self.background, **self.background_attr.dict())
        chara = []
        dialogue = Dialogue(
            dialogue=self.dialog, character=Character(self.dialog_character)
        )
        for chara_res, chara_attr in self.character.items():
            chara.append(Character(res_name=chara_res, **chara_attr.dict()))
        music = Music(res_name=self.music, signal=self.music_signal)
        meta = FrameMeta(self.name)
        return Frame(
            fid=BasicFrame.VOID_FRAME_ID,
            background=background,
            character=chara,
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
    background_attr = ImageModel(**frame.background.__dict__)

    chara = {}
    for cur_chara in frame.character:
        cur_chara_attr = ImageModel(**frame.background.__dict__)
        chara[cur_chara.res_name] = cur_chara_attr

    music_signal = frame.music.signal
    music = frame.music.res_name
    dialog = frame.dialog.dialogue
    name = frame.meta.name

    if frame.dialog.character is None:
        dialog_character = None
    else:
        dialog_character = frame.dialog.character.res_name

    return FrameModel(
        background=background,
        background_attr=background_attr,
        character=chara,
        music=music,
        music_signal=music_signal,
        dialog=dialog,
        dialog_character=dialog_character,
        name=name,
    )


def make_empty_frame(frame_name: str):
    """
    make an empty frame

    @return: empty frame

    """
    frame = Frame(
        Frame.VOID_FRAME_ID,
        Background(""),
        [],
        Music(),
        Dialogue(""),
        FrameMeta(name=frame_name),
    )
    return frame


def make_frame(
    background: Background,
    character: list[Character],
    music: Music,
    dialog: Dialogue,
    meta: FrameMeta,
    **kwargs,
) -> Frame:
    """
    make a frame

    @param background: background
    @param character: character
    @param music: music
    @param dialog: dialog
    @param meta the metadata for the frame
    @return: result frame

    """
    frame = Frame(
        fid=BasicFrame.VOID_FRAME_ID,
        background=background,
        character=character,
        music=music,
        dialog=dialog,
        meta=meta,
    )
    return frame
