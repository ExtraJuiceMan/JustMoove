import pygame
from scene import SceneBase


class HowToPlayScene(SceneBase):
    HowToPlay_rect = pygame.Rect(500, 500, 500, 1000)

    def __init__(self):
        SceneBase.__init__(self)

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        # Set the background color to black
        screen.fill((0, 0, 0))

        # Draw neon pink rectangles for buttons with black text
        pygame.draw.rect(screen, (255, 105, 180), self.HowToPlay_rect)

        # Render text for the buttons
        font = pygame.font.Font(None, 36)
        HowToPlayScene_text = font.render("HowToPlay", True, (0, 0, 0))
        screen.blit(HowToPlayScene_text, (self.HowToPlayScene_rect.x + 10, self.HowToPlayScene_rect.y + 10))
