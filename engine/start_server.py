"""
router service main entry
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from module.project_manager import ProjectManager
from module.config_manager import ConfigLoader
from utils.args_utils import STATUS

app = FastAPI()

CONFIG_DIR = "./service.ini"


class ReturnBody(BaseModel):
    status: STATUS = STATUS.FAIL
    msg: Optional[str]
    content: Optional[list]


def router_exception_handler(func):
    """
    exception decorator for router

    @param func: function to be decorated
    @return:
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e_msg:
            print("Router Error: ", str(e_msg))
            return ReturnBody(status=STATUS.FAIL, msg=f"fail due to: {str(e_msg)}")

    return wrapper


class RouterUtils:
    """
    class for router service

    """

    def __init__(self):
        """
        constructor for router class

        """
        self.__project_manager: ProjectManager = ProjectManager()
        self.__config_loader = ConfigLoader(config_dir=CONFIG_DIR)

    @router_exception_handler
    def init_project(self, base_dir: str) -> ReturnBody:
        """
        initialize project

        @param base_dir: project directory
        @return: status code
        """
        self.__project_manager.init_project(base_dir=base_dir, config_dir=CONFIG_DIR)
        return ReturnBody(status=STATUS.OK, msg=f"initialize project at: {base_dir}")

    @router_exception_handler
    def get_background_resources(self, filter_str: str = "") -> ReturnBody:
        """
        get background resources

        @param filter_str: filter resources by a specific string
        @return: status code
        """
        resources = self.__project_manager.get_backgrounds_res(filter_by=filter_str)
        print(resources)
        return ReturnBody(status=STATUS.OK, content=resources)


router_utils = RouterUtils()


@app.post("/initialize_project")
async def init_project(base_dir: str) -> ReturnBody:
    return router_utils.init_project(base_dir=base_dir)


@app.post("/get_background")
async def get_background(filter_by: str = "") -> ReturnBody:
    return router_utils.get_background_resources(filter_by)
