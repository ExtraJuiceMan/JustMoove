import pygame
from scene import SceneBase


play_img = pygame.image.load("Play Button.png")
HowToPlay_img = pygame.image.load("How To Play Button.png")
exit_img = pygame.image.load("Exit Button.png")

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        pygame.mixer.init()

        self.background_image = pygame.image.load("menuIcon.png")

    def check_mouse_collision(self, rect, pos):
        return rect.collidepoint(pos)
    def click_sound(self):
        clickSound = pygame.mixer.Sound(r'audio\buttonClick.mp3')
        pygame.mixer.Sound.play(clickSound)
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.check_mouse_collision(play_img, mouse_pos):
                self.click_sound()
                self.set_next_scene(playScene)
            elif self.check_mouse_collision(HowToPlay_img, mouse_pos):
                self.click_sound()
            elif self.check_mouse_collision(exit_img, mouse_pos):
                self.click_sound()
    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self):
        pass

    def title(self, screen: pygame.Surface):
        screen.blit(self.background_image, (0, 0))


        # Set the background color to black

        menumusic = pygame.mixer.Sound(r'audio\menu_music.mp3')
        pygame.mixer.Sound.play(menumusic)
        pygame.mixer.Sound.set_volume(menumusic, 1)

        screen.blit(play_img)
        screen.blit(HowToPlay_img)
        screen.blit(exit_img)

