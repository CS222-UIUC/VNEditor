from functools import wraps
from .return_type import ReturnStatus
from .status import StatusCode


def exception_handler(func, module_name: str = "default", debug=False):
    """
    exception decorator for router

    @param func: function to be decorated
    @param module_name: module name
    @param debug: if debug set to be true, error will directly throw instead of caught

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if debug:
                raise e
            e_msg = f"{module_name} ({type(e).__name__}): {str(e)}"
            print(e_msg)
            return ReturnStatus(status=StatusCode.FAIL, msg=e_msg)

    wrapper: func
    return wrapper
