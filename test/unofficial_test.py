from module import GameSlot, ProjectManager
import random
from utils import file_utils

CONFIG_DIR = '../router/service.ini'
game_slot = GameSlot.GameSlot(db_dir="test.db", config_dir=CONFIG_DIR)

game_slot.reset()

print("Initial Slot")
game_slot.print()

# generate 10000 random progress
for _ in range(100):
    progress = int(random.random() * 100)
    game_slot.dump_progress(frame=progress)

game_slot.print(limit=10)

game_slot.close()
if file_utils.delete_file('test.db'):
    print('remove db')
else:
    print("remove db fail")

# test ProjectManager
project = ProjectManager.projectManager(base_dir="./myProject", config_dir=CONFIG_DIR)

# if project.delete():
#     print("remove project")
# else:
#     print("remove project fail")
