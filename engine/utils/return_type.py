from pydantic import BaseModel
from typing import Optional
from utils.status import StatusCode


class ReturnStatus(BaseModel):
    """
    define of return status base model

    """

    status: StatusCode = StatusCode.OK
    msg: Optional[str] = 'ok'


class ReturnList(ReturnStatus):
    """
    define of return list base model

    """

    content: Optional[list]


class ReturnDict(ReturnStatus):
    """
    define of return dictionary base model

    """

    content: Optional[dict]
