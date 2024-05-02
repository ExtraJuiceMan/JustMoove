import sys

import pygame
from game_state import GameState
from media_library import MediaLibrary
from render_util import calculate_scale_ratio, render_font_centered, scale_surface
from scenes.scene import SceneBase
from scenes.scenes import get_scene
from scenes.title_scene import GameButton
from video_downloader import download_video
from game_gui import TITLE_RESOLUTION

from game_gui import GameSprite

FONT_COLOR = (235, 225, 177)
TEMP_VID = "video_downloads/tempvid"

class VideoDlScene(SceneBase):

    def __init__(self, media_library: MediaLibrary, state: GameState):
        SceneBase.__init__(self)
        self.media_library = media_library
        self.state = state

        background_image = pygame.image.load("images/hackdavis_background.png")
        self.background_image = scale_surface(
            calculate_scale_ratio(background_image.get_size(), TITLE_RESOLUTION)[0],
            background_image,
        )

        self.game_icon = GameSprite("images/icon_transparent.png", (343, 128))

        self.heading_font = pygame.font.Font("fonts/Modak-Regular.ttf", 100)
        self.video_font = pygame.font.Font("fonts/Modak-Regular.ttf", 80)

        self.render_state = 0
        self.path = None

    def display_text(self, text, screen):
        screen.blit(self.background_image, (0, 0))

        self.game_icon.draw(screen)

        render_font_centered(
            text,
            FONT_COLOR,
            self.heading_font,
            screen,
            (TITLE_RESOLUTION[0] // 2, 460),
        )

    def render(self, screen: pygame.Surface):
        if self.render_state == 0:
            self.display_text("Downloading Video...", screen)
            self.render_state = 1
            return

        if self.render_state == 1:
            self.path = download_video(self.state.download_url)
            self.display_text("Processing Video...", screen)
            self.render_state = 2
            return

        if self.render_state == 2:
            self.media_library.add_video(self.path)
            self.set_next_scene(get_scene("Level"))
            self.render_state = 0
            return

    def handle_event(self, event: pygame.event.Event):
        pass
