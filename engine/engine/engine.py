"""
----------------------------
The Best Visual Novel Engine
        Yui Engine
----------------------------

contain all basic information to build a visual novel

"""
import time
from typing import Optional
from packaging import version

from module.config_manager import ConfigLoader
from utils.file_utils import check_file_valid, check_folder_valid, abs_dir
from utils.status import StatusCode
from utils.exception import EngineError
from engine.frame import Frame, FrameChecker
from engine.chapter import Chapter
import engine.engine_io as eng_io
from engine.component import Background, Character, Dialogue, Music, FrameMeta

# the version of the engine
ENGINE_NAME = "YuiEngine"
ENGINE_VERSION = "1.0.3"
ENGINE_MINIMAL_COMPATIBLE = "1.0.3"


class Engine:
    """
    Engine main class, used to edit frame in project
    """

    # metadata for the game file, update automatically
    # through calling update_metadata() function
    __metadata_buffer: dict = {}

    # activated variables, initialized after class construct,
    # should be UPDATED ON TIME every time they changed
    __game_content: dict[int, Frame] = {}
    __frame_meta: dict[
        str, list[tuple[int, str]]
    ] = {}  # meta data for frames {chapter_name: [(fid: frame_name)]}
    __head: int = Frame.VOID_FRAME_ID  # the head of the frame list
    __tail: int = Frame.VOID_FRAME_ID  # the tail of the frame list
    __last_fid: int = Frame.VOID_FRAME_ID  # the last used fid (frame id)
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

            # check game file compatibility
            cur_engine_name = self.__metadata_buffer["engine_name"]
            cur_engine_version = self.__metadata_buffer["engine_version"]
            if self.__metadata_buffer["engine_name"] != ENGINE_NAME:
                raise EngineError(
                    f"detect engine incompatible! "
                    f"try to load game file with '{cur_engine_name}' using engine '{ENGINE_NAME}'"
                )

            if version.parse(cur_engine_version) < version.parse(
                    ENGINE_MINIMAL_COMPATIBLE
            ):
                raise EngineError(
                    f"detect version incompatible! "
                    f"the current engine ({ENGINE_VERSION}) "
                    f"do not support the game file version ({cur_engine_version})"
                )

            if cur_engine_version != ENGINE_VERSION:
                print(
                    f"WARNING: detect engine version ({ENGINE_VERSION}) "
                    f"mismatched with game file ({cur_engine_version})"
                )

            # load game content and frame description
            self.__game_content = game_content_raw[1]
            self.__frame_meta = game_content_raw[2]

            # load metadata
            self.__last_fid = self.__metadata_buffer["last_fid"]
            self.__head = self.__metadata_buffer["head"]
            self.__tail = self.__metadata_buffer["tail"]
            self.__all_fids = set(self.__game_content.keys())

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

    @staticmethod
    def make_frame(
            background: Background,
            chara: list[Character],
            music: Music,
            dialog: Dialogue,
    ) -> Frame:
        """
        make a frame

        @param background: background
        @param chara: character
        @param music: music
        @param dialog: dialog
        @return: result frame

        """
        frame = Frame(Frame.VOID_FRAME_ID, background, chara, music, dialog, None)
        return frame

    @staticmethod
    def make_chapter(chapter_name: str) -> Chapter:
        """
        make a chapter
        @return: result chapter

        """
        chapter = Chapter(Chapter.VOID_FRAME_ID, chapter_name)
        return chapter

    def __append(self, frame: Chapter | Frame):
        """
        append chapter ot frame into the game content

        @param frame: frame to be added
        @return the frame id

        """

        # generate the fid
        if self.__last_fid == Frame.VOID_FRAME_ID:
            fid = 0
        else:
            fid = self.__last_fid + 1
        frame.fid = fid

        # change the current last frame's next frame pointer
        if self.__last_fid != Frame.VOID_FRAME_ID:
            self.__game_content[self.__last_fid].action.next_f = fid

        # update the current frame
        frame.action.prev_f = self.__last_fid

        # update activated variables
        self.__game_content[fid] = frame

        self.__last_fid = fid
        self.__all_fids.add(fid)

        # update head and tail
        if self.__head == Frame.VOID_FRAME_ID:
            self.__head = fid

        self.__tail = fid

        return fid

    def append_frame(
            self, frame: Frame, frame_meta: FrameMeta, force: bool = False
    ) -> int:
        """
        add frame to the end of the frame list

        @param frame_meta: frame metadata
        @param force: force push mode, ignore checking frame valid
        @param frame: frame to be added
        @return:  frame id

        """

        # check if chapter exist
        if frame_meta.chapter not in self.__frame_meta.keys():
            raise EngineError(f"Chapter '{frame_meta.chapter}' no found")

        # check frame valid or not
        if not force:
            check_output = self.__frame_checker.check(frame)
            if not check_output[0]:
                raise EngineError(f"Frame invalid: {check_output[1]}")

        # append to the game content
        fid = self.__append(frame)

        # update frame meta
        self.__frame_meta[frame_meta.chapter].append((fid, frame_meta.name))

        return fid

    def append_chapter(self, chapter: Chapter):
        """
        append a chapter into the game content

        @param chapter: the instance for chapter

        """

        # check if chapter already in use
        if chapter.chapter_name in self.__frame_meta.keys():
            raise EngineError(f"Chapter '{chapter.chapter_name}' already in use")

        self.__append(chapter)

        # update frame meta
        self.__frame_meta[chapter.chapter_name] = []

    def get_ordered_fid(self) -> list:
        """
        return a ordered frame id

        @return: ordered fid

        """
        if self.__head == Frame.VOID_FRAME_ID:
            return []

        ordered_id = [self.__head]
        while 1:
            cur = ordered_id[-1]
            next_fid = self.get_frame(cur).action.next_f
            if next_fid == Frame.VOID_FRAME_ID:
                break
            ordered_id.append(next_fid)

        return ordered_id

    def get_frame_meta(self, fid: int) -> FrameMeta:
        """
        find the frame metadata by frame

        @param fid: frame id
        @return: the metadata of the frame

        """
        for chapter, chapter_list in self.__frame_meta.items():
            for f in chapter_list:
                if fid == f[0]:
                    frame_meta = FrameMeta(chapter=chapter, name=f[1])
                    return frame_meta

        raise EngineError(f"cannot find fid '{fid}' in frame metadata")

    def remove_frame(self, fid: int):
        """
        remove the frame from game content

        @param fid: id of frame

        """
        if fid not in self.__all_fids:
            raise EngineError("remove fail, frame not exist")

        cur_frame = self.__game_content[fid]
        if fid != self.__head:
            self.__game_content[
                cur_frame.action.prev_f
            ].action.next_f = cur_frame.action.next_f
        else:
            self.__head = cur_frame.action.next_f

        if fid != self.__tail:
            self.__game_content[
                cur_frame.action.next_f
            ].action.prev_f = cur_frame.action.prev_f
        else:
            self.__tail = cur_frame.action.prev_f
            self.__last_fid = self.__tail

        # update game content and metadata
        self.__game_content.pop(fid)

        # update frame metadata
        for chapter_list in self.__frame_meta.values():
            for idx in range(len(chapter_list)):
                if fid == [0]:
                    chapter_list.pop(idx)
                    break

        if len(self.__game_content) == 0:
            self.__last_fid = Frame.VOID_FRAME_ID
        self.__all_fids.remove(fid)

    def change_frame(self, fid: int, frame: Frame):
        """
        change the frame id by new frame

        @param fid: the id of the frame
        @param frame: added frame

        """
        if fid not in self.__game_content or isinstance(self.__game_content[fid], Chapter):
            raise EngineError(f"fid '{fid}' no found")

        self.__game_content[fid] = frame

    def get_head_id(self) -> int:
        """
        get the head frame id
        @return: the id for the frame on head

        """
        return self.__head

    def get_tail_id(self) -> int:
        """
        get the tail frame id
        @return: the id for the frame on tail

        """
        return self.__tail

    def check_frame_exist(self, fid: int) -> bool:
        """
        check if the frame with fid in the game content

        @param fid: frame id
        @return: exist or not

        """
        return fid in self.__game_content

    def get_frame(self, fid: int) -> Frame:
        """
        get frame by frame id, return none if nothing find

        @param fid: frame id
        @return: shallow copy of frame with such fid

        """
        return self.__game_content[fid]

    def get_all_frames(self) -> dict[int, Frame]:
        """
        get all frames

        @return: format by dict[frame id, shallow copy of frame]

        """
        return self.__game_content

    def get_all_frame_id(self) -> set:
        """
        get all frame id

        @return: the set of all frame id

        """
        return set(self.__game_content.keys())

    def get_length(self) -> int:
        """
        get the total length of the game content

        @return: the length of game content

        """
        return len(self.__game_content)

    def get_metadata_buffer(self) -> dict[dict, dict]:
        """
        get the current meta buffer, WARNING: this method
        return the buffered metadata, might not be up-to-date

        @return: metadata in buffer

        """
        if len(self.__metadata_buffer) == 0:
            return {}
        return self.__metadata_buffer

    @staticmethod
    def get_engine_meta() -> dict:
        """
        get version of current engine

        @return: metadata of engine

        """
        return {
            "version": ENGINE_VERSION,
            "name": ENGINE_NAME,
        }

    def commit(self) -> StatusCode:
        """
        commit all the change to the local game file

        @return: commit status

        """
        self.__update_metadata()
        game_content_raw = [
            self.__metadata_buffer,
            self.__game_content,
            self.__frame_meta,
        ]
        try:
            self.__dumper(game_content_raw, self.__game_file_dir)
        except Exception as e:
            raise EngineError(f"fail to dump game file due to: {str(e)}") from e
        return StatusCode.OK

    def render_struct(self, chapter: Optional[str] = None):
        """
        render the game content struct, if chapter set to be none,
        return the whole struct, or will only render the struct under
        the specified chapter

        @return: the struct for game content

        """
        if chapter is None:
            return self.__frame_meta

        if chapter not in self.__frame_meta:
            return {}
        return self.__frame_meta[chapter]

    def get_all_chapter(self) -> list:
        """
        get all chapters

        @return: all chapters currently

        """
        return list(self.__frame_meta.keys())
