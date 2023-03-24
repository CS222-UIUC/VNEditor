import os
from engine.frame import BasicFrame, Frame
from typing import Optional
from engine.component.music import MusicSignal
from utils.file_utils import check_file_valid, abs_dir
from module.config_manager import ConfigLoader


class FrameChecker:
    def __init__(self, project_dir: str, config: ConfigLoader):
        self.__project_dir = project_dir
        self.__bg_base_dir = os.path.join(self.__project_dir, config.resources()["background_dir"])
        self.__music_base_dir = os.path.join(self.__project_dir, config.resources()["music_dir"])
        self.__chara_base_dir = os.path.join(self.__project_dir, config.resources()["character_dir"])

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
            return [False, f"Background resource {bg_res} cannot find"]

        for character in frame.chara:
            chara_res = character.res_name
            if chara_res is not None:
                if not check_file_valid(abs_dir(self.__chara_base_dir, chara_res)):
                    return [False, f"Character resource {chara_res} cannot find"]

        if music_res is not None:
            if not check_file_valid(abs_dir(self.__music_base_dir, music_res)):
                return [False, f"Music resource {bg_res} cannot find"]

        if music_res and music_status == MusicSignal.PLAY:
            if not check_file_valid(abs_dir(self.__music_base_dir, music_res)):
                return [False, f"Music resources {music_res} cannot find"]

        if dialogue_character is not None:
            if not check_file_valid(
                abs_dir(self.__chara_base_dir, dialogue_character.res_name)
            ):
                return [False, f"Character resource {dialogue_character.res_name} cannot find"]

        return [True, None]
