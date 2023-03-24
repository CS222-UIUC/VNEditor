"""
----------------------------
The Best Visual Novel Engine
        Yui Engine
----------------------------

contain all basic information to build a visual novel
"""
import os
import pickle
import time

from module.exception import EngineError
from module.config_manager import ConfigLoader
from utils.file_utils import check_file_valid, check_folder_valid, get_files_in_folder
from utils.args_utils import Args, STATUS

from .action import Action
from .music import MusicSignal
from .music import Music
from .background import Background
from .character import Character, CharacterPosition
from .dialogue import Dialogue
from .frame import Frame

VERSION = "1.0.0"
RELEASE_DATE = "22/2/2023"
DEFAULT_GAME_FILE_NAME = "GameFile.vne"


def abs_dir(project_dir: str, relevant_dir: str):
    """
    get absolute directory from project/relevant directory

    @param project_dir: project directory
    @param relevant_dir: relevant directory
    @return: absolute directory
    """
    return os.path.join(project_dir, relevant_dir)


def engine_exception_handler(func):
    """
    exception decorator for engine

    @param func: function to be decorated
    @return:
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e_msg:
            print("Engine Error: ", str(e_msg))
            return STATUS.FAIL

    return wrapper


def print_fail(do_what: str):
    """
    print fail message

    @param do_what: fail describe
    @return:
    """
    print(f"(Engine) FAIL -- {do_what}")


class Engine:
    """
    Engine main class, used to edit frame in project
    """

    # metadata for the game file, update automatically
    # through calling update_metadata() function
    __metadata: dict = {}

    # activated variables, initialized after class construct,
    # should be UPDATED ON TIME every time they changed

    __game_content: dict[int, Frame] = {}
    __head: int = -1  # the head of the frame list
    __tail: int = -1  # the tail of the frame list
    __last_fid: int = -1  # the last used fid (frame id)
    __all_fids: set[int] = set()  # all fids in list

    def __init__(
        self,
        project_dir: str,
        config_dir: str,
        game_file_name: str = DEFAULT_GAME_FILE_NAME,
    ):
        """
        constructor for engine

        @param project_dir: project directory
        @param config_dir: config file directory
        @param game_file_name: game file name (not directory)
        @return:
        """
        if not check_folder_valid(project_dir):
            raise EngineError(f"project {project_dir} not exist")

        # self.__project_dir = project_dir
        self.__config = ConfigLoader(config_dir=config_dir)

        self.__bg_base_dir = abs_dir(
            project_dir, self.__config.resources()["background_dir"]
        )
        self.__music_base_dir = abs_dir(
            project_dir, self.__config.resources()["music_dir"]
        )
        self.__chara_base_dir = abs_dir(
            project_dir, self.__config.resources()["character_dir"]
        )
        self.__game_file_dir = abs_dir(project_dir, game_file_name)

        if check_file_valid(self.__game_file_dir):
            with open(self.__game_file_dir, "r", encoding="UTF-8") as file_stream:
                game_content_raw = pickle.load(file_stream)
            self.__metadata = game_content_raw[0]
            self.__game_content = game_content_raw[1]
            self.__last_fid = self.__metadata["last_fid"]
            self.__head = self.__metadata["head"]
            self.__tail = self.__metadata["tail"]
            self.__all_fids = set(self.__game_content.keys())
            self.__update_metadata()

    @engine_exception_handler
    def __update_metadata(self):
        """
        update the metadata by global variable

        @return:
        """
        self.__metadata["engine_version"] = VERSION
        self.__metadata["update_at"] = time.time()
        self.__metadata["total_frame_len"] = len(self.__game_content.keys())
        self.__metadata["last_fid"] = self.__last_fid
        self.__metadata["head"] = self.__head
        self.__metadata["tail"] = self.__tail

    @engine_exception_handler
    def append_frame(
        self,
        bg_res: str,
        chara_res: str,
        chara_position: CharacterPosition,
        music_status: MusicSignal,
        dialogue: str,
        dialogue_character: str = Args.OPTIONAL,
        music_res: str = Args.OPTIONAL,
    ):
        """
        add frame to the end of the frame list

        @param bg_res: background resources name (not directory)
        @param chara_res: character resources name (not directory)
        @param chara_position: character position
        @param dialogue: dialogue content
        @param dialogue_character: dialogue from which character,
        should be character resources name, if leave none, dialogue from VO

        @param music_res: music resources name, signal cannot be PLAY when this item leave none
        @param music_status: music play status for current frame
        @return: added frame id
        """

        # check if input resources valid or not
        if not check_file_valid(abs_dir(self.__bg_base_dir, bg_res)):
            raise EngineError(f"Background resource {bg_res} cannot find")

        if not check_file_valid(abs_dir(self.__chara_base_dir, chara_res)):
            raise EngineError(f"Character resource {chara_res} cannot find")

        if not check_file_valid(abs_dir(self.__music_base_dir, music_res)):
            raise EngineError(f"Music resource {bg_res} cannot find")

        if music_status == MusicSignal.PLAY and not check_file_valid(
            abs_dir(self.__music_base_dir, music_res)
        ):
            raise EngineError(f"Music resources {music_res} cannot find")

        if (
            dialogue_character != Args.OPTIONAL
            and dialogue_character not in get_files_in_folder(self.__chara_base_dir)
        ):
            raise EngineError(f"Character {dialogue_character} cannot find")

        # make the component
        fid = self.__last_fid + 1
        background = Background(res_name=bg_res)
        character = Character(res_name=chara_res, position=chara_position)
        music = Music(res_name=music_res, signal=music_status)

        if dialogue_character == Args.OPTIONAL:
            dialogue_chara = Character()
        else:
            dialogue_chara = Character(res_name=dialogue_character)

        dialogue = Dialogue(dialogue=dialogue, character=dialogue_chara)
        action = Action(next_f_id=Action.LAST_FRAME, prev_f_id=self.__tail)

        frame = Frame(
            fid=fid,
            background=background,
            chara=character,
            music=music,
            dialog=dialogue,
            action=action,
        )

        # change the current last frame next frame pointer
        if self.__last_fid != -1:
            self.__game_content[self.__last_fid].action.change_next_f(next_f_id=fid)

        # update activated variables
        self.__game_content[fid] = frame
        self.__last_fid = fid
        self.__all_fids.add(fid)

        # update head and tail
        if self.__head == -1:
            self.__head = fid

        self.__tail = fid

        return fid

    @engine_exception_handler
    def move_frame(self, distinct_frame_id: int, from_frame_id: int) -> STATUS:
        """
        move the from_frame to the next of the distinct_frame

        @param distinct_frame_id: distinct frame id
        @param from_frame_id: from which frame
        @return: status of the action
        """
        if distinct_frame_id in self.__all_fids and from_frame_id in self.__all_fids:
            print_fail("frame not exist")
            return STATUS.FAIL

        from_frame = self.__game_content[from_frame_id]
        dist_frame = self.__game_content[distinct_frame_id]

        self.__game_content[dist_frame.action.next_f].action.change_prev_f(
            from_frame_id
        )
        self.__game_content[from_frame.action.prev_f].action.change_next_f(
            from_frame.action.next_f
        )
        if self.__tail == from_frame_id:
            self.__tail = from_frame.action.prev_f

        from_frame.action.change_prev_f(distinct_frame_id)
        from_frame.action.change_next_f(dist_frame.action.next_f)
        dist_frame.action.change_next_f(from_frame_id)
        return STATUS.OK

    def commit(self) -> bool:
        """
        commit all the change to the local game file

        @return: commit status
        """
        self.__update_metadata()
        game_content_raw = [self.__metadata, self.__game_content]
        try:
            with open(self.__game_file_dir, "w", encoding="UTF-8") as file_stream:
                pickle.dump(game_content_raw, file_stream)
        except Exception as e_msg:
            print_fail("fail to commit due to: " + str(e_msg))
            return False
        return True
