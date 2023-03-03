"""
API module for game slot control
"""

from .DBManager import DBManager
import time
from .ConfigManager import Loader
from utils.args_utils import Args


def get_cur_time():
    return str(time.time())


def parse_data(data: dict):
    return str(data)


class GameSlot:
    """
    Game slot control service
    """

    def __init__(self, db_dir: str, config_dir: str, slot_name: str = Args.DEFAULT):
        """
        constructor for game slot service

        @param db_dir: database directory, create one if not exist
        @param config_dir: config directory
        @param slot_name: specified slot name, use default if not specified
        """
        if slot_name is Args.DEFAULT:
            config = Loader(config_dir)
            slot_name = config.game_memory()["default_slot_name"]

        self.__dbman = DBManager(db_dir)
        self.__slot_name = slot_name

    def reset(self):
        """
        reset the engine slot
        """
        self.__dbman.drop_table(self.__slot_name)
        self.__dbman.create_table_if_not_exist(self.__slot_name)
        self.__dbman.commit()

    def drop(self):
        """
        drop the slot
        """
        self.__dbman.drop_table(self.__slot_name)
        self.__dbman.commit()

    def get_slot_name(self) -> str:
        """
        get slot name

        @return: slot name
        """
        return self.__slot_name

    def dump_progress(self, frame: int) -> str:
        """
        dump the current game progress (measured by frame) into slot

        @param frame: current progress, measured by frame number
        @return: progress create time
        """
        cur_time = get_cur_time()
        self.__dbman.push(
            key=str(cur_time), value=str(frame), table_name=self.__slot_name
        )
        self.__dbman.commit()
        return cur_time

    def remove_progress(self, time_strap: str):
        """
        remove progress (measured by frame) into slot

        @param time_strap: time to create progress
        """
        self.__dbman.remove(time_strap, self.__slot_name)
        self.__dbman.commit()

    def get_all_progress(self) -> list:
        """
        return all user's progress in dictionary with key is time, value is corresponded progress

        @return: list of {time: progress}
        """
        raw_data = self.__dbman.select(self.__slot_name)
        data = []
        for i in raw_data.keys():
            data.append({"time": i, "frame": raw_data[i]})
        return data

    def close(self):
        """
        close the game slot service

        @return:
        """
        self.__dbman.close()

    def print(self, limit=-1):
        """
        visualizing the progress

        @param limit: limit item print out, -1 for no limit
        """
        print("-" * 40)
        print(" " * 7 + "time" + " " * 14 + "progress")
        print("-" * 40)
        progresses = self.get_all_progress()
        if not len(progresses):
            print("empty")
        else:
            for i in self.get_all_progress():
                if limit != -1:
                    if limit == 0:
                        break
                    limit -= 1
                print(i["time"][:16] + " " * 10 + i["frame"])

            if limit == 0:
                print("...")
        print("-" * 40)


if __name__ == "__main__":
    print("Load GameSlot Class")
