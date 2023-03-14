"""
----------------------------
The Best Visual Novel Engine
        Yui Engine
----------------------------

contain all basic information to build a visual novel
"""

import time

from typing import Optional
from module.exception import EngineError
from module.config_manager import ConfigLoader
from utils.file_utils import check_file_valid, check_folder_valid, abs_dir
from utils.status import StatusCode
from engine.frame import BasicFrame
from engine.f_checker import FrameChecker
from engine.f_maker import FrameMaker
import engine.eng_io as eng_io

VERSION = "1.0.0"


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
            return StatusCode.FAIL

    return wrapper


class Engine:
    """
    Engine main class, used to edit frame in project
    """

    # metadata for the game file, update automatically
    # through calling update_metadata() function
    __metadata: dict = {}

    # activated variables, initialized after class construct,
    # should be UPDATED ON TIME every time they changed
    __game_content: dict[int, BasicFrame] = {}
    __head: int = BasicFrame.VOID_FRAME_ID  # the head of the frame list
    __tail: int = BasicFrame.VOID_FRAME_ID  # the tail of the frame list
    __last_fid: int = BasicFrame.VOID_FRAME_ID  # the last used fid (frame id)
    __all_fids: set[int] = set()  # all fids in set

    def __init__(
            self,
            project_dir: str,
            config_dir: str,
            game_file_name: Optional[str] = None,
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
        self.__engine_config = self.__config.engine()

        resource_config_raw = self.__config.resources()
        resource_config_abs = {}
        for k, v in resource_config_raw.items():
            resource_config_abs[k] = abs_dir(project_dir, v)
        self.__frame_checker = FrameChecker(
            project_dir=project_dir, config=self.__config
        )

        if not game_file_name:
            game_file_name = self.__config.engine()["default_game_file"]
        self.__game_file_dir = abs_dir(project_dir, game_file_name)
        self.__frame_maker = FrameMaker()

        loader = self.__engine_config["loader"]
        dumper = self.__engine_config["dumper"]
        if hasattr(eng_io, loader) and hasattr(eng_io, dumper):
            self.__loader = getattr(eng_io, loader)
            self.__dumper = getattr(eng_io, dumper)
        else:
            raise EngineError("initialize fail due to cannot find loader/dumper")

        if check_file_valid(self.__game_file_dir):
            try:
                game_content_raw = self.__loader(self.__game_file_dir)
            except Exception as e:
                raise EngineError(f"fail to load game file due to {str(e)}") from e
            self.__metadata = game_content_raw[0]
            self.__game_content = game_content_raw[1]
            self.__last_fid = self.__metadata["last_fid"]
            self.__head = self.__metadata["head"]
            self.__tail = self.__metadata["tail"]
            self.__all_fids = set(self.__game_content.keys())

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
    def make_frame(self, _type: type, **kwargs) -> BasicFrame:
        frame = self.__frame_maker.make(_type, **kwargs)

        if frame is None:
            raise EngineError("make frame failed")

        return frame

    def append_frame(self, frame: BasicFrame, force: bool = False) -> int:
        """
        add frame to the end of the frame list

        @param force: force push mode, ignore checking frame valid
        @param frame: frame to be added
        @return:  frame id

        """
        # check frame
        if not force:
            check_output = self.__frame_checker.check(frame)
            if not check_output[0]:
                raise EngineError(check_output[1])

        # generate the fid
        if self.__last_fid == BasicFrame.VOID_FRAME_ID:
            fid = 0
        else:
            fid = self.__last_fid + 1
        frame.fid = fid

        # change the current last frame's next frame pointer
        if self.__last_fid != BasicFrame.VOID_FRAME_ID:
            self.__game_content[self.__last_fid].action.next_f = fid

        # update activated variables
        self.__game_content[fid] = frame
        self.__last_fid = fid
        self.__all_fids.add(fid)

        # update head and tail
        if self.__head == BasicFrame.VOID_FRAME_ID:
            self.__head = fid

        self.__tail = fid

        return fid

    @engine_exception_handler
    def insert_frame(self, dest_frame_id: int, from_frame_id: int):
        """
        move the from_frame to the next of the dest_frame_id,
        if dest frame is VOID_FRAME_ID, then move to the head

        @param dest_frame_id: distinct frame id
        @param from_frame_id: from which frame

        """
        if dest_frame_id == BasicFrame.VOID_FRAME_ID:
            # edge case, add frame to the head
            from_frame = self.__game_content[from_frame_id]
            if from_frame.action.prev_f != BasicFrame.VOID_FRAME_ID:
                self.__game_content[
                    from_frame.action.prev_f
                ].action.next_f = from_frame.action.next_f
            else:
                return
            if from_frame.action.next_f != BasicFrame.VOID_FRAME_ID:
                self.__game_content[
                    from_frame.action.next_f
                ].action.prev_f = from_frame.action.prev_f
            else:
                self.__tail = from_frame.action.prev_f
            from_frame.action.next_f = self.__head
            self.__game_content[self.__head].action.prev_f = from_frame_id
            self.__head = from_frame_id
            return

        if dest_frame_id not in self.__all_fids or from_frame_id not in self.__all_fids:
            raise EngineError("insert fail, frame not exist")

        from_frame = self.__game_content[from_frame_id]
        dest_frame = self.__game_content[dest_frame_id]

        if from_frame == self.__head:
            self.__head = from_frame.action.next_f

        from_frame.action.next_f = dest_frame.action.next_f
        from_frame.action.prev_f = dest_frame_id

        if dest_frame.action.next_f != BasicFrame.VOID_FRAME_ID:
            self.__game_content[dest_frame.action.next_f].action.prev_f = from_frame
        else:
            self.__tail = from_frame_id

        dest_frame.action.next_f = from_frame

    @engine_exception_handler
    def remove_frame(self, frame_id: int):
        """
        remove the frame from game content

        @param frame_id: id of frame

        """
        if frame_id not in self.__all_fids:
            raise EngineError("remove fail, frame not exist")

        cur_frame = self.__game_content[frame_id]
        if cur_frame.action.prev_f != BasicFrame.VOID_FRAME_ID:
            self.__game_content[
                cur_frame.action.prev_f
            ].action.next_f = cur_frame.action.next_f
        else:
            self.__head = cur_frame.action.next_f

        if cur_frame.action.next_f != BasicFrame.VOID_FRAME_ID:
            self.__game_content[
                cur_frame.action.next_f
            ].action.prev_f = cur_frame.action.prev_f
        else:
            self.__tail = cur_frame.action.prev_f

        # update metadata
        self.__all_fids.remove(frame_id)

    def change_frame(self, frame_id: int, frame: BasicFrame):
        """
        change the frame id by new frame

        @param frame_id:
        @param frame:

        """
        self.__game_content[frame_id] = frame

    @engine_exception_handler
    def commit(self):
        """
        commit all the change to the local game file

        @return: commit status
        """
        self.__update_metadata()
        game_content_raw = [self.__metadata, self.__game_content]
        try:
            self.__dumper(game_content_raw, self.__game_file_dir)
        except Exception as e:
            raise EngineError(f"fail to dump game file due to: {str(e)}") from e
