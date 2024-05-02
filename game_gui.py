import pygame
import cv2
from pygame.transform import scale

TITLE_RESOLUTION = (1440, 1024)

class GameSprite:
    def __init__(self, path: str, position: tuple[int, int]):
        self.sprite = pygame.image.load(path).convert_alpha()
        self.position = position

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.position)

    def was_clicked(self, pos):
        return self.sprite.get_rect(topleft=self.position).collidepoint(pos)


class GameButton(GameSprite):
    def __init__(self, path: str, position: tuple[int, int], on_click):
        GameSprite.__init__(self, path, position)
        self.on_click = on_click

def image_scaled_dim(shape, width=None, height=None):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return shape

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    return dim

# https://stackoverflow.com/a/44659589
def image_resize(image, width = None, height = None, inter = cv2.INTER_LINEAR):
    resized = cv2.resize(image, image_scaled_dim(image.shape, width, height), interpolation = inter)

    # return the resized image
    return resized
