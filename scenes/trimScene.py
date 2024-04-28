import pygame
from scene import SceneBase
from playScene import playScene

# Implement back button to urlScene
# Go next to gameScene

class trimScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.set_back
        self.set_background("Menu.png")
