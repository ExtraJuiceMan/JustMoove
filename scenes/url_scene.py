import sys

import pygame
from game_state import GameState
from render_util import calculate_scale_ratio, render_font_centered, scale_surface
from scenes.scene import SceneBase
from scenes.scenes import get_scene
from scenes.title_scene import GameButton
from video_downloader import download_video
from game_gui import TITLE_RESOLUTION

from game_gui import GameSprite

FONT_COLOR = (235, 225, 177)

class InputBox(GameSprite):
    def __init__(self, path: str, position: tuple[int, int], font: pygame.font.Font, font_offset=(0,0)):
        super().__init__(path, position)
        self.active = False
        self.font = font
        self.text = ""
        self.font_offset = font_offset

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.was_clicked(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            pasted = pygame.scrap.get(pygame.SCRAP_TEXT)
            if pasted:
                self.text += pasted.decode("ascii").replace("\x00", "")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def render(self, screen: pygame.Surface):
        self.draw(screen)

        text = self.text
        rendered_font = self.font.render(text, True, FONT_COLOR)

        while rendered_font.get_size()[0] > self.sprite.get_size()[0] - self.font_offset[0] * 2:
            text = text[1:]
            rendered_font = self.font.render(text, True, FONT_COLOR)

        screen.blit(rendered_font, (self.position[0] + self.font_offset[0], self.position[1] + self.font_offset[1]))


class UrlScene(SceneBase):

    def __init__(self, state: GameState):
        SceneBase.__init__(self)

        self.state = state

        background_image = pygame.image.load("images/hackdavis_background.png")
        self.background_image = scale_surface(calculate_scale_ratio(background_image.get_size(), TITLE_RESOLUTION)[0], background_image)

        self.game_icon = GameSprite("images/icon_transparent.png", (343, 128))

        self.heading_font = pygame.font.Font("fonts/Modak-Regular.ttf", 100)
        self.video_font = pygame.font.Font("fonts/Modak-Regular.ttf", 80)

        self.buttons = [
            GameButton("images/Back Button.png", (69, 60),
                       lambda: ((), self.set_next_scene(get_scene("Level")))),
            GameButton("images/Next Button.png", (890, 880),
                       lambda: ((self.state.set_download_url(self.input.text)), self.set_next_scene(get_scene("VideoDl"))))
        ]

        self.input = InputBox("images/url_bar.png", (256, 500), self.video_font, (50, 12))

    def render(self, screen: pygame.Surface):
        screen.blit(self.background_image, (0,0))

        self.game_icon.draw(screen)
        self.input.render(screen)

        render_font_centered("Enter a Video URL:", FONT_COLOR, self.heading_font, screen, (TITLE_RESOLUTION[0] // 2, 460))

        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event: pygame.event.Event):
        self.input.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            button = next(filter(lambda x: x.was_clicked(event.pos), self.buttons), None)

            if button:
                button.on_click()
