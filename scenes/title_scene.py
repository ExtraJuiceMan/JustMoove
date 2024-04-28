import pygame
from scenes.scene import SceneBase
from playScene import playScene
import pyautogui
import cv2




class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        pygame.mixer.init()
        self.set_background("Menu.png")

    def click_sound(self):
        clickSound = pygame.mixer.Sound(r'audio\buttonClick.mp3')
        pygame.mixer.Sound.play(clickSound)

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self):
        pass

    def menu(self, screen: pygame.Surface):
        menumusic = pygame.mixer.Sound(r'audio\menu_music.mp3')
        pygame.mixer.Sound.play(menumusic)
        pygame.mixer.Sound.set_volume(menumusic, 1)


    def find_and_click(image_path, confidence=0.5, grayscale=True):
        # Find position of the image using PyAutoGUI
        image_position = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, grayscale=grayscale)

        if image_position:
            # Create a rectangle around the image position
            image_rect = pygame.Rect(image_position[0] - 50, image_position[1] - 15, 100, 30)

            # Display a message if the rectangle is clicked
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if image_rect.collidepoint(pos):
                            print("I've been clicked")
                            return