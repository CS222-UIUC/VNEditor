from functools import wraps

from module.config_manager import ConfigLoader
from utils.exception import ControllerException
from utils.status import StatusCode
from utils.return_type import ReturnList, ReturnDict, ReturnStatus

from .project_controller import Task
from engine.frame import Frame, FrameModel


def engine_controller_exception_handler(func):
    """
    exception decorator for router

    @param func: function to be decorated

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e_msg:
            print(f"Project Controller Error ({type(e_msg).__name__}): ", str(e_msg))
            return ReturnStatus(status=StatusCode.FAIL, msg=str(e_msg))

    wrapper: func
    return wrapper


class EngineController:
    """
    class for engine controller

    """

    def __init__(self, config_dir: str):
        """
        constructor for router class

        """
        config_loader = ConfigLoader(config_dir=config_dir)
        self.__engine_config: dict = config_loader.engine()

    @engine_controller_exception_handler
    def get_frames_id(self, task: Task) -> ReturnList:
        """
        get all frame id

        @param task:
        @return: list of ordered frame id

        """
        engine = task.project_engine
        fids = engine.get_ordered_fid()
        if fids == StatusCode.FAIL:
            raise ControllerException("get frame id fails")

        return ReturnList(status=StatusCode.OK, content=fids)

    @engine_controller_exception_handler
    def get_engine_meta(self, task: Task) -> ReturnDict:
        """
        get the metadata for engine

        @return: metadata for engine

        """
        engine = task.project_engine
        return ReturnDict(status=StatusCode.OK, content=engine.get_engine_meta())

    @engine_controller_exception_handler
    def append_frame(
            self, task: Task, frame_component_raw: FrameModel, force=False
    ) -> ReturnList:
        """
        append frame: Frame into game content

        @return: metadata for engine

        """
        engine = task.project_engine
        frame_component = frame_component_raw.to_frame().__dict__
        frame_component.pop("fid")
        frame_component.pop("action")
        frame = engine.make_frame(**frame_component)
        fid = engine.append_frame(frame, force)
        if fid == StatusCode.FAIL:
            return ReturnList(status=StatusCode.FAIL)
        else:
            return ReturnList(status=StatusCode.OK, content=[fid])

    def get_frame(self, task: Task, fid: int) -> ReturnDict:
        """
        get the frame information

        @return: content of frame with given id

        """
        engine = task.project_engine
        frame_raw = engine.get_frame(fid=fid)
        if frame_raw is None:
            return ReturnDict(status=StatusCode.FAIL, msg=f"No such frame id '{fid}'")
        background = frame_raw.background.res_name
        chara = [i.res_name for i in frame_raw.chara]
        chara_pos = [[i.position.x, i.position.y] for i in frame_raw.chara]
        music = frame_raw.music.res_name
        dialog = frame_raw.dialog.dialogue
        if frame_raw.dialog.character is None:
            dialog_character = None
        else:
            dialog_character = frame_raw.dialog.character.res_name
        if background is None:
            background = ""
        if music is None:
            music = ""
        if dialog is None:
            dialog = ""
        if dialog_character is None:
            dialog_character = ""
        to_return = FrameModel(background=background, chara=chara, chara_pos=chara_pos, music=music,
                               dialog=dialog, dialog_character=dialog_character)
        return ReturnDict(content=to_return.__dict__)

    @engine_controller_exception_handler
    def commit(self, task: Task) -> ReturnStatus:
        """
        commit all changes

        @param task: current task
        @return: status

        """
        engine = task.project_engine
        status = engine.commit()
        if status == StatusCode.FAIL:
            return ReturnStatus(status=StatusCode.FAIL, msg="fail to commit changes")

        return ReturnStatus(status=StatusCode.OK)

    @engine_controller_exception_handler
    def get_metadata(self, task: Task) -> ReturnDict:
        """
        get game content metadata buffer

        @param task: current task
        @return: status

        """
        engine = task.project_engine
        meta_buffer = engine.get_metadata_buffer()
        if meta_buffer is None:
            return ReturnDict(status=StatusCode.OK, content=[])

        return ReturnDict(status=StatusCode.OK, content=meta_buffer)
