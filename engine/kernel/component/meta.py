"""
frame meta data

"""


class FrameMeta:
    """
    metadata of the frame

    """

    def __init__(self, name: str = "default"):
        """
        constructor for meta, if not given, set to default

        @param name: name of current frame

        """
        self.name: str = name
