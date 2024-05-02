import sys

import pygame
from render_util import calculate_scale_ratio, render_font_centered, scale_surface
from scenes.scene import SceneBase
from scenes.scenes import get_scene
from scenes.title_scene import GameButton
from ytdlMoo import download_video
from game_gui import TITLE_RESOLUTION

from game_gui import GameSprite

FONT_COLOR = (235, 225, 177)

class InputBox(GameSprite):
    def __init__(self, path: str, position: tuple[int, int]):
        super().__init__(path, position)
        self.active = False
        self.text = ""
    
    def handle_event(self, event: pygame.event.Event):
        pass

    def render(self, screen: pygame.Surface):
        pass



class UrlScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

        background_image = pygame.image.load("images/hackdavis_background.png")
        self.background_image = scale_surface(calculate_scale_ratio(background_image.get_size(), TITLE_RESOLUTION)[0], background_image)

        self.game_icon = GameSprite("images/icon_transparent.png", (343, 128))
        self.url_bar_sprite = GameSprite("images/url_bar.png", (256, 500))

        self.heading_font = pygame.font.Font("fonts/Modak-Regular.ttf", 100)
        self.video_font = pygame.font.Font("fonts/Modak-Regular.ttf", 80)

        self.buttons = [
            GameButton("images/Back Button.png", (69, 60),
                       lambda: ((), self.set_next_scene(get_scene("Level")))),
            GameButton("images/Next Button.png", (890, 880),
                       lambda: ((), self.set_next_scene(get_scene("Game"))))
        ]

    def render(self, screen: pygame.Surface):
        screen.blit(self.background_image, (0,0))

        self.game_icon.draw(screen)
        self.url_bar_sprite.draw(screen)

        render_font_centered("Enter a Video URL:", FONT_COLOR, self.heading_font, screen, (TITLE_RESOLUTION[0] // 2, 460))

        for button in self.buttons:
            button.draw(screen)
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = next(filter(lambda x: x.was_clicked(event.pos), self.buttons), None)

            if button:
                button.on_click()

    def takeUrl(self):
        base_font = pygame.font.Font(None, 32)
        user_text = ''


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