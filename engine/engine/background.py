"""
background component for frame
"""


class Background:
    """
    background component in frame
    """

    def __init__(self, res_name: str):
        """
        constructor for background

        @param res_name: the direction of background file, relative address
        """
        self.res_name = res_name

    def get_background(self):
        """
        getter for background

        @return:
        """
        return self.res_name

    def set_background(self, res_name: str):
        """
        setter

        @param res_name: new resources name
        @return:
        """
        self.res_name = res_name
