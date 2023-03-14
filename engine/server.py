"""
router service main entry
"""

import os
import time
import secrets

from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from module.project_manager import ProjectManager, ResourcesType
from module.config_manager import ConfigLoader
from module.exception import RouterError
from utils.status import StatusCode
from utils.file_utils import check_file_valid, get_folders_in_folder, check_folder_valid

CONFIG_DIR = "./service.ini"


class ReturnStatus(BaseModel):
    """
    define of return status base model

    """

    status: StatusCode = StatusCode.FAIL
    msg: Optional[str]


class ReturnList(ReturnStatus):
    """
    define of return list base model

    """

    content: Optional[list]


class ReturnDict(ReturnStatus):
    """
    define of return dictionary base model

    """

    content: Optional[dict]


class Task:
    """
    single task structure

    """

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
            return ReturnStatus(status=StatusCode.FAIL, msg=str(e_msg))

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
        """
        generate a new task, called when initial a new project

        @param base_dir: base directory of the project
        @return: task token

        """
        base_dir = base_dir.lower()
        for task_id, task in self.__tasks.items():
            if task.base_dir == base_dir:
                return task_id

        token_length = int(self.__project_config["token_length"])
        token = secrets.token_urlsafe(token_length)
        while token in self.__tasks:
            token = secrets.token_urlsafe(token_length)

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
            status=StatusCode.OK,
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
        return ReturnList(status=StatusCode.OK, msg="ok", content=resources)

    # @router_exception_handler
    @router_exception_handler
    def upload_file(
        self, task_id: str, rtype: ResourcesType, file: UploadFile
    ) -> ReturnDict:
        """
        upload a single file into the rtype directory

        @param task_id: id for task
        @param rtype: resources type
        @param file: file to be uploaded
        @return: diction contain upload file information

        """
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager

        max_file_size = int(self.__resources_config["max_size"])
        suffix = os.path.splitext(file.filename)[-1].lower()
        to_path = project_manager.get_dir_by_rtype(rtype)

        if to_path == "":
            raise RouterError(f"no such rtype: {rtype}")

        if rtype is ResourcesType.Background:
            if suffix not in self.__resources_config["background_support"].split(","):
                raise RouterError(f"file type '{suffix}' not support")

        elif rtype is ResourcesType.Music:
            if suffix not in self.__resources_config["music_support"].split(","):
                raise RouterError(f"file type '{suffix}' not support")

        elif rtype is ResourcesType.Character:
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
            raise RouterError(
                f"cannot write file {file.filename} due to {str(e)}"
            ) from e
        finally:
            file.file.close()

        to_return = {"filename": file.filename, "directory": to_path, "size": file_size}
        return ReturnDict(status=StatusCode.OK, msg="ok", content=to_return)

    @router_exception_handler
    def get_base_dir(self, task_id: str) -> ReturnDict:
        """
        get the base directory of the project

        @param task_id: id for task
        @return: diction contain status information

        """
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        to_return = {"base": project_manager.get_base_dir()}
        return ReturnDict(status=StatusCode.OK, content=to_return)

    @router_exception_handler
    def remove_task(self, task_id: str) -> ReturnDict:
        """
        remove the task from task list

        @param task_id: if for task
        @return: diction contain status information

        """
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        task_last_time = time.time() - self.__tasks[task_id].time_start
        self.__tasks.pop(task_id)
        return ReturnDict(
            status=StatusCode.OK,
            content={"task_id": task_id, "time_last": task_last_time},
        )

    @router_exception_handler
    def get_resources(
        self, task_id: str, rtype: ResourcesType, item_name: str
    ) -> ReturnList:
        """
        get the resources absolute address

        @param task_id: id for task
        @param rtype: resource type
        @param item_name: resource name
        @return: list contain status information

        """
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        resource_dir = project_manager.get_dir_by_rtype(rtype)
        resources_at = os.path.join(resource_dir, item_name)

        if check_file_valid(resources_at):
            return ReturnList(status=StatusCode.OK, msg="ok", content=[resources_at])

        return ReturnList(
            status=StatusCode.FAIL,
            msg=f"fail to get resources because file '{resources_at}' is not valid",
        )

    @router_exception_handler
    def remove_resource(
        self, task_id: str, rtype: ResourcesType, item_name: str
    ) -> ReturnList:
        """
        remove resources

        @param task_id: id for task
        @param rtype: resources type
        @param item_name: resource name
        @return: list contain status information

        """
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        status = project_manager.delete_resources_by_rtype(
            rtype=rtype, file_name=item_name
        )
        if not status:
            raise RouterError(f"item {item_name} cannot find in category {rtype}")

        return ReturnList(status=StatusCode.OK, msg="ok", content=[item_name])

    @router_exception_handler
    def rename_resource(
        self, task_id: str, rtype: ResourcesType, item_name: str, new_name: str
    ) -> ReturnDict:
        """
        rename the resource

        @param task_id: id for task
        @param rtype: resources type
        @param item_name: resource name
        @param new_name: new name
        @return: dictionary contain status information

        """
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        status = project_manager.rename_resources_by_rtype(
            rtype=rtype, file_name=item_name, new_name=new_name
        )
        if not status:
            raise RouterError(f"item {item_name} cannot find in category {rtype}")

        return ReturnDict(
            status=StatusCode.OK, msg="ok", content={"old": item_name, "new": new_name}
        )

    @router_exception_handler
    def list_projects(self) -> ReturnList:
        """
        list all projects

        @return: list contain projects information
        """
        project_base = self.__project_config["projects_base"]
        if check_folder_valid(project_base):
            project_dirs = get_folders_in_folder(project_base)
            return ReturnList(status=StatusCode.OK, content=project_dirs)

        raise RouterError(
            f"project folder {project_base} not valid, check the ini file"
        )

    @router_exception_handler
    def remove_project_dir(self, task_id: str) -> ReturnDict:
        """
        remove the project, include the whole directory

        @param task_id: id for task
        @return: dictionary contain status information

        """
        if task_id not in self.__tasks:
            raise RouterError(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        status = project_manager.delete_project()

        if status:
            task_last_time = time.time() - self.__tasks[task_id].time_start
            self.__tasks.pop(task_id)
            return ReturnDict(
                status=StatusCode.OK,
                msg="ok",
                content={"task_id": task_id, "time_last": task_last_time},
            )

        raise RouterError(f"remove project id:{task_id} fails")

    def check_task_exist(self, task_id: str) -> bool:
        """
        check if the given task id in the current progress, for most situation,
        router utils can handle task checking process automatically,
        THIS FUNCTION SHOULD NOT ALWAYS USE!!!

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

with open("static/ascii_logo", "r", encoding="UTF-8") as f_stream:
    print("\n", f_stream.read())
    print(
        "\n"
        f"{router_utils.version_info['name']}\n"
        f"Version: {router_utils.version_info['version']}\n"
    )


@app.get("/", include_in_schema=False)
async def read_index():
    """
    server index page

    """
    return FileResponse("static/index.html")


@app.get("/ok_image", include_in_schema=False)
async def ok_image():
    """
    server index page image

    """
    return FileResponse("static/ok.webp")


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
async def remove_resource(
    task_id: str, rtype: ResourcesType, item_name: str
) -> ReturnList:
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
    status: StatusCode = StatusCode.FAIL  # at least one mission succeed

    if router_utils.check_task_exist(task_id):
        for file in files:
            mission_status = router_utils.upload_file(
                task_id=task_id, rtype=rtype, file=file
            )
            if mission_status.status == StatusCode.OK:
                status = StatusCode.OK
            to_return.append(mission_status)

    if status == StatusCode.FAIL:
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
    if resource_at.status == StatusCode.FAIL:
        raise HTTPException(status_code=404, detail="Item not found")

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
    return router_utils.remove_project_dir(task_id=task_id)
