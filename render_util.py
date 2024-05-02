import pygame


def render_centered(to_render: pygame.Surface, surface: pygame.Surface, position: tuple[int, int]):
    size_x, size_y = to_render.get_size()
    surface.blit(to_render, (position[0] - size_x // 2, position[1] - size_y // 2))

def render_font_centered(text: str, color: tuple[int, int, int], font: pygame.font.Font, surface: pygame.Surface, position: tuple[int, int]):
    rendered_font = font.render(text, True, color)
    render_centered(rendered_font, surface, position)

def calculate_scale_ratio(scale_img_dim: tuple[int, int], scale_to_dim: tuple[int, int]):
    return (scale_to_dim[0] / scale_img_dim[0], scale_to_dim[1] / scale_img_dim[1])

def scale_surface(ratio_x: float, surface: pygame.Surface):
    return pygame.transform.smoothscale(surface, (surface.get_size()[0] * ratio_x, surface.get_size()[1] * ratio_x))