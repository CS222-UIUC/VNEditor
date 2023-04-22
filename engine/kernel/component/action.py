"""
action component for frame
"""

from typing import Optional
from kernel.component.branch import BranchTree


class Action:
    """
    Frame attribute, guild the next step after current frame
    """

    def __init__(
        self, next_f_id: int, prev_f_id: int, branch: Optional[BranchTree] = None
    ):
        """
        constructor for Action

        @param prev_f_id: previous frame id
        @param next_f_id: next frame id
        @param branch: special action, i.e. branch frame
        """
        self.prev_f: int = prev_f_id
        self.next_f: int = next_f_id
        self.branch: BranchTree = branch
