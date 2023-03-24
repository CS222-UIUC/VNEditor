from engine.engine import Engine

<<<<<<< HEAD
from engine.component.character import CharacterPosition
from engine.component.music import MusicSignal
from engine.frame import *
=======
import random
from engine.component.character import CharacterPosition
from engine.component.music import MusicSignal
from engine.frame import *
from utils import status
>>>>>>> 70dad1d15cfc57f95f402403263021528a40be31

engine = Engine(project_dir="../projects/aaa", config_dir="../service.ini")

<<<<<<< HEAD
engine = Engine(project_dir="../projects/aaa",
                config_dir="../service.ini")
=======
print(engine.get_metadata_buffer())

background = Background(res_name="b.jpg")
character1 = Character(res_name="c.jpg", position=CharacterPosition(x=12, y=11.9))
character2 = Character(res_name="c.jpg", position=CharacterPosition(x=56, y=11.9))
characters = [character1, character2]
dialogue = Dialogue(dialogue="hello world", character=character1)
music = Music(signal=MusicSignal.KEEP)
>>>>>>> 70dad1d15cfc57f95f402403263021528a40be31

for i in range(100):
    frame = engine.make_frame(
        _type=Frame,
        background=background,
        chara=characters,
        music=music,
        dialog=dialogue,
    )
    if i % 10 == 0:
        nid = engine.append_frame(frame)
        print("add frame: ", nid)

head_id = engine.get_head_id()
print(f"head id: {head_id}")

frame_keys = engine.get_all_frame_id()

for i in frame_keys:
    if random.getrandbits(1):
        print(f"remove id: {i}")
        engine.remove_frame(frame_id=i)

engine.commit()
print(engine.get_metadata_buffer())

<<<<<<< HEAD
background = Background(res_name='b.jpg')
character1 = Character(res_name="c.jpg", position=CharacterPosition(x=12, y=11.9))
character2 = Character(res_name="c.jpg", position=CharacterPosition(x=56, y=11.9))
characters = [character1, character2]
dialogue = Dialogue(dialogue="hello world", character=character1)
music = Music(signal=MusicSignal.KEEP)

for i in range(100):
    frame = engine.make_frame(_type=Frame, background=background, chara=characters, music=music, dialog=dialogue)
    if i % 10 == 0:
        engine.append_frame(frame)

engine.commit()
=======
>>>>>>> 70dad1d15cfc57f95f402403263021528a40be31
