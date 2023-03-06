import configparser
from utils.file_utils import *
from .Exception import *


class Loader:
    """
    config loading helper
    """

    def __init__(self, config_dir: str):
        if check_file_valid(config_dir):
            self.config = configparser.ConfigParser()
            self.config.read(config_dir)
        else:
            raise ConfigLoaderError("cannot open config file")

    def game_memory(self) -> dict:
        """
        get game_memory config

        @return: game_memory config
        """
        return dict(self.config["GameMemory"])

    def engine(self) -> dict:
        """
        get engine config

        @return: engine config
        """
        return dict(self.config["Engine"])

    def log_file(self) -> dict:
        """
        get log_file config

        @return: log_file config
        """
        return dict(self.config["LogFile"])

    def resources(self) -> dict:
        """
        get resources config

        @return: resources config
        """
        return dict(self.config["Resources"])

    def register_service(self) -> dict:
        """
        get register_service config

        @return: register_service config
        """
        return dict(self.config["RegisterService"])

    def version(self) -> dict:
        """
        get version config

        @return: version config
        """
        return dict(self.config["Version"])

    def get_all_section(self) -> list:
        """
        get all sections in config file

        @return: all sections in config file
        """
        return list(self.config.sections())
