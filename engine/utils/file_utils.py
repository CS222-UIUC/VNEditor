import os
import shutil

"""
utils for checking files validation and get file path etc.
"""


def check_file_valid(file_dir: str) -> bool:
    """
    check if thr given file is valid or not

    :param file_dir: path of files
    :return: if the given file is valid or not
    """
    return os.path.isfile(file_dir)


def check_folder_valid(folder_dir: str) -> bool:
    """
    check if thr given folder is valid or not

    :param folder_dir: path of dictionary
    :return: if the given folder is valid or not
    """
    return os.path.isdir(folder_dir)


def get_files_in_folder(folder_dir: str, suffix: str = "") -> list:
    """
    get all files in folder

    :param folder_dir: folder direction
    :param suffix: filter by suffix of files
    :return: the list of files under folder
    """
    files = get_all_in_folder(folder_dir)
    if not len(files):
        files = [f for f in files if os.path.isfile(folder_dir + "/" + f)]
        if not len(suffix):
            files = [f for f in files if get_ext(f) == "." + suffix]
    return files


def get_all_in_folder(folder_dir: str) -> list:
    """
    get all files and folder in given folder

    :param folder_dir: folder direction
    :return: the list of file and dictionary under folder
    """
    if check_folder_valid(folder_dir):
        files = os.listdir(folder_dir)
        return files
    return []


def get_folder_dir(file_dir: str) -> str:
    """
    get folder direction with given file direction, regardless validation of given file

    :param file_dir: path of file
    :return: return the given folder with given file direction
    """
    return "".join(file_dir.split("\\")[:-1])


def get_ext(file_dir: str) -> str:
    """
    get extension for give file

    :param file_dir: path of file
    :return: extension for file, regardless validation of file
    """
    return os.path.splitext(file_dir)[1]


def delete_file(file_dir: str) -> bool:
    """
    delete given file

    :param file_dir: path of file
    :return: ok or not
    """
    if not check_file_valid(file_dir):
        return False

    try:
        os.remove(file_dir)
    except OSError:
        return False
    return True


def delete_folder(folder_dir: str) -> bool:
    """
    delete give folder and remove all files and folder inside

    :param folder_dir: path of folder
    :return: ok or not
    """
    if not check_folder_valid(folder_dir):
        return False

    try:
        shutil.rmtree(folder_dir)
    except OSError:
        return False
    return True
