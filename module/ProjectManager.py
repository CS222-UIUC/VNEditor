import os.path

from utils import file_utils
from .ConfigManager import *

BACKGROUND_CAT = 'background_dir'
CHARACTER_CAT = 'character_dir'
MUSIC_CAT = 'music_dir'


def delete_project(folder_dir: str) -> bool:
    """
    :param folder_dir: project direction to be delete
    :return: status of delete action
    """
    if not file_utils.check_folder_valid(folder_dir):
        return False

    return file_utils.delete_folder(folder_dir=folder_dir)


class projectManager:
    def __init__(self, base_dir: str, config_dir: str):
        """
        constructor for project manager

        :param base_dir: the base direction of the project
        :param config_dir: direction of config
        """
        if not file_utils.check_folder_valid(base_dir):
            os.makedirs(base_dir)

        self.__base = base_dir
        config = Loader(config_dir)
        self.__config_res = config.resources()

        for i in config.resources().keys():
            res_path_abs = os.path.join(base_dir, config.resources()[i])
            if not file_utils.check_folder_valid(res_path_abs):
                os.makedirs(res_path_abs)
            self.__config_res[i] = res_path_abs

    def __get_general_res(self, cat: str, filter_by: str = '') -> list:
        """
        helper for get all resources under specific category
        :param filter_by: fetch resources which contain filter string
        :param cat: specified category
        :return: get all resources in specified category
        """
        file_dir_abs = os.path.join(self.__base, self.__config_res[cat])
        res = file_utils.get_all_in_folder(file_dir_abs)
        if not len(filter_by):
            return res

    def __delete_general_res(self, cat: str, file_dir: str) -> bool:
        """
        helper for remove file under specific category
        :param cat: specified category
        :param file_dir: which file to delete, relative path
        :return: ok or not
        """
        file_dir_abs = os.path.join(self.__base, os.path.join(cat, file_dir))
        if not file_utils.check_file_valid(file_dir_abs):
            return False

        return file_utils.delete_file(file_dir_abs)

    def get_backgrounds_res(self, filter_by='') -> list:
        """
        :param filter_by: fetch resources which contain filter string
        :return: get all background resources
        """
        return self.__get_general_res(BACKGROUND_CAT, filter_by)

    def get_music_res(self, filter_by='') -> list:
        """
        :param filter_by: fetch resources which contain filter string
        :return: get all background resources
        """
        return self.__get_general_res(MUSIC_CAT, filter_by)

    def get_character_res(self, filter_by='') -> list:
        """
        :param filter_by: fetch resources which contain filter string
        :return: get all background resources
        """
        return self.__get_general_res(CHARACTER_CAT, filter_by)

    def delete_backgrounds_res(self, filer_dir: str) -> bool:
        """
        :param filer_dir: fetch resources which contain filter string
        :return: get all background resources
        """
        return self.__delete_general_res(BACKGROUND_CAT, filer_dir)

    def delete_music_res(self, filer_dir: str) -> bool:
        """
        :param filer_dir: fetch resources which contain filter string
        :return: get all background resources
        """
        return self.__delete_general_res(MUSIC_CAT, filer_dir)

    def delete_character_res(self, filer_dir: str) -> bool:
        """
        :param filer_dir: fetch resources which contain filter string
        :return: get all background resources
        """
        return self.__delete_general_res(CHARACTER_CAT, filer_dir)

    def delete(self) -> bool:
        """
        delete the whole project
        :return: status of delete action
        """
        return delete_project(self.__base)
