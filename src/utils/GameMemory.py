# API for game memory control

from src.utils import DBManager
from src.utils import MsgColor
import time


def get_cur_time():
    return str(time.time())


def parse_data(data: dict):
    return str(data)


class Service:
    def __init__(self, db_dict: str, slot_name: str):
        self._dbman = DBManager.Service(db_dict)
        self._slot_name = slot_name

    def reset(self):
        self._dbman.drop_table(self._slot_name)
        self._dbman.create_table_if_not_exist(self._slot_name)
        self._dbman.commit()
        print(
            MsgColor.MsgColor.OK,
            "(+) successfully reset slot: %s" % self._slot_name,
            MsgColor.MsgColor.END,
        )

    def drop(self):
        self._dbman.drop_table(self._slot_name)
        self._dbman.commit()
        print(
            MsgColor.MsgColor.OK,
            "(-) successfully drop slot: %s" % self._slot_name,
            MsgColor.MsgColor.END,
        )

    def get_slot_name(self) -> str:
        return self._slot_name

    def dump_memory(self, frame: int) -> str:
        cur_time = get_cur_time()
        self._dbman.push(
            key=str(cur_time), value=str(frame), table_name=self._slot_name
        )
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
