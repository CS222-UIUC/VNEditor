import time
import secrets

from functools import wraps

from module.project_manager import ProjectManager
from module.config_manager import ConfigLoader
from utils.exception import ControllerException
from utils.status import StatusCode
from utils.file_utils import get_folders_in_folder, check_folder_valid

from engine.engine import Engine
from utils.return_type import ReturnList, ReturnDict, ReturnStatus


class Task:
    """
    single task structure

    """

    def __init__(
        self, project_manager: ProjectManager, project_engine: Engine, base_dir: str
    ):
        self.project_manager: ProjectManager = project_manager
        self.project_engine: Engine = project_engine
        self.time_start: float = time.time()
        self.base_dir: str = base_dir


def project_controller_exception_handler(func):
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


class ProjectController:
    """
    class for router service

    """

    def __init__(self, config_dir: str):
        """
        constructor for router class

        """
        config_loader = ConfigLoader(config_dir=config_dir)
        self.__config_dir = config_dir
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

        project_manager = ProjectManager(
            base_dir=base_dir, config_dir=self.__config_dir
        )
        project_engine = Engine(
            project_dir=project_manager.get_project_dir(), config_dir=self.__config_dir
        )
        self.__tasks[token] = Task(
            project_manager=project_manager,
            project_engine=project_engine,
            base_dir=base_dir,
        )
        return token

    @project_controller_exception_handler
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

    @project_controller_exception_handler
    def get_project_dir(self, task_id: str) -> ReturnDict:
        """
        get the project directory

        @param task_id: id for task
        @return: diction contain status information

        """
        if task_id not in self.__tasks:
            raise ControllerException(f"cannot find task id '{task_id}'")

        project_manager = self.__tasks[task_id].project_manager
        to_return = {"base": project_manager.get_project_dir()}
        return ReturnDict(status=StatusCode.OK, content=to_return)

    @project_controller_exception_handler
    def remove_task(self, task_id: str) -> ReturnDict:
        """
        remove the task from task list

        @param task_id: if for task
        @return: diction contain status information

        """
        if task_id not in self.__tasks:
            raise ControllerException(f"cannot find task id '{task_id}'")

        task_last_time = time.time() - self.__tasks[task_id].time_start
        self.__tasks.pop(task_id)
        return ReturnDict(
            status=StatusCode.OK,
            content={"task_id": task_id, "time_last": task_last_time},
        )

    @project_controller_exception_handler
    def list_projects(self) -> ReturnList:
        """
        list all projects

        @return: list contain projects information
        """
        project_base = self.__project_config["projects_base"]
        if check_folder_valid(project_base):
            project_dirs = get_folders_in_folder(project_base)
            return ReturnList(status=StatusCode.OK, content=project_dirs)

        raise ControllerException(
            f"project folder {project_base} not valid, check the ini file"
        )

    @project_controller_exception_handler
    def remove_project_dir(self, task_id: str) -> ReturnDict:
        """
        remove the project, include the whole directory

        @param task_id: id for task
        @return: dictionary contain status information

        """
        if task_id not in self.__tasks:
            raise ControllerException(f"cannot find task id '{task_id}'")

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

        raise ControllerException(f"remove project id:{task_id} fails")

    def check_task_exist(self, task_id: str) -> bool:
        """
        check if the given task id in the current progress, for most situation,
        router utils can handle task checking process automatically,
        THIS FUNCTION SHOULD NOT ALWAYS USE!!!

        @param task_id: task id to check
        @return: bool indicator

        """
        return task_id in self.__tasks

    def get_task(self, task_id: str):
        """
        return the task corresponded to the task id,
        return None if not find

        @param task_id: id for task
        @return: corresponding task

        """
        if not self.check_task_exist(task_id):
            return None

        return self.__tasks[task_id]
