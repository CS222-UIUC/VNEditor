from Frame import Frame
from Branch import BranchTree


class Action:
    """
    Frame attribute, guild the next step after current frame
    """

    def __init__(self, next_f: Frame, action: BranchTree = BranchTree.DEFAULT):
        """
        constructor for Action
        :param next_f: next frame
        :param action: special action, i.e. branch frame
        """
        self.next = next_f
        self.action = action
