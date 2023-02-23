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

VERSION = '1.0.0'
RELEASE_DATE = '22/2/2023'
DEFAULT_GAME_FILE_NAME = 'GameFile.vne'


def abs_dir(project_dir: str, relevant_dir: str):
    return os.path.join(project_dir, relevant_dir)


class Engine:
    cur_frame_id = -1
    game_content = None

    def __int__(self, project_dir: str, config_dir: str, game_file_name: str = DEFAULT_GAME_FILE_NAME):

        if not check_folder_valid(project_dir):
            raise EngineError("project {} not exist".format(project_dir))

        self.project_dir = project_dir
        self.config = Loader(config_dir=config_dir)

        self.bg_base_dir = abs_dir(project_dir, self.config.resources()['background_dir'])
        self.music_base_dir = abs_dir(project_dir, self.config.resources()['music_dir'])
        self.chara_base_dir = abs_dir(project_dir, self.config.resources()['character_dir'])
        self.game_file_dir = abs_dir(project_dir, game_file_name)

        if check_file_valid(self.game_file_dir):
            with open(self.game_file_dir, 'r') as fo:
                self.game_content = pickle.load(fo)

    def add_frame(self, bg_res: str, chara_res: str, music_res: str = None, music_status: int = 0):
        """
        add frame to game file
        :param bg_res:
        :param chara_res:
        :param music_res:
        :param music_status:
        :return: status of the action
        """
        if not check_file_valid(abs_dir(self.bg_base_dir, bg_res)):
            raise EngineError("Background resource {} cannot find".format(bg_res))

        if not check_file_valid(abs_dir(self.chara_base_dir, chara_res)):
            raise EngineError("Character resource {} cannot find".format(chara_res))

        if not check_file_valid(abs_dir(self.music_base_dir, bg_res)):
            raise EngineError("Music resource {} cannot find".format(bg_res))

    def commit(self) -> bool:
        """
        commit all the change to the local game file

        :return: commit status
        """
        try:
            with open(self.game_file_dir, 'w') as fo:
                pickle.dump(self.game_content, fo)
        except Exception as e:
            print("cannot commit: ", str(e))
            return False
        return True
