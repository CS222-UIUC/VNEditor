"""
frame meta data

"""


class FrameMeta:
    """
    metadata of the frame

    """

    def __init__(self, chapter: str = "default", description: str = ""):
        """
        constructor for meta

        @param chapter: the chapter of this frame
        @param description: description of current frame

        """
        if chapter == "":
            chapter = "default"

        self.chapter: str = chapter
        self.description: str = description
