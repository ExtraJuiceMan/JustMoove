import pygame
from game_state import GameState, GameVideoConfiguration
from scenes.scene import SceneBase
from game_gui import GameSprite, GameButton, TITLE_RESOLUTION
import cv2

from scenes.scenes import get_scene

class ScoreBox(GameSprite):
    def __init__(self, path: str, position: tuple[int, int], font: pygame.font.Font, score):
        GameSprite.__init__(self, path, position)
        self.font = font
        self.score = score

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        rendered_font = self.font.render(f"Score: {self.score:.2f}", True, (0, 0, 0))

        font_x, font_y = rendered_font.get_size()
        entry_x, entry_y = self.sprite.get_size()
        font_pos = (self.position[0] + entry_x // 2 - font_x // 2, self.position[1] + entry_y // 2 - font_y // 2)

        screen.blit(rendered_font, font_pos)

class EndScene(SceneBase):
    def __init__(self, video_config: GameVideoConfiguration, state: GameState):
        SceneBase.__init__(self)

        self.state = state
        self.score = 0
        self.video_config = video_config
        self.click_sound = pygame.mixer.Sound("audio/buttonClick.mp3")
        self.game_icon = pygame.transform.smoothscale(pygame.image.load("images/menuIcon.png"), (500, 515)).convert_alpha()
        background_image = pygame.image.load("images/hackdavis_background.png")
        scale_ratio = TITLE_RESOLUTION[0] / background_image.get_size()[0]
        self.background_image = pygame.transform.smoothscale(background_image, (background_image.get_size()[0] * scale_ratio, background_image.get_size()[1] * scale_ratio))

        self.font = pygame.font.Font("fonts/Modak-Regular.ttf", 80)
        self.score_box = ScoreBox("images/score_rect.png", (333, 559), self.font, self.state.score)

        self.buttons = [
            GameButton("images/Play Again.png", (323, 822), lambda: (self.click_sound.play(), self.set_next_scene(get_scene("Title")))),
            GameButton("images/Library.png", (729, 822), lambda: (self.click_sound.play(), self.set_next_scene(get_scene("Level")))),
        ]

    def set_score(self, score):
        self.score = score
        self.score_box.score = score

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = next(filter(lambda x: x.was_clicked(event.pos), self.buttons), None)

            if button:
                button.on_click()

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.game_icon, (470, 30))

        screen.blit(self.font.render(f"Moove #{self.video_config.video_meta.id}", True,(255,255,255)), (552, 480))

        self.score_box.draw(screen)

        for button in self.buttons:
            button.draw(screen)

    def on_load(self):
        self.state.set_resolution(TITLE_RESOLUTION)
