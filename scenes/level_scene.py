from numpy import positive
import pygame
from game_state import GameState, GameVideoConfiguration
from scenes.scene import SceneBase
import cv2

from scenes.scenes import get_scene, set_scene
from game_gui import GameSprite, GameButton, TITLE_RESOLUTION
from video_impl import RecordedCV2VideoFrames

ROW_START_Y_OFFSET = 180
ROW_START_X_OFFSET = 74
ROW_COUNT = 4
ROW_GAP_X = 32
ROW_GAP_Y = 16
FONT_COLOR = (235, 225, 177)

class LevelEntry(GameButton):
    def __init__(self, path: str, position: tuple[int, int], on_click, font: pygame.font.Font, dance_name, high_score):
        GameButton.__init__(self, path, position, on_click)
        self.font = font
        self.dance_name = dance_name
        self.high_score = high_score

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        rendered_font = self.font.render(self.dance_name, True, FONT_COLOR)
        font_x, font_y = rendered_font.get_size()
        entry_x, entry_y = GameSprite("images/level_entry.png", (0, 0)).sprite.get_size()
        font_pos = (self.position[0] + entry_x // 2 - font_x // 2, self.position[1] - font_y // 2)
        screen.blit(rendered_font, font_pos)

class LevelScene(SceneBase):
    def __init__(self, video_config: GameVideoConfiguration, state: GameState):
        SceneBase.__init__(self)

        self.video_config = video_config
        self.state = state

        background_image = pygame.image.load("images/hackdavis_background.png")
        scale_ratio = TITLE_RESOLUTION[0] / background_image.get_size()[0]
        self.background_image = pygame.transform.smoothscale(background_image, (background_image.get_size()[0] * scale_ratio, background_image.get_size()[1] * scale_ratio))

        self.game_icon = GameSprite("images/icon_transparent.png", (343, 128))
        self.back_button = GameButton("images/level_back.png", (-24, 40), lambda: self.set_next_scene(get_scene("Title")))
        self.entry_font = pygame.font.Font("fonts/Modak-Regular.ttf", 40)

        self.entries = self.create_level_entries()

    def switch_level(self, id):
        video = self.state.videos.get_video(id)
        self.video_config.set_video(RecordedCV2VideoFrames(video))
        self.set_next_scene(get_scene("Game"))

    def create_level_entries(self):
        videos = list(self.state.videos.all_videos().items())
        dummy_entry = GameSprite("images/level_entry.png", (0, 0)).sprite

        entry_x, entry_y = dummy_entry.get_size()

        entries = []

        for i in range(len(videos)):
            video_meta = videos[i]

            row = i // ROW_COUNT
            column = i % ROW_COUNT

            offset_x = ROW_START_X_OFFSET + column * entry_x + column * ROW_GAP_X
            offset_y = ROW_START_Y_OFFSET + row * entry_y + row * ROW_GAP_Y

            entries.append(
                LevelEntry("images/level_entry.png", (offset_x, offset_y),
                    lambda x=video_meta[1].id: self.switch_level(x), self.entry_font,
                    f"Dance #{video_meta[0]}",
                    69))

        return entries

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.was_clicked(event.pos):
                self.back_button.on_click()
                return

            button = next(filter(lambda x: x.was_clicked(event.pos), self.entries), None)

            if button:
                button.on_click()

    def update(self):
        pass

    def menu(self, screen: pygame.Surface):
        pygame.display.update()
        menumusic = pygame.mixer.Sound(r'audio\menu_music.mp3')
        pygame.mixer.Sound.play(menumusic)
        pygame.mixer.Sound.set_volume(menumusic, 1)

    def render(self, screen: pygame.Surface):
        screen.blit(self.background_image, (0, 0))

        self.game_icon.draw(screen)
        self.back_button.draw(screen)

        for entry in self.entries:
            entry.draw(screen)

    def on_load(self):
        self.state.set_resolution(TITLE_RESOLUTION)