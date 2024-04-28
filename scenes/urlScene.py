import pygame
from playScene import SceneBase
from playScene import playScene


# Implement back button to playScene
# Go next to trimScene

class urlScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.set_background("Menu.png")