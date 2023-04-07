import sys

sys.path.append("..")

from unittest import TestCase
from engine.engine import Engine

import random
from engine.component.branch import BranchTree
from engine.component.character import CharacterPosition
from engine.component.music import MusicSignal
from engine.frame import *


class TestEngine(TestCase):
    engine = Engine(project_dir="../projects/aa", config_dir="../service.ini")

    def test_make_frame(self):
        engine = self.engine
        print(engine.get_metadata_buffer())

        background = Background(res_name="b.jpg")
        character1 = Character(
            res_name="c.jpg", position=CharacterPosition(x=12, y=11.9)
        )
        character2 = Character(
            res_name="c.jpg", position=CharacterPosition(x=56, y=11.9)
        )
        characters = [character1, character2]
        dialogue = Dialogue(dialogue="hello world", character=character1)
        branch = BranchTree()
        branch.add_branch(1, "choice 1")
        branch.add_branch(1, "choice 1")
        print(branch.get_all_branch())
        self.assertTrue(branch.get_all_branch()[1] == "choice 1")

        branch.delete_branch(1)
        branch.delete_branch(111)

        dialogue.set_dialogue("hello world")
        self.assertEqual(dialogue.get_dialogue()[0], "hello world")

        music = Music(signal=MusicSignal.KEEP)
        music.set_music()
        music.get_music()

        for i in range(100):
            frame = engine.make_frame(
                background=background,
                chara=characters,
                music=music,
                dialog=dialogue,
            )
            if i % 10 == 0:
                nid = engine.append_frame(frame, force=True)
                print("add frame: ", nid)

        head_id = engine.get_head_id()
        print(f"head id: {head_id}")

        with self.assertRaises(Exception):
            engine.remove_frame(10000)
        frame_keys = engine.get_all_frame_id()

        for i in frame_keys:
            if random.getrandbits(1):
                print(f"remove id: {i}")
                engine.remove_frame(frame_id=i)

        engine.commit()
        ids = list(engine.get_all_frame_id())
        print(engine.get_metadata_buffer())
        for i in ids:
            print(i, engine.get_frame(fid=i))

        # engine.insert_frame(ids[-1], ids[0])

        frame_keys = engine.get_all_frame_id()
        self.assertNotEqual(len(frame_keys), 0)
        for i in frame_keys:
            if random.getrandbits(1):
                print(f"remove id: {i}")
                engine.remove_frame(frame_id=i)

        engine.commit()
