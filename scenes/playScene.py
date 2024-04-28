import sys

import pygame
from scene import SceneBase
from scenes.scenes import get_scene
from scenes.title_scene import GameButton


# Implement back button to titleScene
# Go next to urlScene
# Implement library of videos

class playScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

        self.buttons = [
            GameButton("images/Back Button.png", (429, 103),
                       lambda: (self.click_sound.play(), self.set_next_scene(get_scene("TitleScene")))),
        ]






