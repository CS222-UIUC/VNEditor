"""
router service main entry
"""

import os
import time
from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import FileResponse
from enum import Enum
import secrets

from module.project_manager import ProjectManager
from module.config_manager import ConfigLoader
from module.exception import RouterError
from utils.args_utils import STATUS
from utils.file_utils import check_file_valid

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


class Task:
    project_manager: ProjectManager
    time_start: time

    def __init__(self, project_manager: ProjectManager):
        self.project_manager = project_manager
        self.time_start = time.time()


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
        config_loader = ConfigLoader(config_dir=CONFIG_DIR)
        self.__resources_config: dict = config_loader.resources()
        self.__project_config: dict = config_loader.project()
        self.version_info: dict = config_loader.version()

        self.__tasks: dict[str, Task] = {}

    def __new_task(self, base_dir: str) -> str:
        token = secrets.token_urlsafe(16)
        while token in self.__tasks:
            token = secrets.token_urlsafe(16)

        project_manager = ProjectManager()
        project_manager.init_project(base_dir=base_dir, config_dir=CONFIG_DIR)
        self.__tasks[token] = Task(project_manager=project_manager)
        return token

    def __get_dir_by_rtype(self, rtype: str, project_manager: ProjectManager):
        if rtype is ResourcesType.background:
            to_path = os.path.join(
                project_manager.get_base_dir(),
                self.__resources_config["background_dir"],
            )

        elif rtype is ResourcesType.music:
            to_path = os.path.join(
                project_manager.get_base_dir(),
                self.__resources_config["music_dir"],
            )

        elif rtype is ResourcesType.character:
            to_path = os.path.join(
                project_manager.get_base_dir(),
                self.__resources_config["character_dir"],
            )
        else:
            to_path = ""

        return to_path

    @router_exception_handler
    def init_project(self, base_dir: str) -> ReturnDict:
        """
        initialize project

        @param base_dir: project directory
        @return: status code
        """
        task_id = self.__new_task(base_dir)
        return ReturnDict(status=STATUS.OK,
                          msg=f"successfully initialize project in '{base_dir}'",
                          content={'task_id': task_id})

    @router_exception_handler
    def get_resource_name(self, task_id: str, rtype=ResourcesType, filter_str: str = "") -> ReturnList:
        """
        get resources name

        @param task_id: id for the task
        @param rtype: type of resources to fetch
        @param filter_str: filter resources by a specific string
        @return: status code
        """
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        if rtype is ResourcesType.background:
            resources = project_manager.get_backgrounds_res(filter_by=filter_str)
        elif rtype is ResourcesType.music:
            resources = project_manager.get_music_res(filter_by=filter_str)
        elif rtype is ResourcesType.character:
            resources = project_manager.get_character_res(filter_by=filter_str)
        else:
            raise RouterError(f"cannot find rtype: '{rtype}'")

        return ReturnList(status=STATUS.OK, content=resources)

    @router_exception_handler
    def upload_file(self, task_id: str, rtype: ResourcesType, file: UploadFile) -> ReturnDict:
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager

        max_file_size = int(self.__resources_config["max_size"])
        suffix = os.path.splitext(file.filename)[-1].lower()
        to_path = self.__get_dir_by_rtype(rtype, project_manager)

        if to_path == "":
            raise RouterError(f"no such rtype: {rtype}")

        if rtype is ResourcesType.background:
            if suffix not in self.__resources_config["background_support"].split(","):
                raise RouterError(f"file type '{suffix}' not support")

        elif rtype is ResourcesType.music:
            if suffix not in self.__resources_config["music_support"].split(","):
                raise RouterError(f"file type '{suffix}' not support")

        elif rtype is ResourcesType.character:
            if suffix not in self.__resources_config["character_support"].split(","):
                raise RouterError(f"file type '{suffix}' not support")
        else:
            raise RouterError(f"no such rtype: {rtype}")

        file_content = file.file.read()
        file_size = len(file_content)

        if len(file_content) > max_file_size:
            file.file.close()
            raise RouterError(f"file excess max size {str(max_file_size)}")
        try:
            with open(os.path.join(to_path, file.filename), "wb") as f:
                f.write(file_content)
        except Exception as e:
            file.file.close()
            raise RouterError(f"cannot write file {file.filename} due to {str(e)}")
        finally:
            file.file.close()

        to_return = {"filename": file.filename, "directory": to_path, "size": file_size}
        return ReturnDict(status=STATUS.OK, content=to_return)

    @router_exception_handler
    def get_base_dir(self, task_id: str) -> ReturnDict:
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        to_return = {"base": project_manager.get_base_dir()}
        return ReturnDict(status=STATUS.OK, content=to_return)

    @router_exception_handler
    def remove_task(self, task_id: str) -> ReturnDict:
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        task_last_time = time.time() - self.__tasks[task_id].time_start
        self.__tasks.pop(task_id)
        return ReturnDict(status=STATUS.OK, content={"task_id": task_id, "time_last": task_last_time})

    @router_exception_handler
    def get_resources(self, task_id: str, item_cat: ResourcesType, item_name: str) -> str:
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        resource_dir = self.__get_dir_by_rtype(item_cat, project_manager)
        resources_at = os.path.join(resource_dir, item_name)

        if check_file_valid(resources_at):
            return resources_at
        else:
            return ""


router_utils = RouterUtils()

with open("doc/ascii_logo", "r", encoding="UTF-8") as f_stream:
    print("\n", f_stream.read())
    print(
        "\n"
        f"{router_utils.version_info['name']}\n"
        f"Version: {router_utils.version_info['version']}\n"
    )


@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse("doc/index.html")


@app.get("/baka", include_in_schema=False)
async def read_index():
    return FileResponse("doc/baka.png")


@app.post("/init_project")
async def initialize_project(base_dir: str) -> ReturnDict:
    """
    initialize project, create new if given directory not exist

    @param base_dir: where is the project
    """
    result = router_utils.init_project(base_dir=base_dir)
    return result


@app.post("/get_res")
async def get_resources_name(task_id: str, rtype: ResourcesType, filter_by: str = "") -> ReturnList:
    """
    get background resources, need to initialize project before use

    @param task_id: id for task
    @param rtype: type of resources to get
    @param filter_by: filter by specific string
    """
    result = router_utils.get_resource_name(task_id=task_id, rtype=rtype, filter_str=filter_by)
    return result


@app.post("/upload")
async def upload_file(task_id: str, rtype: ResourcesType, file: UploadFile) -> ReturnDict:
    """
    update resources to rtype

    @param task_id: id for task
    @param rtype: resource type
    @param file: file steam
    """
    return router_utils.upload_file(task_id=task_id, rtype=rtype, file=file)


@app.post("/get_base")
async def get_base_dir(task_id: str) -> ReturnDict:
    """
    get the base directory of the project

    """
    return router_utils.get_base_dir(task_id=task_id)


@app.post("/remove_task")
async def remove_task(task_id: str) -> ReturnDict:
    """
    remove task by task id

    """
    return router_utils.remove_task(task_id=task_id)


@app.get("/resources/{item_cat}/{rtype}")
async def get_resources(task_id: str, rtype: ResourcesType, item_name: str):
    """
    get resources file

    @param task_id: if for task
    @param rtype: resource type
    @param item_name: resource name
    """
    resource_at = router_utils.get_resources(task_id=task_id, item_cat=rtype, item_name=item_name)
    if resource_at == "":
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return FileResponse(resource_at)
