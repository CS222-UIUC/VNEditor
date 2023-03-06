"""
some unofficial testcase
"""
import traceback

from module import gameslot, project_manager
import random
from utils import file_utils


def engine_exception_handler(func):
    """
    exception decorator for engine

    @param func: function to be decorated
    @return:
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("Engine Error: ", str(e))
            return -1

    return wrapper


@engine_exception_handler
def foo():
    return 1 / 0


c = foo()
print(c)
