import pygame
from game_state import GameState
from scenes.scene import SceneBase
from game_gui import GameSprite, GameButton, TITLE_RESOLUTION
import cv2

from scenes.scenes import get_scene


class TitleScene(SceneBase):
    def __init__(self, state: GameState):
        SceneBase.__init__(self)

        self.state = state
        self.click_sound = pygame.mixer.Sound("audio/buttonClick.mp3")
        self.game_icon = GameSprite("images/menuIcon.png", (100, 128))
        background_image = pygame.image.load("images/hackdavis_background.png")
        scale_ratio = TITLE_RESOLUTION[0] / background_image.get_size()[0]
        self.background_image = pygame.transform.smoothscale(background_image, (background_image.get_size()[0] * scale_ratio, background_image.get_size()[1] * scale_ratio))

        self.buttons = [
            GameButton("images/Play Button.png", (654, 359), lambda: (self.click_sound.play(), self.set_next_scene(get_scene("Level")))),
            GameButton("images/How to Play Button.png", (654, 474), lambda: 0),
            GameButton("images/Exit Button.png", (654, 590), lambda: (self.click_sound.play(), exit()))
        ]

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = next(filter(lambda x: x.was_clicked(event.pos), self.buttons), None)

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

        for button in self.buttons:
            button.draw(screen)

    def on_load(self):
        self.state.set_resolution(TITLE_RESOLUTION)
