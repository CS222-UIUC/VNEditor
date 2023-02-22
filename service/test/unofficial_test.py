from service.module import GameSlot
import random

game_slot = GameSlot.GameSlot(db_dir="test.db")

game_slot.reset()

print("Initial Slot")
game_slot.print()

# generate 10000 random progress
for _ in range(100):
    progress = int(random.random() * 100)
    game_slot.dump_progress(frame=progress)

game_slot.print(limit=10)
