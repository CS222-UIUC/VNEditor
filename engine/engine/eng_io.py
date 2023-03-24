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
<<<<<<< HEAD
    with open(file_dir, 'rb') as file_stream:
=======
    with open(file_dir, "rb") as file_stream:
>>>>>>> 70dad1d15cfc57f95f402403263021528a40be31
        return pickle.load(file_stream)


def pickle_dumper(game_content_raw: list, file_dir: str):
    """
    define how to dump the game content into file stream

    @param game_content_raw: raw game content
    @param file_dir: the directory of file
    @return: ok or not

    """
<<<<<<< HEAD
    with open(file_dir, 'wb') as file_stream:
=======
    with open(file_dir, "wb") as file_stream:
>>>>>>> 70dad1d15cfc57f95f402403263021528a40be31
        pickle.dump(game_content_raw, file_stream)
