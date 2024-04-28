import pygame

TITLE_RESOLUTION = (1440, 1024)

class GameSprite:
    def __init__(self, path: str, position: tuple[int, int]):
        self.sprite = pygame.image.load(path)
        self.position = position

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.position)

class GameButton(GameSprite):
    def __init__(self, path: str, position: tuple[int, int], on_click):
        GameSprite.__init__(self, path, position)
        self.on_click = on_click

    def was_clicked(self, pos):
        return self.sprite.get_rect(topleft=self.position).collidepoint(pos)