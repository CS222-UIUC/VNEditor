from service.utils import file_utils
from .ConfigManager import *

BACKGROUND_CAT = 'background_dir'
CHARACTER_CAT = 'character_dir'
MUSIC_CAT = 'music_dir'


class projectManager:
    def __init__(self, base: str):
        """
        constructor for project manager
        :param base: the base direction of the project
        """
        if not file_utils.check_folder_valid(base):
            os.mkdir(base)

        self.base = base
        config = Loader(Loader.DEFAULT_CONFIG_DIR)
        self.config_res = config.resources()

        for i in config.resources().keys():
            res_path_abs = os.path.join(base, config.resources()[i])
            os.mkdir(res_path_abs)
            self.config_res[i] = res_path_abs

    def __get_general_res(self, cat: str, filter_by: str = '') -> list:
        """
        helper for get all resources under specific category
        :param filter_by: fetch resources which contain filter string
        :param cat: specified category
        :return: get all resources in specified category
        """
        res = file_utils.get_all_in_folder(self.config_res[cat])
        if not len(filter_by):
            return res

    def __delete_general_res(self, cat: str, file_dir: str) -> bool:
        """
        helper for remove file under specific category
        :param cat: specified category
        :param file_dir: which file to delete, relative path
        :return: ok or not
        """
        file_dir_abs = os.path.join(self.base, os.path.join(cat, file_dir))
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

    def delete_backgrounds_res(self, file_dir: str) -> bool:
        """
        :param file_dir: fetch resources which contain filter string
        :return: get all background resources
        """
        return self.__delete_general_res(BACKGROUND_CAT, file_dir)

    def delete_music_res(self, file_dir: str) -> bool:
        """
        :param file_dir: fetch resources which contain filter string
        :return: get all background resources
        """
        return self.__delete_general_res(MUSIC_CAT, file_dir)

    def delete_character_res(self, file_dir: str) -> bool:
        """
        :param file_dir: fetch resources which contain filter string
        :return: get all background resources
        """
        return self.__delete_general_res(CHARACTER_CAT, file_dir)
