import os

from functools import wraps
from fastapi import UploadFile

from module.project_manager import ProjectManager, ResourcesType
from module.config_manager import ConfigLoader
from utils.exception import ControllerException
from utils.status import StatusCode
from utils.file_utils import check_file_valid

from utils.return_type import ReturnList, ReturnDict, ReturnStatus

from .project_controller import Task


def resource_controller_exception_handler(func):
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


class ResourceController:
    """
    class for router service

    """

    def __init__(self, config_dir: str):
        """
        constructor for router class

        """
        config_loader = ConfigLoader(config_dir=config_dir)
        self.__resources_config: dict = config_loader.resources()

    @resource_controller_exception_handler
    def get_resource_name(
            self,
            task: Task,
            rtype: ResourcesType,
            filter_str: str = "",
    ) -> ReturnList:
        """
        get resources name

        @param task: current task information
        @param rtype: type of resources to fetch
        @param filter_str: filter resources by a specific string
        @return: status code

        """
        project_manager = task.project_manager
        resources = project_manager.get_resources_by_rtype(
            rtype=rtype, filter_by=filter_str
        )
        return ReturnList(status=StatusCode.OK, msg="ok", content=resources)

    @resource_controller_exception_handler
    def upload_file(
            self, task: Task, rtype: ResourcesType, file: UploadFile
    ) -> ReturnDict:
        """
        upload a single file into the rtype directory

        @param task: current task information
        @param rtype: resources type
        @param file: file to be uploaded
        @return: diction contain upload file information

        """
        project_manager = task.project_manager
        max_file_size = int(self.__resources_config["max_size"])
        suffix = os.path.splitext(file.filename)[-1].lower()
        to_path = project_manager.get_dir_by_rtype(rtype)

        if to_path == "":
            raise ControllerException(f"no such rtype: {rtype}")

        if not self.__check_resource_suffix(rtype, suffix):
            raise ControllerException(
                f"resources {file.filename} cannot be uploaded due to suffix not support"
            )

        file_content = file.file.read()
        file_size = len(file_content)

        if len(file_content) > max_file_size:
            file.file.close()
            raise ControllerException(f"file excess max size {str(max_file_size)}")
        try:
            with open(os.path.join(to_path, file.filename), "wb") as f:
                f.write(file_content)
        except Exception as e:
            file.file.close()
            raise ControllerException(
                f"cannot write file {file.filename} due to {str(e)}"
            ) from e
        finally:
            file.file.close()

        to_return = {"filename": file.filename, "directory": to_path, "size": file_size}
        return ReturnDict(status=StatusCode.OK, msg="ok", content=to_return)

    @resource_controller_exception_handler
    def upload_files(
            self,
            task: Task,
            rtype: ResourcesType,
            files: list[UploadFile],
    ) -> ReturnList:
        """
        upload a lot of files

        @param task: current task information
        @param rtype: resources type
        @param files: file to be uploaded
        @return:
        """
        to_return = []
        status: StatusCode = StatusCode.FAIL  # at least one mission succeed
        project_manager = task.project_manager

        for file in files:
            mission_status = self.upload_file(
                project_manager=project_manager, rtype=rtype, file=file
            )
            if mission_status.status == StatusCode.OK:
                status = StatusCode.OK
            to_return.append(mission_status)

        if status == StatusCode.FAIL:
            msg = "fail to upload files"
        else:
            msg = "ok"

        return ReturnList(status=status, msg=msg, content=to_return)

    @resource_controller_exception_handler
    def get_resources(
            self, task: Task, rtype: ResourcesType, item_name: str
    ) -> ReturnList:
        """
        get the resources absolute address

        @param task: current task information
        @param rtype: resource type
        @param item_name: resource name
        @return: list contain status information

        """
        project_manager = task.project_manager
        resource_dir = project_manager.get_dir_by_rtype(rtype)
        resources_at = os.path.join(resource_dir, item_name)

        if check_file_valid(resources_at):
            return ReturnList(status=StatusCode.OK, msg="ok", content=[resources_at])

        return ReturnList(
            status=StatusCode.FAIL,
            msg=f"fail to get resources because file '{resources_at}' is not valid",
        )

    @resource_controller_exception_handler
    def remove_resource(
            self, task: Task, rtype: ResourcesType, item_name: str
    ) -> ReturnList:
        """
        remove resources

        @param task: current task information
        @param rtype: resources type
        @param item_name: resource name
        @return: list contain status information

        """
        project_manager = task.project_manager
        status = project_manager.delete_resources_by_rtype(
            rtype=rtype, file_name=item_name
        )
        if not status:
            raise ControllerException(
                f"item {item_name} cannot find in category {rtype}"
            )

        return ReturnList(status=StatusCode.OK, msg="ok", content=[item_name])

    @resource_controller_exception_handler
    def rename_resource(
            self,
            task: Task,
            rtype: ResourcesType,
            item_name: str,
            new_name: str,
    ) -> ReturnDict:
        """
        rename the resource

        @param task: current task information
        @param rtype: resources type
        @param item_name: resource name
        @param new_name: new name
        @return: dictionary contain status information

        """
        project_manager = task.project_manager
        status = project_manager.rename_resources_by_rtype(
            rtype=rtype, file_name=item_name, new_name=new_name
        )
        if not status:
            raise ControllerException(
                f"item {item_name} cannot find in category {rtype}"
            )

        return ReturnDict(
            status=StatusCode.OK, msg="ok", content={"old": item_name, "new": new_name}
        )

    def __check_resource_suffix(self, rtype: ResourcesType, suffix: str) -> bool:
        """
        check the suffix of the resources

        @param rtype: resource type
        @param suffix: suffix
        @return: check pass or not

        """
        if rtype is ResourcesType.Background:
            if suffix not in self.__resources_config["background_support"].split(","):
                return False

        elif rtype is ResourcesType.Music:
            if suffix not in self.__resources_config["music_support"].split(","):
                return False

        elif rtype is ResourcesType.Character:
            if suffix not in self.__resources_config["character_support"].split(","):
                return False
        else:
            return False

        return True
