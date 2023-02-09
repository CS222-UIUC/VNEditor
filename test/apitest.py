from src.api import memory
import time

memory_service = memory.Service(db_dict="test.db", slot_name="slot1")

memory_service.reset()

memory_service.dump_memory(12)
memory_service.dump_memory(10)
memory_service.dump_memory(17)
memory_service.dump_memory(30)
create_time = memory_service.dump_memory(13)

memory_service.remove_memory(create_time)
memory_service.remove_memory(create_time)


print("-" * 40)
print(" " * 7 + "time" + " " * 14 + "progress")
print("-" * 40)
for i in memory_service.get_all_memory():
    print(i["time"] + " " * 10 + i["frame"])
print("-" * 40)
