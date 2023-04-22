"""
define the class for Chapter, which is a special frame

"""
from pydantic import BaseModel
from engine.frame import BasicFrame


class Chapter(BasicFrame):
    """
    Chapter class, use to classified frames

    """

    tail_fid: int = BasicFrame.VOID_FRAME_ID

    def __init__(self, fid: int, chapter_name: str):
        super().__init__(fid)
        self.chapter_name = chapter_name

    def set_tail_fid(self, fid: int):
        """
        set the tail fid

        @param fid: the frame id for tail
        """
        self.tail_fid = fid


class ChapterModel(BaseModel):
    """
    class for base model for Chapter class

    """

    chapter_name: str

    def to_chapter(self) -> Chapter:
        """
        convert a chapter model to chapter instance

        @return:
        """

        return Chapter(fid=BasicFrame.VOID_FRAME_ID, chapter_name=self.chapter_name)


def chapter_to_model(chapter: Chapter):
    """
    convert a chapter to chapter model

    @param chapter: chapter name
    @return: the model for the current chapter

    """
    model = ChapterModel()
    model.chapter_name = chapter.chapter_name
    return model
