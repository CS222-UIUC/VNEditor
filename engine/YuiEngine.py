from Frame import Frame
from Background import Background
from Character import Character
from Dialogue import Dialogue
from Music import Music
from module.Exception import *
from module.ConfigManager import Loader
from utils.file_utils import *
import os
import pickle
from Music import MusicSignal
from Background import Background
from Character import Character, CharacterPosition
from Dialogue import Dialogue
from utils.args_utils import Args
from Action import Action
import time


VERSION = "1.0.0"
RELEASE_DATE = "22/2/2023"
DEFAULT_GAME_FILE_NAME = "GameFile.vne"


def abs_dir(project_dir: str, relevant_dir: str):
    return os.path.join(project_dir, relevant_dir)


class Engine:
    __metadata: dict = {}

    __game_content: dict = {}  # update on time
    __last_id = 0  # update on time

    def __int__(
        self,
        project_dir: str,
        config_dir: str,
        game_file_name: str = DEFAULT_GAME_FILE_NAME,
    ):
        if not check_folder_valid(project_dir):
            raise EngineError("project {} not exist".format(project_dir))

        self.project_dir = project_dir
        self.config = Loader(config_dir=config_dir)

        self.bg_base_dir = abs_dir(
            project_dir, self.config.resources()["background_dir"]
        )
        self.music_base_dir = abs_dir(project_dir, self.config.resources()["music_dir"])
        self.chara_base_dir = abs_dir(
            project_dir, self.config.resources()["character_dir"]
        )
        self.game_file_dir = abs_dir(project_dir, game_file_name)

        if check_file_valid(self.game_file_dir):
            with open(self.game_file_dir, "r") as fo:
                game_content_raw = pickle.load(fo)
            self.__metadata = game_content_raw[0]
            self.__game_content = game_content_raw[1]
            self.__last_id = self.__metadata["last_id"]
            self.update_metadata()

    def update_metadata(self):
        self.__metadata["engine_version"] = VERSION
        self.__metadata["update_at"] = time.time()
        self.__metadata["total_frame_len"] = len(self.__game_content.keys())
        self.__metadata["last_id"] = self.__last_id

    def add_frame(
        self,
        bg_res: str,
        chara_res: str,
        chara_position: CharacterPosition,
        music_status: MusicSignal,
        dialogue: str,
        dialogue_character: Args.OPTIONAL,
        music_res: str = Args.OPTIONAL,
    ):
        """
        add frame to game file

        :param bg_res: background resources name
        :param chara_res: character resources name
        :param chara_position: character position
        :param dialogue: dialogue content
        :param dialogue_character: dialogue from which character, if leave none, dialogue from VO
        :param music_res: music resources name, signal cannot be PLAY when this item leave none
        :param music_status: music play status for current frame
        :return: status of the action
        """
        if not check_file_valid(abs_dir(self.bg_base_dir, bg_res)):
            raise EngineError("Background resource {} cannot find".format(bg_res))

        if not check_file_valid(abs_dir(self.chara_base_dir, chara_res)):
            raise EngineError("Character resource {} cannot find".format(chara_res))

        if not check_file_valid(abs_dir(self.music_base_dir, music_res)):
            raise EngineError("Music resource {} cannot find".format(bg_res))

        if music_status == MusicSignal.PLAY and not check_file_valid(
            abs_dir(self.music_base_dir, music_res)
        ):
            raise EngineError("Music resources {} cannot find".format(music_res))

        if dialogue_character not in get_files_in_folder(self.chara_base_dir):
            raise EngineError("Character {} cannot find".format(dialogue_character))

        background = Background(res_name=bg_res)
        character = Character(res_name=chara_res, position=chara_position)
        music = Music(res_name=music_res, signal=music_status)
        dialogue = Dialogue(dialogue=dialogue, character=dialogue_character)
        # action = Action(next_f=)
        # frame = Frame(bg=background, chara=character, music=music, dialog=dialogue, action=)

    def commit(self) -> bool:
        """
        commit all the change to the local game file

        :return: commit status
        """
        self.update_metadata()
        game_content_raw = [self.__metadata, self.__game_content]
        try:
            with open(self.game_file_dir, "w") as fo:
                pickle.dump(game_content_raw, fo)
        except Exception as e:
            print("fail to commit: ", str(e))
            return False
        return True
