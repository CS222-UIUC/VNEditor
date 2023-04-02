import os

from functools import wraps
from fastapi import UploadFile

from engine.engine import Engine
from module.project_manager import ProjectManager, ResourcesType
from module.config_manager import ConfigLoader
from utils.exception import ControllerException
from utils.status import StatusCode
from utils.file_utils import check_file_valid

from utils.return_type import ReturnList, ReturnDict, ReturnStatus

from .project_controller import Task


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
    def get_frames(self, task: Task):
        engine = 1
