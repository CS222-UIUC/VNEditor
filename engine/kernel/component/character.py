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
        width: float = 0,
        height: float = 0,
        **kwargs
    ):
        """
        constructor for character

        @param res_name: character file name, if leave none, default is voice over
        @param x: coordinate x
        @param y: coordinate y
        @param width: the width of the Character
        @param height: the height of the Character

        """
        super().__init__(x=x, y=y, width=width, height=height)
        self.res_name: str = res_name
