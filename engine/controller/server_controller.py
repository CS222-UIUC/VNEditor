"""
controller for directly control server files and folders

"""
import os

from functools import partial

from module.config_module import ConfigLoader
from utils.file_utils import check_folder_valid, delete_folder
from utils.exception_handler import exception_handler

from utils.return_type import ReturnStatus

file_controller_exception_handler = partial(exception_handler, module_name="Server Controller", debug=False)


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
