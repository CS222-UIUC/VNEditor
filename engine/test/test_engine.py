import sys

sys.path.append("..")

from unittest import TestCase
from kernel.engine import Engine

import random
from kernel.component.branch import BranchTree
from kernel.frame import *
from utils.file_utils import delete_folder
from kernel.frame import make_frame


class TestEngine(TestCase):
    delete_folder("../projects/test/")
    os.mkdir("../projects/test/")
    engine = Engine(project_dir="../projects/test", config_dir="../service.ini")

    def test_make_frame(self):
        engine = self.engine
        print(engine.get_metadata_buffer())

        background = Background(res_name="b.jpg")
        character1 = Character(res_name="c.jpg")
        character2 = Character(
            res_name="c.jpg",
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
        dialogue.set_dialogue("hello world")
        self.assertEqual(dialogue.get_dialogue()[0], "hello world")
        music = Music(res_name="", signal=MusicSignal.KEEP)
        music.set_music()
        music.get_music()
        engine.add_chapter("a")
        print(engine.get_all_chapter())
        for i in range(100):
            frame = make_frame(
                background=background,
                character=characters,
                music=music,
                dialog=dialogue,
                meta=meta,
            )
            model = frame_to_model(frame)
            self.assertNotEqual(frame, None)
            self.assertNotEqual(model.to_frame(), None)
            if i % 10 == 0:
                nid = engine.append_frame(frame, "a", force=True)
                print("add frame: ", nid)
        frame = make_frame(
            background=background,
            character=characters,
            music=music,
            dialog=dialogue,
            meta=meta,
        )
        checker = FrameChecker("../projects/test", ConfigLoader("../service.ini"))
        self.assertFalse(checker.check(frame)[0])

        print(engine.render_struct())
        meta = FrameMeta("")
        frame = make_frame(
            background=background,
            character=characters,
            music=music,
            dialog=dialogue,
            meta=meta,
        )
        print(engine.render_struct())

        with self.assertRaises(Exception):
            engine.remove_frame(10000)
        frame_keys = list(engine.get_frame_ids())

        for i in frame_keys:
            if random.getrandbits(1):
                print(f"remove id: {i}")
                engine.remove_frame(fid=i)

        engine.commit()
        ids = list(engine.get_frame_ids())
        print(engine.get_metadata_buffer())
        for i in ids:
            print(i, engine.get_frame(fid=i))

        # kernel.insert_frame(ids[-1], ids[0])

        frame_keys = engine.get_frame_ids()
        self.assertNotEqual(len(frame_keys), 0)
        for i in list(frame_keys):
            if random.getrandbits(1):
                print(f"remove id: {i}")
                engine.remove_frame(fid=i)
        with self.assertRaises(Exception):
            engine.render_struct("not exist chapter")

        engine.commit()
