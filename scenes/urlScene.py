import pygame
from playScene import SceneBase
from playScene import playScene
from scenes.scenes import get_scene
from scenes.title_scene import GameButton


# Implement back button to playScene
# Go next to trimScene

class urlScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

        self.buttons = [
            GameButton("images/Back Button.png", (429, 103),
                       lambda: (self.click_sound.play(), self.set_next_scene(get_scene("playScene")))),
            GameButton("images/Next Button.png", (429, 103),
                       lambda: (self.click_sound.play(), self.set_next_scene(get_scene("Game"))))

        ]