"""
IO for engine

"""

import pickle


def pickle_loader(file_dir: str):
    """
    define how to load the game content from file stream

    @param file_dir: the directory of file
    @return ok or not

    """
    with open(file_dir, 'rb') as file_stream:
        return pickle.load(file_stream)


def pickle_dumper(game_content_raw: list, file_dir: str):
    """
    define how to dump the game content into file stream

    @param game_content_raw: raw game content
    @param file_dir: the directory of file
    @return: ok or not

    """
    with open(file_dir, 'wb') as file_stream:
        pickle.dump(game_content_raw, file_stream)
