"""
define the class for Chapter, which is a special frame

"""
from kernel.frame import FrameInfo


class Chapter:
    """
    Chapter class, use to classified frames

    """

    def __init__(self, chapter_name: str):
        self.__tail_fid: int = -1
        self.chapter_name: str = chapter_name
        self.__frames_info: list[FrameInfo] = []

    def append_frame_info(self, frame_info: FrameInfo):
        """
        set the tail fid

        @param frame_info: the frame info to be appended

        """
        self.__frames_info.append(frame_info)
        self.__tail_fid = frame_info.fid

    def get_all_frame_info(self) -> list[FrameInfo]:
        """
        get all the frame info

        @return: list of frame info

        """
        return self.__frames_info

    def get_all_fid(self) -> list[int]:
        """
        get all frame id

        @return: list of frame id

        """
        return [i.fid for i in self.__frames_info]

    def get_tail_fid(self) -> int:
        """
        get the tail of the frame info

        @return: the frame info in the end of chapter

        """
        return self.__tail_fid

    def remove_fid(self, fid: int) -> int:
        """
        remove the frame by fid

        @return: the removed fid, or -1 if failed

        """
        for idx, frame_info in enumerate(self.__frames_info):
            if frame_info.fid == fid:
                self.__frames_info.pop(idx)
                return fid

        return -1
