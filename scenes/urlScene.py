import sys

import pygame
from playScene import SceneBase
from playScene import playScene
from scenes.scenes import get_scene
from scenes.title_scene import GameButton
from ytdlMoo import download_video


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

    def takeUrl(self):
        base_font = pygame.font.Font(None, 32)
        user_text = ''

        input_rect = pygame.Rect(928, 85)  # Adjust width and height as needed

        active = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            url = user_text  # Save the user text as URL
                            download_video(video_url=url)
                        else:
                            user_text += event.unicode