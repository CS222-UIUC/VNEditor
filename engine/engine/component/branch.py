"""
branch component for frame
"""


class BranchTree:
    """
    Branch struct
    """

    def __init__(self):
        self.__branch_tree: dict[int, str] = {}

    def add_branch(self, corresponding_frame_id: int, description: str):
        """
        add branch to the Branch tree, cannot add if branch already exists

        @param corresponding_frame_id: corresponding next frame related to description
        @param description: selection text
        @return: action status

        """

        if corresponding_frame_id in self.__branch_tree:
            return False

        self.__branch_tree[corresponding_frame_id] = description
        return True

    def delete_branch(self, corresponding_frame_id: int) -> bool:
        """
        delete branch in branch tree

        @param corresponding_frame_id: id of the frame try to delete
        @return: action status

        """
        if corresponding_frame_id not in self.__branch_tree:
            return False

        self.__branch_tree.pop(corresponding_frame_id)
        return True

    def get_all_branch(self) -> dict:
        """
        get all branch, {frame id: description}

        @return: branchTree
        """
        return self.__branch_tree
