"""
router service main entry
"""

import os
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import FileResponse
from enum import Enum

from module.project_manager import ProjectManager
from module.config_manager import ConfigLoader
from module.exception import RouterError
from utils.args_utils import STATUS

app = FastAPI()

CONFIG_DIR = "./service.ini"


class ResourcesType(str, Enum):
    background = "background"
    music = "music"
    character = "character"


class ReturnStatus(BaseModel):
    status: STATUS = STATUS.FAIL
    msg: Optional[str]


class ReturnList(ReturnStatus):
    msg: str = "ok"
    content: Optional[list]


class ReturnDict(ReturnStatus):
    msg: str = "ok"
    content: Optional[dict]


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
            return ReturnStatus(status=STATUS.FAIL, msg=str(e_msg))

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
        self.__resources_config: dict = self.__config_loader.resources()
        self.version_info: dict = self.__config_loader.version()

    @router_exception_handler
    def init_project(self, base_dir: str) -> ReturnStatus:
        """
        initialize project

        @param base_dir: project directory
        @return: status code
        """
        self.__project_manager.init_project(base_dir=base_dir, config_dir=CONFIG_DIR)
        return ReturnStatus(status=STATUS.OK, msg=f"initialize project at: {base_dir}")

    @router_exception_handler
    def get_resources(self, rtype=ResourcesType, filter_str: str = "") -> ReturnList:
        """
        get background resources

        @param rtype: type of resources to fetch
        @param filter_str: filter resources by a specific string
        @return: status code
        """
        if rtype is ResourcesType.background:
            resources = self.__project_manager.get_backgrounds_res(filter_by=filter_str)
        elif rtype is ResourcesType.music:
            resources = self.__project_manager.get_music_res(filter_by=filter_str)
        elif rtype is ResourcesType.character:
            resources = self.__project_manager.get_character_res(filter_by=filter_str)
        else:
            raise RouterError(f"cannot find rtype: '{rtype}'")

        return ReturnList(status=STATUS.OK, content=resources)

    @router_exception_handler
    def upload_file(self, rtype: ResourcesType, file: UploadFile) -> ReturnDict:
        max_file_size = int(self.__resources_config["max_size"])
        suffix = os.path.splitext(file.filename)[-1]

        if rtype is ResourcesType.background:
            to_path = os.path.join(self.__project_manager.get_base_dir(),
                                   self.__resources_config["background_dir"])
            if suffix not in self.__resources_config["background_support"].split(','):
                raise RouterError(f"file type '{suffix}' not support")

        elif rtype is ResourcesType.music:
            to_path = os.path.join(self.__project_manager.get_base_dir(),
                                   self.__resources_config["music_dir"])
            if suffix not in self.__resources_config["music_support"].split(','):
                raise RouterError(f"file type '{suffix}' not support")

        elif rtype is ResourcesType.character:
            to_path = os.path.join(self.__project_manager.get_base_dir(),
                                   self.__resources_config["character_dir"])
            if suffix not in self.__resources_config["character_support"].split(','):
                raise RouterError(f"file type '{suffix}' not support")
        else:
            raise RouterError(f"no such rtype: {rtype}")

        file_content = file.file.read()
        file_size = len(file_content)

        if len(file_content) > max_file_size:
            file.file.close()
            raise RouterError(f"file excess max size {str(max_file_size)}")
        try:
            with open(os.path.join(to_path, file.filename), "wb") as f_stream:
                f_stream.write(file_content)
        except Exception as e:
            file.file.close()
            raise RouterError(f"cannot write file {file.filename} due to {str(e)}")
        finally:
            file.file.close()

        to_return = {"filename": file.filename, "directory": to_path, "size": file_size}
        return ReturnDict(status=STATUS.OK, content=to_return)

    @router_exception_handler
    def get_base_dir(self) -> ReturnDict:
        to_return = {"base": self.__project_manager.get_base_dir()}
        return ReturnDict(status=STATUS.OK, content=to_return)


router_utils = RouterUtils()

with open('doc/ascii_logo', 'r') as f_stream:
    print('\n', f_stream.read())
    print("\n"
          f"{router_utils.version_info['name']}\n"
          f"Version: {router_utils.version_info['version']}\n")


@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse('doc/index.html')


@app.get("/baka", include_in_schema=False)
async def read_index():
    return FileResponse('doc/baka.png')


@app.post("/init_project")
async def initialize_project(base_dir: str) -> ReturnStatus:
    """
    initialize project, create new if given directory not exist

    @param base_dir: where is the project
    """
    result = router_utils.init_project(base_dir=base_dir)
    return result


@app.post("/get_res")
async def get_resources(rtype: ResourcesType, filter_by: str = "") -> ReturnList:
    """
    get background resources, need to initialize project before use

    @param rtype: type of resources to get
    @param filter_by: filter by specific string
    """
    result = router_utils.get_resources(rtype=rtype, filter_str=filter_by)
    return result


@app.post("/upload/")
async def upload_file(rtype: ResourcesType, file: UploadFile):
    return router_utils.upload_file(rtype=rtype, file=file)


@app.post("/get_base/")
async def get_base_dir() -> ReturnDict:
    """
    get the base directory of the project

    """
    return router_utils.get_base_dir()
