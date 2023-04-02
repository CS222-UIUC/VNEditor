"""
router service main entry
"""
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from module.project_manager import ResourcesType
from utils.status import StatusCode
import engine

from controller.project_controller import ProjectController
from controller.resource_controller import ResourceController
from controller.server_controller import ServerController
from utils.return_type import ReturnList, ReturnDict, ReturnStatus

CONFIG_DIR = "./service.ini"

# register controllers
project_utils = ProjectController(config_dir=CONFIG_DIR)
resources_utils = ResourceController(config_dir=CONFIG_DIR)
server_utils = ServerController(config_dir=CONFIG_DIR)
# end register controllers

origins = project_utils.cors_info["origins"].split(",")

app = FastAPI(
    title=project_utils.version_info["name"],
    description=project_utils.version_info["description"],
    version=project_utils.version_info["version"],
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
        f"{project_utils.version_info['name']}\n"
        f"Version: {project_utils.version_info['version']}\n"
        f"{engine.engine.ENGINE_NAME}: {engine.engine.ENGINE_VERSION}\n"
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
    result = project_utils.init_project(base_dir=base_dir)
    return result


@app.post("/get_base", tags=["project"])
async def get_project_dir(task_id: str) -> ReturnDict:
    """
    get the project directory

    """
    return project_utils.get_project_dir(task_id=task_id)


@app.post("/remove_task", tags=["project"])
async def remove_task(task_id: str) -> ReturnDict:
    """
    remove task by task id

    """
    return project_utils.remove_task(task_id=task_id)


@app.post("/list_projects", tags=["project"])
async def list_project() -> ReturnList:
    """
    list all projects

    """
    return project_utils.list_projects()


@app.post("/remove_project_by_id", tags=["project"])
async def remove_project(task_id: str) -> ReturnDict:
    """
    remove the project

    @param task_id: if for task
    """
    return project_utils.remove_project_dir(task_id=task_id)


@app.post("/remove_project", tags=["project"])
async def remove_project(project_name: str) -> ReturnStatus:
    """
    remove the project

    @param project_name: the name of the project
    """
    return server_utils.delete_project(project_name=project_name)


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
    task = project_utils.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=400, detail="task id invalid")

    resource_at = resources_utils.get_resources(
        task=task, rtype=rtype, item_name=item_name
    )
    if resource_at.status == StatusCode.FAIL:
        raise HTTPException(status_code=404, detail="item not found")

    return FileResponse(resource_at.content[0])


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
    task = project_utils.get_task(task_id)
    if task is None:
        return ReturnList(status=StatusCode.FAIL, msg="no such task id")

    result = resources_utils.get_resource_name(
        task=task, rtype=rtype, filter_str=filter_by
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
    task = project_utils.get_task(task_id)
    if task is None:
        return ReturnList(status=StatusCode.FAIL, msg="no such task id")

    return resources_utils.remove_resource(
        task=task, rtype=rtype, item_name=item_name
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
    task = project_utils.get_task(task_id)
    if task is None:
        return ReturnDict(status=StatusCode.FAIL, msg="no such task id")

    return resources_utils.rename_resource(
        task=task,
        rtype=rtype,
        item_name=item_name,
        new_name=new_name,
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
    task = project_utils.get_task(task_id)
    if task is None:
        return ReturnDict(status=StatusCode.FAIL, msg="no such task id")

    return resources_utils.upload_file(
        task=task, rtype=rtype, file=file
    )


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
    task = project_utils.get_task(task_id)
    if task is None:
        return ReturnList(status=StatusCode.FAIL, msg="no such task id")

    return resources_utils.upload_files(
        task=task, rtype=rtype, files=files
    )
