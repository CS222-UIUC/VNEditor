"""
Image class, define some image attribute

"""
from pydantic import BaseModel


class Image:
    """
    coordinate of visual novel component

    """

    def __init__(self, x: float = 0, y: float = 0, width: float = 0, height: float = 0):
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height


class ImageModel(BaseModel):
    """
    define the base model for image

    """

    x: float
    y: float
    width: float
    height: float
