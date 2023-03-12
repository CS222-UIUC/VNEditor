"""
router service main entry
"""

import os
import time
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import FileResponse
import secrets

from module.project_manager import ProjectManager, ResourcesType
from module.config_manager import ConfigLoader
from module.exception import RouterError
from utils.args_utils import STATUS
from utils.file_utils import check_file_valid, get_folders_in_folder, check_folder_valid

CONFIG_DIR = "./service.ini"


class ReturnStatus(BaseModel):
    status: STATUS = STATUS.FAIL
    msg: Optional[str]


class ReturnList(ReturnStatus):
    content: Optional[list]


class ReturnDict(ReturnStatus):
    content: Optional[dict]


class Task:
    project_manager: ProjectManager
    time_start: time
    base_dir: str

    def __init__(self, project_manager: ProjectManager, base_dir: str):
        self.project_manager = project_manager
        self.time_start = time.time()
        self.base_dir = base_dir


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
        self.cors_info: dict = config_loader.cors()

        self.__tasks: dict[str, Task] = {}

    def __new_task(self, base_dir: str) -> str:
        base_dir = base_dir.lower()
        for task_id, task in self.__tasks.items():
            if task.base_dir == base_dir:
                return task_id

        token = secrets.token_urlsafe(16)
        while token in self.__tasks:
            token = secrets.token_urlsafe(16)

        project_manager = ProjectManager()
        project_manager.init_project(base_dir=base_dir, config_dir=CONFIG_DIR)
        self.__tasks[token] = Task(project_manager=project_manager, base_dir=base_dir)
        return token

    @router_exception_handler
    def init_project(self, base_dir: str) -> ReturnDict:
        """
        initialize project

        @param base_dir: project directory
        @return: status code
        """
        task_id = self.__new_task(base_dir)
        return ReturnDict(
            status=STATUS.OK,
            msg=f"successfully initialize project in '{base_dir}'",
            content={"task_id": task_id},
        )

    @router_exception_handler
    def get_resource_name(
        self, task_id: str, rtype: ResourcesType, filter_str: str = ""
    ) -> ReturnList:
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
        resources = project_manager.get_resources_by_rtype(
            rtype=rtype, filter_by=filter_str
        )
        return ReturnList(status=STATUS.OK, msg="ok", content=resources)

    # @router_exception_handler
    @router_exception_handler
    def upload_file(
        self, task_id: str, rtype: ResourcesType, file: UploadFile
    ) -> ReturnDict:
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager

        max_file_size = int(self.__resources_config["max_size"])
        suffix = os.path.splitext(file.filename)[-1].lower()
        to_path = project_manager.get_dir_by_rtype(rtype)

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
        return ReturnDict(
            status=STATUS.OK, content={"task_id": task_id, "time_last": task_last_time}
        )

    @router_exception_handler
    def get_resources(
        self, task_id: str, rtype: ResourcesType, item_name: str
    ) -> ReturnList:
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        resource_dir = project_manager.get_dir_by_rtype(rtype)
        resources_at = os.path.join(resource_dir, item_name)

        if check_file_valid(resources_at):
            return ReturnList(status=STATUS.OK, msg="ok", content=[resources_at])
        else:
            return ReturnList(
                status=STATUS.FAIL,
                msg=f"fail to get resources because file '{resources_at}' is not valid",
            )

    @router_exception_handler
    def remove_resource(
        self, task_id: str, rtype: ResourcesType, item_name: str
    ) -> ReturnStatus:
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        status = project_manager.delete_resources_by_rtype(
            rtype=rtype, file_name=item_name
        )
        if not status:
            raise RouterError(f"item {item_name} cannot find in category {rtype}")

        return ReturnDict(status=STATUS.OK, msg="ok", content=[item_name])

    @router_exception_handler
    def rename_resource(
        self, task_id: str, rtype: ResourcesType, item_name: str, new_name: str
    ) -> ReturnDict:
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        status = project_manager.rename_resources_by_rtype(
            rtype=rtype, file_name=item_name, new_name=new_name
        )
        if not status:
            raise RouterError(f"item {item_name} cannot find in category {rtype}")

        return ReturnDict(
            status=STATUS.OK, msg="ok", content={"old": item_name, "new": new_name}
        )

    @router_exception_handler
    def list_projects(self) -> ReturnList:
        project_base = self.__project_config["projects_base"]
        if check_folder_valid(project_base):
            project_dirs = get_folders_in_folder(project_base)
            return ReturnList(status=STATUS.OK, content=project_dirs)
        else:
            raise RouterError(
                f"project folder {project_base} not valid, check the ini file"
            )

    @router_exception_handler
    def remove_project(self, task_id: str) -> ReturnDict:
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        status = project_manager.delete_project()

        if status:
            task_last_time = time.time() - self.__tasks[task_id].time_start
            self.__tasks.pop(task_id)
            return ReturnDict(
                status=STATUS.OK,
                msg="ok",
                content={"task_id": task_id, "time_last": task_last_time},
            )
        else:
            raise RouterError(f"remove project id:{task_id} fails")

    def check_task_exist(self, task_id: str) -> bool:
        """
        check if the given task id in the current progress, for most situation, router utils can handle
        task checking process automatically, THIS FUNCTION SHOULD NOT ALWAYS USE!!!

        @param task_id: task id to check
        @return: bool indicator
        """
        return task_id in self.__tasks


router_utils = RouterUtils()
origins = router_utils.cors_info["origins"].split(",")

app = FastAPI(
    title=router_utils.version_info["name"],
    description=router_utils.version_info["description"],
    version=router_utils.version_info["version"],
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/init_project", tags=["project"])
async def initialize_project(base_dir: str) -> ReturnDict:
    """
    initialize project, create new if given directory not exist

    @param base_dir: where is the project
    """
    result = router_utils.init_project(base_dir=base_dir)
    return result


@app.post("/get_res", tags=["resources"])
async def get_resources_name(
    task_id: str, rtype: ResourcesType, filter_by: str = ""
) -> ReturnList:
    """
    get background resources, need to initialize project before use

    @param task_id: id for task
    @param rtype: type of resources to get
    @param filter_by: filter by specific string
    """
    result = router_utils.get_resource_name(
        task_id=task_id, rtype=rtype, filter_str=filter_by
    )
    return result


@app.post("/remove_res", tags=["resources"])
async def remove_project(
    task_id: str, rtype: ResourcesType, item_name: str
) -> ReturnStatus:
    """
    remove resources by resources name

    @param item_name: resource to be removed (name not directory)
    @param rtype: resource type
    @param task_id: id for task
    """

    return router_utils.remove_resource(
        task_id=task_id, rtype=rtype, item_name=item_name
    )


@app.post("/rename_res", tags=["resources"])
async def rename_project(
    task_id: str, rtype: ResourcesType, item_name: str, new_name: str
) -> ReturnDict:
    """
    rename resources by resources name

    @param new_name: new name for item
    @param item_name: resource to be renamed (name not directory)
    @param rtype: resource type
    @param task_id: id for task
    """

    return router_utils.rename_resource(
        task_id=task_id, rtype=rtype, item_name=item_name, new_name=new_name
    )


@app.post("/upload", tags=["resources"])
async def upload_file(
    task_id: str, rtype: ResourcesType, file: UploadFile
) -> ReturnDict:
    """
    update resources to rtype

    @param task_id: id for task
    @param rtype: resource type
    @param file: file steam
    """
    return router_utils.upload_file(task_id=task_id, rtype=rtype, file=file)


@app.post("/upload_files", tags=["resources"])
async def upload_files(
    task_id: str, rtype: ResourcesType, files: list[UploadFile]
) -> ReturnList:
    """
    update multi resources to rtype

    @param task_id: id for task
    @param rtype: resource type
    @param files: files steam
    """
    to_return = []
    status: STATUS = STATUS.FAIL  # at least one mission succeed

    if router_utils.check_task_exist(task_id):
        for file in files:
            mission_status = router_utils.upload_file(
                task_id=task_id, rtype=rtype, file=file
            )
            if mission_status.status == STATUS.OK:
                status = STATUS.OK
            to_return.append(mission_status)

    if status == STATUS.FAIL:
        msg = "fail to upload files"
    else:
        msg = "ok"

    return ReturnList(status=status, msg=msg, content=to_return)


@app.post("/get_base", tags=["project"])
async def get_base_dir(task_id: str) -> ReturnDict:
    """
    get the base directory of the project

    """
    return router_utils.get_base_dir(task_id=task_id)


@app.post("/remove_task", tags=["project"])
async def remove_task(task_id: str) -> ReturnDict:
    """
    remove task by task id

    """
    return router_utils.remove_task(task_id=task_id)


@app.get("/resources/{rtype}/{item_name}", tags=["resources"])
async def get_resources(
    task_id: str, rtype: ResourcesType, item_name: str
) -> FileResponse:
    """
    get resources file

    @param task_id: if for task
    @param rtype: resource type
    @param item_name: resource name
    """
    resource_at = router_utils.get_resources(
        task_id=task_id, rtype=rtype, item_name=item_name
    )
    if resource_at.status == STATUS.FAIL:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return FileResponse(resource_at.content[0])


@app.post("/list_projects", tags=["project"])
async def list_project() -> ReturnList:
    """
    list all projects

    """
    return router_utils.list_projects()


@app.post("/remove_project", tags=["project"])
async def remove_project(task_id: str) -> ReturnDict:
    """
    remove the project

    @param task_id: if for task
    """
    return router_utils.remove_project(task_id=task_id)
