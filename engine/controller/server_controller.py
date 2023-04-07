"""
controller for directly control server files and folders

"""
import os

from functools import wraps

from module.config_manager import ConfigLoader
from utils.status import StatusCode
from utils.file_utils import check_folder_valid, delete_folder

from utils.return_type import ReturnStatus


def file_controller_exception_handler(func):
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


class ServerController:
    """
    a direct entry to manipulate files

    """

    def __init__(self, config_dir: str):
        """
        constructor for router class

        """
        config = ConfigLoader(config_dir)
        self.__config_res = config.resources()
        self.__project_base_dir = config.project()["projects_base"]

    @file_controller_exception_handler
    def delete_project(self, project_name: str) -> ReturnStatus:
        folder_dir = os.path.join(self.__project_base_dir, project_name)

        if not check_folder_valid(folder_dir):
            return ReturnStatus(status=False, msg=f"fail remove project '{folder_dir}'")

        if delete_folder(folder_dir=folder_dir):
            return ReturnStatus(
                status=True, msg=f"successfully remove project '{folder_dir}'"
            )

        return ReturnStatus(status=False, msg=f"fail remove project '{folder_dir}'")
