# from kernel.kernel import Engine
#
# import random
# from kernel.component.character import CharacterPosition
# from kernel.component.music import MusicSignal
# from kernel.frame import *
#
# kernel = Engine(project_dir="../projects/aaa", config_dir="../service.ini")
#
# print(kernel.get_metadata_buffer())
#
# background = Background(res_name="b.jpg")
# character1 = Character(res_name="c.jpg", position=CharacterPosition(x=12, y=11.9))
# character2 = Character(res_name="c.jpg", position=CharacterPosition(x=56, y=11.9))
# characters = [character1, character2]
# dialogue = Dialogue(dialogue="hello world", character=character1)
# music = Music(signal=MusicSignal.KEEP)
#
# for i in range(100):
#     frame = kernel.make_frame(
#         _type=Frame,
#         background=background,
#         chara=characters,
#         music=music,
#         dialog=dialogue,
#     )
#     if i % 10 == 0:
#         nid = kernel.append_frame(frame)
#         print("add frame: ", nid)
#
# head_id = kernel.get_head_id()
# print(f"head id: {head_id}")
#
# frame_keys = kernel.get_all_frame_id()
#
# for i in frame_keys:
#     if random.getrandbits(1):
#         print(f"remove id: {i}")
#         kernel.remove_frame(frame_id=i)
#
# kernel.commit()
# ids = list(kernel.get_all_frame_id())
# print(kernel.get_metadata_buffer())
# for i in ids:
#     print(i, kernel.get_frame(fid=i))
#
# ids = list(kernel.get_all_frame_id())
#
# kernel.insert_frame(ids[-1], ids[0])
#
# frame_keys = kernel.get_all_frame_id()
#
# for i in frame_keys:
#     if random.getrandbits(1):
#         print(f"remove id: {i}")
#         kernel.remove_frame(frame_id=i)
#
# kernel.commit()
#
#
