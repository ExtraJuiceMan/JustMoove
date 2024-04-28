import pygame
from scenes.scene import SceneBase
import pyautogui
import cv2

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        pygame.mixer.init()

    def set_background(self, screen: pygame.Surface, background_image_path: str):
        """
        Sets the background image for the given screen.

        Args:
            screen (pygame.Surface): The Pygame surface to set the background on.
            background_image_path (str): Path to the background image file.
        """
        background_image = pygame.image.load(background_image_path)
        screen.blit(background_image, (0, 0))

    def click_sound(self):
        clickSound = pygame.mixer.Sound(r'audio\buttonClick.mp3')
        pygame.mixer.Sound.play(clickSound)

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self):
        pass

    def menu(self, screen: pygame.Surface):
        self.set_background(screen, "images\\menuicon.png")  # Set background
        pygame.display.update()
        menumusic = pygame.mixer.Sound(r'audio\menu_music.mp3')
        pygame.mixer.Sound.play(menumusic)
        pygame.mixer.Sound.set_volume(menumusic, 1)



sa