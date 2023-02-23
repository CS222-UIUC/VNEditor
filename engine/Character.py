class Character:
    def __init__(self, res_name: str, position: int):
        """
        constructor for character

        :param res_name: character file name
        :param position: choose from 1, 2, 3, 4, the character position on stage
        """
        self.res_name = res_name
        self.position = position
