"""
character component for frame
"""
from .image import Image
from typing import Optional


class Character(Image):
    """
    character component in frame

    """

    def __init__(
        self,
        res_name: Optional[str],
        x: float = 0,
        y: float = 0,
        size: float = 0,
        **kwargs
    ):
        """
        constructor for character

        @param res_name: character file name, if leave none, default is voice over
        @param x: coordinate x
        @param y: coordinate y
        @param size: size of the background

        """
        super().__init__(x=x, y=y, size=size)
        self.res_name: str = res_name
