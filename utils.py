import pygame


def load_image(filename: str) -> pygame.surface.Surface:
    return pygame.image.load(f"assets/{filename}")


def render_text(
    text: str, size: int = 40, color: list[int] = [255, 255, 255]
) -> pygame.surface.Surface:
    font = pygame.font.SysFont("timesnewroman", size)
    return font.render(text, False, color)
