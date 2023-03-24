from engine.engine import Engine

from engine.component.character import CharacterPosition
from engine.component.music import MusicSignal
from engine.frame import *


engine = Engine(project_dir="../projects/aaa",
                config_dir="../service.ini")


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
