"""
frame meta data

"""


class FrameMeta:
    """
    metadata of the frame

    """

    def __init__(self, chapter: str = "default", name: str = "default"):
        """
        constructor for meta, if not given, set to default

        @param chapter: the chapter of this frame
        @param name: name of current frame

        """

        self.chapter: str = chapter
        self.name: str = name
