import sys

sys.path.append("..")

from unittest import TestCase
from engine.engine import Engine

import random
from engine.component.branch import BranchTree
from engine.frame import *


class TestEngine(TestCase):
    engine = Engine(project_dir="../projects/test", config_dir="../service.ini")

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
        meta = FrameMeta()

        branch.delete_branch(1)
        branch.delete_branch(111)
        frame_meta = FrameMeta(chapter='a')
        dialogue.set_dialogue("hello world")
        self.assertEqual(dialogue.get_dialogue()[0], "hello world")
        music = Music(signal=MusicSignal.KEEP)
        music.set_music()
        music.get_music()
        engine.append_chapter(engine.make_chapter('a'))
        print(engine.get_all_chapter())
        for i in range(100):
            frame = engine.make_frame(
                background=background,
                chara=characters,
                music=music,
                dialog=dialogue,
            )
            self.assertNotEqual(frame_to_model(frame, frame_meta), None)
            if i % 10 == 0:
                nid = engine.append_frame(frame, frame_meta, force=True)
                print("add frame: ", nid)
        frame = engine.make_frame(
            background=background,
            chara=characters,
            music=music,
            dialog=dialogue,
        )
        checker = FrameChecker("../projects/test", ConfigLoader("../service.ini"))
        self.assertFalse(checker.check(frame)[0])

        print(engine.render_struct())
        meta = FrameMeta("", "test")
        frame = engine.make_frame(
            background=background,
            chara=characters,
            music=music,
            dialog=dialogue,
        )
        print(engine.render_struct())

        with self.assertRaises(Exception):
            engine.remove_frame(10000)
        frame_keys = engine.get_all_frame_id()

        for i in frame_keys:
            if random.getrandbits(1):
                print(f"remove id: {i}")
                engine.remove_frame(fid=i)

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
                engine.remove_frame(fid=i)
        self.assertNotEqual(len(engine.get_ordered_fid()), 0)
        self.assertEqual(engine.render_struct("not exist chapter"), {})
        engine.commit()
