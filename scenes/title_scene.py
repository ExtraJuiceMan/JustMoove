import pygame
from scenes.scene import SceneBase


play_rect = pygame.Rect(100, 100, 100, 50)
rules_rect = pygame.Rect(100, 160, 100, 50)
exit_rect = pygame.Rect(100, 220, 100, 50)

class TitleScene(SceneBase):
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
        pygame.draw.rect(screen, (255, 105, 180), play_rect)
        pygame.draw.rect(screen, (255, 105, 180), rules_rect)
        pygame.draw.rect(screen, (255, 105, 180), exit_rect)

        # Render text for the buttons
        font = pygame.font.Font(None, 36)
        play_text = font.render("Play", True, (0, 0, 0))
        rules_text = font.render("Rules", True, (0, 0, 0))
        exit_text = font.render("Exit", True, (0, 0, 0))

        screen.blit(play_text, (play_rect.x + 10, play_rect.y + 10))
        screen.blit(rules_text, (rules_rect.x + 10, rules_rect.y + 10))
        screen.blit(exit_text, (exit_rect.x + 10, exit_rect.y + 10))