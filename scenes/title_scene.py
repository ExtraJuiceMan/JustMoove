import pygame
from scenes.scene import SceneBase


play_rect = pygame.Rect(100, 100, 100, 50)
HowToPlay_rect = pygame.Rect(100, 160, 100, 50)
exit_rect = pygame.Rect(100, 220, 100, 50)

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        pygame.mixer.init()

    def check_mouse_collision(self, rect, pos):
        return rect.collidepoint(pos)
    def click_sound(self):
        clickSound = pygame.mixer.Sound(r'audio\buttonClick.mp3')
        pygame.mixer.Sound.play(clickSound)
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.check_mouse_collision(play_rect, mouse_pos):
                self.click_sound()
            elif self.check_mouse_collision(HowToPlay_rect, mouse_pos):
                self.click_sound()
            elif self.check_mouse_collision(exit_rect, mouse_pos):
                self.click_sound()
    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self):
        pass

    def title(self, screen: pygame.Surface):
        WINDOW_WIDTH = 1280
        WINDOW_HEIGHT = 720

        # Set the background color to black
        screen.fill((0, 0, 0))
        menumusic = pygame.mixer.Sound(r'audio\menu_music.mp3')
        pygame.mixer.Sound.play(menumusic)
        pygame.mixer.Sound.set_volume(menumusic, 1)
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # Draw neon pink rectangles for buttons with black text
        pygame.draw.rect(screen, (255, 105, 180), play_rect)
        pygame.draw.rect(screen, (255, 105, 180), HowToPlay_rect)
        pygame.draw.rect(screen, (255, 105, 180), exit_rect)

        # Render text for the buttons
        font = pygame.font.Font(None, 36)
        play_text = font.render("Play", True, (0, 0, 0))
        HowToPlay_text = font.render("HowToPlay", True, (0, 0, 0))
        exit_text = font.render("Exit", True, (0, 0, 0))

        screen.blit(play_text, (play_rect.x + 10, play_rect.y + 10))
        screen.blit(HowToPlay_text, (HowToPlay_rect.x + 10, HowToPlay_rect.y + 10))
        screen.blit(exit_text, (exit_rect.x + 10, exit_rect.y + 10))

