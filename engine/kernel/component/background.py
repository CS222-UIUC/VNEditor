"""
background component for frame
"""
from .image import Image


class Background(Image):
    """
    background component in frame

    """

    def __init__(
        self, res_name: str, x: float = 0, y: float = 0, size: float = 0, **kwargs
    ):
        """
        constructor for background

        @param res_name: the direction of background file, relative address
        @param x: coordinate x
        @param y: coordinate y
        @param size: size of the background

        """
        super().__init__(x=x, y=y, size=size)
        self.res_name = res_name
