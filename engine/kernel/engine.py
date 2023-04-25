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

from module.config_module import ConfigLoader
from utils.file_utils import check_file_valid, check_folder_valid, abs_dir
from utils.status import StatusCode
from utils.exception import EngineError
from kernel.frame import Frame, FrameChecker, FrameInfo
from kernel.chapter import Chapter
import kernel.engine_io as eng_io
from kernel.component import Background, Character, Dialogue, Music, FrameMeta

# the version of the kernel
ENGINE_NAME = "YuiEngine"
ENGINE_VERSION = "1.1.2"
ENGINE_MINIMAL_COMPATIBLE = "1.1.2"


class Engine:
    """
    Engine main class, used to edit frame in project
    """

    def __init__(
        self,
        project_dir: str,
        config_dir: str,
        game_file_name: Optional[str] = None,
    ):
        """
        constructor for kernel

        @param project_dir: project directory
        @param config_dir: config file directory
        @param game_file_name: game file name (not directory)

        """

        self.__metadata_buffer: dict = {}  # metadata for the game file

        # variables that need to update once change
        self.__game_content: dict[int, Frame] = {}  # game content
        self.__chapter_meta: dict[str, Chapter] = {}  # {chapter name: Chapter instance}
        self.__head: int = Frame.VOID_FRAME_ID  # the head of the frame list
        self.__tail: int = Frame.VOID_FRAME_ID  # the tail of the frame list
        self.__all_fids: set[int] = set()  # all fids in set

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
            # if the local game file already exist, load its information
            self.__load_local_file()

    def __load_local_file(self):
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
                f"detect kernel incompatible! "
                f"try to load game file with '{cur_engine_name}' using kernel '{ENGINE_NAME}'"
            )

        if version.parse(cur_engine_version) < version.parse(ENGINE_MINIMAL_COMPATIBLE):
            raise EngineError(
                f"detect version incompatible! "
                f"the current kernel ({ENGINE_VERSION}) "
                f"do not support the game file version ({cur_engine_version})"
            )

        if cur_engine_version != ENGINE_VERSION:
            print(
                f"WARNING: detect kernel version ({ENGINE_VERSION}) "
                f"mismatched with game file ({cur_engine_version})"
            )

        self.__game_content: dict[int, Frame] = game_content_raw[1]
        self.__chapter_meta: dict[str, Chapter] = game_content_raw[2]
        self.__head: int = self.__metadata_buffer["head"]
        self.__tail: int = self.__metadata_buffer["tail"]
        self.__all_fids: set[int] = set(self.__game_content.keys())

    def __update_metadata(self):
        """
        update the metadata by global variable

        """
        self.__metadata_buffer["engine_name"] = ENGINE_NAME
        self.__metadata_buffer["engine_version"] = ENGINE_VERSION
        self.__metadata_buffer["engine_minimal_compatible"] = ENGINE_MINIMAL_COMPATIBLE
        self.__metadata_buffer["update_at"] = time.time()
        self.__metadata_buffer["total_frame_len"] = len(self.__game_content.keys())
        self.__metadata_buffer["head"] = self.__head
        self.__metadata_buffer["tail"] = self.__tail

    @staticmethod
    def make_frame(
        background: Background,
        chara: list[Character],
        music: Music,
        dialog: Dialogue,
        meta: FrameMeta,
    ) -> Frame:
        """
        make a frame

        @param background: background
        @param chara: character
        @param music: music
        @param dialog: dialog
        @param meta the metadata for the frame
        @return: result frame

        """
        frame = Frame(Frame.VOID_FRAME_ID, background, chara, music, dialog, meta)
        return frame

    @staticmethod
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

    def __append(self, frame: Frame) -> int:
        """
        append a frame into the game content

        @param frame: frame to be added
        @return the frame id

        """

        # generate the fid
        if len(self.__all_fids) == 0:
            fid = 0
        else:
            fid = max(self.__all_fids) + 1

        frame.fid = fid

        # change the current last frame's next frame pointer
        if self.__head != Frame.VOID_FRAME_ID:
            self.__game_content[self.__tail].action.next_f = fid
        else:
            self.__head = fid

        # update the current frame
        frame.action.prev_f = self.__tail

        # update activated variables
        self.__game_content[fid] = frame

        self.__all_fids.add(fid)

        self.__tail = fid

        return fid

    def __insert(self, frame: Frame, after_fid: int) -> int:
        """
        Insert a frame into the game content after a specific frame id

        @param after_fid: frame id after which the new frame should be inserted
        @param frame: frame to be inserted
        @return the inserted frame id
        """

        if after_fid == -1:
            return self.__append(frame)

        if after_fid not in self.__game_content:
            raise EngineError(
                f"Frame with id {after_fid} not found in the game content"
            )

        # Generate the new frame id
        new_fid = max(self.__all_fids) + 1
        frame.fid = new_fid

        # Find the frame after which the new frame will be inserted
        after_frame = self.__game_content[after_fid]

        # Update the next and previous frame pointers of the new frame
        frame.action.prev_f = after_fid
        frame.action.next_f = after_frame.action.next_f

        # Update the next frame pointer of the frame after which the new frame is inserted
        after_frame.action.next_f = new_fid

        # Update the previous frame pointer of the frame that comes after the new frame
        if frame.action.next_f != Frame.VOID_FRAME_ID:
            next_frame = self.__game_content[frame.action.next_f]
            next_frame.action.prev_f = new_fid

        # Update the game content
        self.__game_content[new_fid] = frame

        # Update the list of all frame ids
        self.__all_fids.add(new_fid)

        # Update the tail of the linked list, if necessary
        if self.__tail == after_fid:
            self.__tail = new_fid

        return new_fid

    def __remove(self, fid: int):
        """
        remove the frame from game content

        @param fid: id of frame

        """
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

        # update game content and metadata
        self.__game_content.pop(fid)
        self.__all_fids.remove(fid)

    def append_frame(self, frame: Frame, to_chapter: str, force: bool = False) -> int:
        """
        add frame to the end of the frame list

        @param to_chapter: append to this chapter
        @param force: force push mode, ignore checking frame valid
        @param frame: frame to be added
        @return:  frame id

        """
        # check if chapter exist
        if to_chapter not in self.__chapter_meta.keys():
            raise EngineError(f"Chapter '{to_chapter}' no found")

        # check frame valid or not
        if not force:
            check_output = self.__frame_checker.check(frame)
            if not check_output[0]:
                raise EngineError(f"Frame invalid: {check_output[1]}")

        # append to the game content
        tail_id = self.__chapter_meta[to_chapter].get_tail_fid()
        fid = self.__insert(frame, after_fid=tail_id)

        # update frame meta and chapter info
        self.__chapter_meta[to_chapter].append_frame_info(FrameInfo(fid, frame.meta))

        return fid

    def remove_frame(self, fid: int):
        """
        remove the frame from game content

        @param fid: id of frame

        """
        if not self.check_frame_exist(fid):
            raise EngineError("remove fail, frame not exist")

        self.__remove(fid)

        # update chapter data
        for chapter in self.__chapter_meta.values():
            if chapter.remove_fid(fid) != -1:
                return
        raise EngineError("kernel error when remove frame, contact developer for help")

    def change_frame(self, fid: int, frame: Frame):
        """
        change the frame id by new frame

        @param fid: the id of the frame
        @param frame: added frame

        """
        if not self.check_frame_exist(fid):
            raise EngineError(f"fid '{fid}' no found")

        self.__game_content[fid] = frame

    def check_frame_exist(self, fid: int) -> bool:
        """
        check if the frame with fid in the game content

        @param fid: frame id
        @return: exist or not

        """
        return fid in self.__all_fids

    def get_frame(self, fid: int) -> Frame:
        """
        get frame by frame id, return none if nothing find

        @param fid: frame id
        @return: shallow copy of frame with such fid

        """
        if fid not in self.__game_content:
            raise EngineError(f"the fid '{fid}' not exist")

        return self.__game_content[fid]

    def length(self) -> int:
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
        get version of current kernel

        @return: metadata of kernel

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
            self.__chapter_meta,
        ]
        try:
            self.__dumper(game_content_raw, self.__game_file_dir)
        except Exception as e:
            raise EngineError(f"fail to dump game file due to: {str(e)}") from e
        return StatusCode.OK

    def rollback(self):
        """
        rollback to the last modified status

        """
        try:
            self.__load_local_file()
        except Exception as e:
            print(f"something wrong when rollback: {str(e)}")

        print("rollback ok!")

    def render_struct(self, by_chapter: Optional[str] = None) -> dict:
        """
        render the game content struct, if chapter set to be none,
        return the whole struct, or will only render the struct under
        the specified chapter

        @return: the struct for game content

        """
        if by_chapter is None:
            out = {}
            for chapter_name, chapter_info in self.__chapter_meta.items():
                out[chapter_name] = chapter_info.get_all_fid()
            return out

        if by_chapter not in self.__chapter_meta.keys():
            raise EngineError(f"chapter with name '{by_chapter}' not exist")
        out = {}
        chapter_info = self.__chapter_meta[by_chapter]
        out[by_chapter] = chapter_info.get_all_fid()
        return out

    def get_all_chapter(self) -> list:
        """
        get all chapters

        @return: all chapters currently

        """
        return list(self.__chapter_meta.keys())

    def get_chapter(self, chapter_name: str) -> Chapter:
        """
        get a chapter by providing chapter name

        @param chapter_name: the name for the chapter.
        @return: the chapter instance

        """
        if chapter_name not in self.__chapter_meta:
            raise EngineError(f"cannot find chapter with name: '{chapter_name}'")
        return self.__chapter_meta[chapter_name]

    def add_chapter(self, chapter_name):
        """
        add an empty chapter

        @param chapter_name: name for chapter

        """
        if chapter_name in self.__chapter_meta:
            raise EngineError(f"chapter '{chapter_name}' already exist")

        self.__chapter_meta[chapter_name] = Chapter(chapter_name)

    def remove_chapter(self, chapter_name):
        """
        remove the chapter and the frames in it

        @param chapter_name: the name for chapter
        @return:

        """
        if chapter_name not in self.__chapter_meta:
            raise EngineError(f"chapter name {chapter_name} not exist")

        fids = self.__chapter_meta[chapter_name].get_all_fid()
        for i in fids:
            self.remove_frame(i)

        self.__chapter_meta.pop(chapter_name)

    def get_frame_name(self, fid: int):
        """
        get the frame name by providing frame id

        @param fid: the frame id
        @return: the frame name

        """
        frame = self.get_frame(fid)
        return frame.meta.name

    def get_frame_ids(self) -> set:
        """
        get all fids

        @return: all fids

        """
        return self.__all_fids
