# from engine.engine import Engine
#
# import random
# from engine.component.character import CharacterPosition
# from engine.component.music import MusicSignal
# from engine.frame import *
#
# engine = Engine(project_dir="../projects/aaa", config_dir="../service.ini")
#
# print(engine.get_metadata_buffer())
#
# background = Background(res_name="b.jpg")
# character1 = Character(res_name="c.jpg", position=CharacterPosition(x=12, y=11.9))
# character2 = Character(res_name="c.jpg", position=CharacterPosition(x=56, y=11.9))
# characters = [character1, character2]
# dialogue = Dialogue(dialogue="hello world", character=character1)
# music = Music(signal=MusicSignal.KEEP)
#
# for i in range(100):
#     frame = engine.make_frame(
#         _type=Frame,
#         background=background,
#         chara=characters,
#         music=music,
#         dialog=dialogue,
#     )
#     if i % 10 == 0:
#         nid = engine.append_frame(frame)
#         print("add frame: ", nid)
#
# head_id = engine.get_head_id()
# print(f"head id: {head_id}")
#
# frame_keys = engine.get_all_frame_id()
#
# for i in frame_keys:
#     if random.getrandbits(1):
#         print(f"remove id: {i}")
#         engine.remove_frame(frame_id=i)
#
# engine.commit()
# ids = list(engine.get_all_frame_id())
# print(engine.get_metadata_buffer())
# for i in ids:
#     print(i, engine.get_frame(fid=i))
#
# ids = list(engine.get_all_frame_id())
#
# engine.insert_frame(ids[-1], ids[0])
#
# frame_keys = engine.get_all_frame_id()
#
# for i in frame_keys:
#     if random.getrandbits(1):
#         print(f"remove id: {i}")
#         engine.remove_frame(frame_id=i)
#
# engine.commit()
#
#
