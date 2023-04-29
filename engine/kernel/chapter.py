"""
define the class for Chapter, which is a special frame

"""
from kernel.frame import FrameInfo


class Chapter:
    """
    Chapter class, use to classified frames

    """

    def __init__(self, chapter_name: str):
        self.chapter_name: str = chapter_name
        self.__frames_info: dict[int, FrameInfo] = {}
        self.__fid_list: list[int] = []  # aim to maintain the order of the frames

    def append_frame_info(self, frame_info: FrameInfo):
        """
        set the tail fid

        @param frame_info: the frame info to be appended

        """
        self.__frames_info[frame_info.fid] = frame_info
        self.__fid_list.append(frame_info.fid)

    def get_all_fid(self) -> list[int]:
        """
        get all frame id

        @return: list of frame id

        """
        return self.__fid_list

    def get_tail_fid(self) -> int:
        """
        get the tail of the frame info

        @return: the frame info in the end of chapter

        """
        if len(self.__fid_list) == 0:
            return -1
        return self.__fid_list[-1]

    def remove_fid(self, fid: int) -> int:
        """
        remove the frame by fid

        @return: the removed fid, or -1 if failed

        """
        if len(self.__frames_info) == 0 or fid not in self.__fid_list:
            return -1

        self.__frames_info.pop(fid)
        self.__fid_list.remove(fid)
        return fid
