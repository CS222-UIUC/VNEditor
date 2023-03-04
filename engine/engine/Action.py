from Frame import Frame
from Branch import BranchTree
from utils.args_utils import Args


class Action:
    """
    Frame attribute, guild the next step after current frame
    """

    LAST_FRAME = -1

    def __init__(
        self, next_f_id: int, prev_f_id: int, branch: BranchTree = BranchTree.DEFAULT
    ):
        """
        constructor for Action

        @param prev_f_id: previous frame id
        @param next_f_id: next frame id
        @param branch: special action, i.e. branch frame
        """
        self.prev_f = prev_f_id
        self.next_f = next_f_id
        self.branch = branch

    def change_next_f(self, next_f_id: int):
        """
        change the next frame pointer

        @param next_f_id: the new next frame
        @return:
        """
        self.next_f = next_f_id

    def change_prev_f(self, prev_f_id: int):
        """
        change the prev frame pointer

        @param prev_f_id: the new next frame
        @return:
        """
