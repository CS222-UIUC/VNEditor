"""
Manage Project, provide service to manage project, include add, remove, edit
"""

import os.path
from enum import Enum
from module.exception import ProjectManagerError
from utils import file_utils
from .config_manager import ConfigLoader

BACKGROUND_CAT = "background_dir"
CHARACTER_CAT = "character_dir"
MUSIC_CAT = "music_dir"


class ResourcesType(str, Enum):
    """
    Resource Type Enumerator

    """

    Background = "background"
    Music = "music"
    Character = "character"


def delete_project(folder_dir: str) -> bool:
    """
    @param folder_dir: project directory to be deleted
    @return: status of delete action
    """
    if not file_utils.check_folder_valid(folder_dir):
        return False

    return file_utils.delete_folder(folder_dir=folder_dir)


class ProjectManager:
    """
    project manager class
    """

    def __init__(self, base_dir: str, config_dir: str):
        """
        constructor for project manager

        @param base_dir: the base directory of the project
        @param config_dir: directory of config
        """

        config = ConfigLoader(config_dir)
        self.__config_res = config.resources()
        project_base_dir = config.project()["projects_base"]
        self.__base = os.path.join(project_base_dir, base_dir)

        if not file_utils.check_folder_valid(self.__base):
            os.makedirs(self.__base)

        for i in ["background_dir", "music_dir", "character_dir"]:
            res_path_abs = os.path.join(self.__base, config.resources()[i])
            if not file_utils.check_folder_valid(res_path_abs):
                os.makedirs(res_path_abs)
            self.__config_res[i] = res_path_abs

    def __get_general_res(self, cat: str, filter_by: str = "") -> list:
        """
        helper for get all resources under specific category

        @param filter_by: fetch resources which contain filter string
        @param cat: specified category
        @return: get all resources in specified category
        """
        res = file_utils.get_files_in_folder(self.__config_res[cat])
        if len(filter_by) != 0:
            return [i for i in res if filter_by in i]
        return res

    def __delete_general_res(self, cat: str, res_name: str) -> bool:
        """
        helper for remove file under specific category

        @param cat: specified category
        @param res_name: resources name
        @return: ok or not
        """
        base = self.__config_res[cat]
        res_abs_dir = os.path.join(base, res_name)

        if not file_utils.check_file_valid(res_abs_dir):
            return False
        return file_utils.delete_file(res_abs_dir)

    def __rename_general_res(self, cat: str, res_name: str, new_name: str) -> bool:
        """
        helper for rename file under specific category

        @param cat: specified category
        @param res_name: resources name
        @return: ok or not
        """
        base = self.__config_res[cat]
        res_abs_dir = os.path.join(base, res_name)

        if not file_utils.check_file_valid(res_abs_dir):
            return False

        res_abs_dir = os.path.join(base, res_name)
        return file_utils.rename_file(file_dir=res_abs_dir, new_name=new_name)

    def delete_project(self) -> bool:
        """
        delete the whole project

        @return: status of delete action
        """
        return delete_project(self.__base)

    def get_resources_by_rtype(self, rtype: ResourcesType, filter_by="") -> list:
        """
        get the resources by resource type

        @param rtype: resource type
        @param filter_by: fetch resources which contain filter string
        @return: valid resources name

        """
        if rtype == ResourcesType.Background:
            return self.__get_general_res(BACKGROUND_CAT, filter_by)
        if rtype == ResourcesType.Music:
            return self.__get_general_res(MUSIC_CAT, filter_by)
        if rtype == ResourcesType.Character:
            return self.__get_general_res(CHARACTER_CAT, filter_by)

        raise ProjectManagerError(f"cannot find rtype: '{rtype}'")

    def delete_resources_by_rtype(self, rtype: ResourcesType, file_name: str) -> bool:
        """
        delete resources by resources type

        @param rtype: resources type
        @param file_name: file name
        @return: ok or not
        """
        if rtype == ResourcesType.Background:
            return self.__delete_general_res(BACKGROUND_CAT, file_name)
        if rtype == ResourcesType.Music:
            return self.__delete_general_res(MUSIC_CAT, file_name)
        if rtype == ResourcesType.Character:
            return self.__delete_general_res(CHARACTER_CAT, file_name)

        raise ProjectManagerError(f"cannot find rtype: '{rtype}'")

    def rename_resources_by_rtype(
        self, rtype: ResourcesType, file_name: str, new_name: str
    ) -> bool:
        """
        rename the resources by new_name

        @param rtype: resources type
        @param file_name: origin file name
        @param new_name: new file name
        @return: ok or not
        """
        if rtype == ResourcesType.Background:
            return self.__rename_general_res(BACKGROUND_CAT, file_name, new_name)
        if rtype == ResourcesType.Music:
            return self.__rename_general_res(MUSIC_CAT, file_name, new_name)
        if rtype == ResourcesType.Character:
            return self.__rename_general_res(CHARACTER_CAT, file_name, new_name)

        raise ProjectManagerError(f"cannot find rtype: '{rtype}'")

    def get_dir_by_rtype(self, rtype: str):
        """
        get the directory by resources type

        @param rtype: resources type
        @return: corresponding directory
        """
        if rtype is ResourcesType.Background:
            return self.__config_res[BACKGROUND_CAT]
        if rtype is ResourcesType.Music:
            return self.__config_res[MUSIC_CAT]
        if rtype is ResourcesType.Character:
            return self.__config_res[CHARACTER_CAT]

        raise ProjectManagerError(f"cannot find rtype: '{rtype}'")

    def get_project_dir(self) -> str:
        """
        get the base directory of current project

        @return: the base directory for the project
        """
        return self.__base
