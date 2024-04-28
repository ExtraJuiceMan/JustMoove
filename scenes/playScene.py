import pygame
from scene import SceneBase

# Implement back button to titleScene
# Go next to urlScene
# Implement library of videos

class playScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)


    def set_background(screen: pygame.Surface, background_image_path: str):
        """
        Sets the background image for the given screen.

        Args:
            screen (pygame.Surface): The Pygame surface to set the background on.
            background_image_path (str): Path to the background image file.
        """
        background_image = pygame.image.load(background_image_path)
        screen.blit(background_image, (0, 0))



