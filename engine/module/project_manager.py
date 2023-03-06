"""
Manage Project, provide service to manage project, include add, remove, edit
"""

import os.path

from module.exception import ProjectManagerError
from utils import file_utils
from .config_manager import ConfigLoader

BACKGROUND_CAT = "background_dir"
CHARACTER_CAT = "character_dir"
MUSIC_CAT = "music_dir"


def delete_project(folder_dir: str) -> bool:
    """
    @param folder_dir: project directory to be deleted
    @return: status of delete action
    """
    if not file_utils.check_folder_valid(folder_dir):
        return False

    return file_utils.delete_folder(folder_dir=folder_dir)


def init_check(func):
    """
    check if project has been initialized

    @return:
    """

    def wrapper(*args, **kwargs):
        if not args[0].is_init:
            raise ProjectManagerError("used before initialized project")
        else:
            return func(*args, **kwargs)

    return wrapper


class ProjectManager:
    """
    project manager class
    """

    def __init__(self):
        self.__config_res = None
        self.__base = None
        self.is_init = False

    def init_project(self, base_dir: str, config_dir: str):
        """
        constructor for project manager

        @param base_dir: the base directory of the project
        @param config_dir: directory of config
        """
        if not file_utils.check_folder_valid(base_dir):
            os.makedirs(base_dir)

        self.__base = base_dir
        config = ConfigLoader(config_dir)
        self.__config_res = config.resources()

        for i in config.resources().keys():
            res_path_abs = os.path.join(base_dir, config.resources()[i])
            if not file_utils.check_folder_valid(res_path_abs):
                os.makedirs(res_path_abs)
            self.__config_res[i] = res_path_abs
        self.is_init = True

    @init_check
    def __get_general_res(self, cat: str, filter_by: str = "") -> list:
        """
        helper for get all resources under specific category

        @param filter_by: fetch resources which contain filter string
        @param cat: specified category
        @return: get all resources in specified category
        """
        res = file_utils.get_all_in_folder(self.__config_res[cat])
        if len(filter_by) != 0:
            return [i for i in res if filter_by in i]
        return res

    @init_check
    def __delete_general_res(self, cat: str, file_dir: str) -> bool:
        """
        helper for remove file under specific category

        @param cat: specified category
        @param file_dir: which file to delete, relative path
        @return: ok or not
        """
        if not file_utils.check_file_valid(self.__config_res[cat]):
            return False
        return file_utils.delete_file(self.__config_res[cat])

    @init_check
    def delete(self) -> bool:
        """
        delete the whole project

        @return: status of delete action
        """
        return delete_project(self.__base)

    def get_backgrounds_res(self, filter_by="") -> list:
        """
        @param filter_by: fetch resources which contain filter string
        @return: get all background resources
        """
        return self.__get_general_res(BACKGROUND_CAT, filter_by)

    def get_music_res(self, filter_by="") -> list:
        """
        @param filter_by: fetch resources which contain filter string
        @return: get all background resources
        """
        return self.__get_general_res(MUSIC_CAT, filter_by)

    def get_character_res(self, filter_by="") -> list:
        """
        @param filter_by: fetch resources which contain filter string
        @return: get all background resources
        """
        return self.__get_general_res(CHARACTER_CAT, filter_by)

    def delete_backgrounds_res(self, filer_dir: str) -> bool:
        """
        @param filer_dir: fetch resources which contain filter string
        @return: get all background resources
        """
        return self.__delete_general_res(BACKGROUND_CAT, filer_dir)

    def delete_music_res(self, filer_dir: str) -> bool:
        """
        @param filer_dir: fetch resources which contain filter string
        @return: get all background resources
        """
        return self.__delete_general_res(MUSIC_CAT, filer_dir)

    def delete_character_res(self, filer_dir: str) -> bool:
        """
        @param filer_dir: fetch resources which contain filter string
        @return: get all background resources
        """
        return self.__delete_general_res(CHARACTER_CAT, filer_dir)
