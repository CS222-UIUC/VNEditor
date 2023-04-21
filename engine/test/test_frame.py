import os
import unittest
from typing import Optional
from pydantic import BaseModel

from module.config_manager import ConfigLoader
from engine.component.background import Background
from engine.component.character import (
    Character,
    CharacterPosition,
    CharacterPositionModal,
)
from engine.component.dialogue import Dialogue
from engine.component.music import Music, MusicSignal
from engine.component.action import Action
from engine.component.meta import FrameMeta

from engine.frame import FrameChecker, Frame

class TestFrameChecker(unittest.TestCase):
    def setUp(self):
        self.project_dir = '../projects/test'
        self.config = ConfigLoader("../service.ini")
        self.frame_checker = FrameChecker(self.project_dir, self.config)

    def test_frame_check(self):
        frame = Frame(
            fid=1,
            background=Background(res_name="bg_res_name"),
            chara=[
                Character(res_name="chara_res_name1", position=CharacterPosition(0, 0)),
                Character(res_name="chara_res_name2", position=CharacterPosition(100, 100)),
            ],
            music=Music(res_name="music_res_name", signal=MusicSignal.PLAY),
            dialog=Dialogue(dialogue="Hello!", character=Character(res_name="chara_res_name1")),
            action=Action(1, 2)
        )

        result, message = self.frame_checker.check(frame)

        self.assertTrue(result)
        self.assertIsNone(message)

    def test_frame_check_failure(self):
        frame = Frame(
            fid=1,
            background=Background(res_name="nonexistent_bg_res"),
            chara=[
                Character(res_name="chara_res_name1", position=CharacterPosition(0, 0)),
                Character(res_name="chara_res_name2", position=CharacterPosition(100, 100)),
            ],
            music=Music(res_name="music_res_name", signal=MusicSignal.PLAY),
            dialog=Dialogue(dialogue="Hello!", character=Character(res_name="chara_res_name1")),
            action=Action(1, 2)
        )

        result, message = self.frame_checker.check(frame)

        self.assertFalse(result)
        self.assertIsNotNone(message)


if __name__ == "__main__":
    unittest.main()