"""
API module for game memory control
"""

import MsgColor, DBManager
import time


def get_cur_time():
    return str(time.time())


def parse_data(data: dict):
    return str(data)


class Service:
    def __init__(self, db_dir: str, slot_name: str):
        self._dbman = DBManager.Service(db_dir)
        self._slot_name = slot_name

    def reset(self):
        """
        reset the game slot
        """
        self._dbman.drop_table(self._slot_name)
        self._dbman.create_table_if_not_exist(self._slot_name)
        self._dbman.commit()

    def drop(self):
        self._dbman.drop_table(self._slot_name)
        self._dbman.commit()

    def get_slot_name(self) -> str:
        return self._slot_name

    def dump_memory(self, frame: int) -> str:
        cur_time = get_cur_time()
        self._dbman.push(key=str(cur_time), value=str(frame), table_name=self._slot_name)
        self._dbman.commit()
        return cur_time

    def remove_memory(self, time_strap: str):
        self._dbman.remove(time_strap, self._slot_name)
        self._dbman.commit()

    def get_all_memory(self) -> list:
        raw_data = self._dbman.select(self._slot_name)
        data = []
        for i in raw_data.keys():
            data.append({"time": i, "frame": raw_data[i]})
        return data

    def close(self):
        self._dbman.close()

    def print(self):
        print("-" * 40)
        print(" " * 7 + "time" + " " * 14 + "progress")
        print("-" * 40)
        for i in self.get_all_memory():
            print(i["time"] + " " * 10 + i["frame"])
        print("-" * 40)


if __name__ == "__main__":
    print(MsgColor.MsgColor.OK, "Load GameSlot Class", MsgColor.MsgColor.END)
