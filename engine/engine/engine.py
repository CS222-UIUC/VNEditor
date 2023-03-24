"""
----------------------------
The Best Visual Novel Engine
        Yui Engine
----------------------------

contain all basic information to build a visual novel
"""

import time
from packaging import version

from typing import Optional
from functools import wraps
from module.exception import EngineError
from module.config_manager import ConfigLoader
from utils.file_utils import check_file_valid, check_folder_valid, abs_dir
from utils.status import StatusCode
from engine.frame import BasicFrame
from engine.f_checker import FrameChecker
from engine.f_maker import FrameMaker
import engine.eng_io as eng_io

# the version of the engine
ENGINE_NAME = "YuiEngine"
ENGINE_VERSION = "1.0.0"
ENGINE_MINIMAL_COMPATIBLE = "1.0.0"


def engine_exception_handler(func):
    """
    exception decorator for engine

    @param func: function to be decorated

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e_msg:
            print(f"Engine Error ({type(e_msg).__name__}): ", str(e_msg))
            return StatusCode.FAIL

    wrapper: func
    return wrapper


class Engine:
    """
    Engine main class, used to edit frame in project
    """

    # metadata for the game file, update automatically
    # through calling update_metadata() function
    __metadata_buffer: dict = {}

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
            self.__metadata_buffer = game_content_raw[0]

            # check game file incompatibility
            cur_engine_name = self.__metadata_buffer["engine_name"]
            cur_engine_version = self.__metadata_buffer["engine_version"]
            if self.__metadata_buffer["engine_name"] != ENGINE_NAME:
                raise EngineError(f"detect engine incompatible! "
                                  f"try to load game file with '{cur_engine_name}' using engine '{ENGINE_NAME}'")

            if version.parse(cur_engine_version) < version.parse(ENGINE_MINIMAL_COMPATIBLE):
                raise EngineError(f"detect version incompatible! "
                                  f"the current engine ({ENGINE_VERSION}) "
                                  f"do not support the game file version ({cur_engine_version})")

            if cur_engine_version != ENGINE_VERSION:
                print(f"WARNING: detect engine version ({ENGINE_VERSION}) "
                      f"mismatched with game file ({cur_engine_version})")

            # load metadata
            self.__game_content = game_content_raw[1]
            self.__last_fid = self.__metadata_buffer["last_fid"]
            self.__head = self.__metadata_buffer["head"]
            self.__tail = self.__metadata_buffer["tail"]
            self.__all_fids = set(self.__game_content.keys())

    @engine_exception_handler
    def __update_metadata(self):
        """
        update the metadata by global variable

        """
        self.__metadata_buffer["engine_name"] = ENGINE_NAME
        self.__metadata_buffer["engine_version"] = ENGINE_VERSION
        self.__metadata_buffer["engine_minimal_compatible"] = ENGINE_MINIMAL_COMPATIBLE
        self.__metadata_buffer["update_at"] = time.time()
        self.__metadata_buffer["total_frame_len"] = len(self.__game_content.keys())
        self.__metadata_buffer["last_fid"] = self.__last_fid
        self.__metadata_buffer["head"] = self.__head
        self.__metadata_buffer["tail"] = self.__tail

    @engine_exception_handler
    def make_frame(self, _type: type, **kwargs) -> BasicFrame:
        frame = self.__frame_maker.make(_type, **kwargs)

        if frame is None:
            raise EngineError("make frame failed")

        return frame

    @engine_exception_handler
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

        # update the current frame
        frame.action.prev_f = self.__last_fid

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

        # update game content and metadata
        self.__game_content.pop(frame_id)
        if len(self.__game_content) == 0:
            self.__last_fid = BasicFrame.VOID_FRAME_ID
        self.__all_fids.remove(frame_id)

    @engine_exception_handler
    def change_frame(self, frame_id: int, frame: BasicFrame):
        """
        change the frame id by new frame

        @param frame_id:
        @param frame:

        """
        self.__game_content[frame_id] = frame

    @engine_exception_handler
    def get_head_id(self) -> int:
        """
        get the head frame id
        @return: the id for the frame on head

        """
        return self.__head

    @engine_exception_handler
    def get_tail_id(self) -> int:
        """
        get the tail frame id
        @return: the id for the frame on tail

        """
        return self.__tail

    @engine_exception_handler
    def get_frame(self, fid: int) -> BasicFrame | None:
        """
        get frame by frame id, return none if nothing find

        @param fid: frame id
        @return: shallow copy of frame with such fid

        """
        if fid not in self.__game_content:
            return None
        return self.__game_content[fid]

    @engine_exception_handler
    def get_all_frames(self) -> dict[int, BasicFrame]:
        """
        get all frames

        @return: format by dict[frame id, shallow copy of frame]

        """
        return self.__game_content

    @engine_exception_handler
    def get_all_frame_id(self) -> set:
        """
        get all frame id

        @return: the set of all frame id

        """
        return set(self.__game_content.keys())

    @engine_exception_handler
    def get_length(self) -> int:
        """
        get the total length of the game content

        @return: the length of game content

        """
        return len(self.__game_content)

    @engine_exception_handler
    def get_metadata_buffer(self) -> dict[dict, dict] | None:
        """
        get the current meta buffer, WARNING, this method
        return the buffered metadata, might not be up-to-date

        @return: metadata in buffer

        """
        if len(self.__metadata_buffer) == 0:
            return None
        return self.__metadata_buffer

    @engine_exception_handler
    def get_engine_version(self) -> str:
        """
        get version of current engine

        @return: version of engine

        """
        return ENGINE_VERSION

    @engine_exception_handler
    def commit(self):
        """
        commit all the change to the local game file

        @return: commit status
        """
        self.__update_metadata()
        game_content_raw = [self.__metadata_buffer, self.__game_content]
        try:
            self.__dumper(game_content_raw, self.__game_file_dir)
        except Exception as e:
            raise EngineError(f"fail to dump game file due to: {str(e)}") from e
