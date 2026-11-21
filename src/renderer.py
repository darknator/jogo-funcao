import pygame
from palette import PALETTE

_FONT_CACHE = {}


def get_font(size, bold=True):
    key = (size, bold)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = pygame.font.SysFont('Arial', size, bold=bold)
    return _FONT_CACHE[key]


def draw_sprite(surface, sprite, x, y, palette=None, scale=1):
    """Desenha um sprite de pixel art. Cada caractere vira um bloco scale x scale."""
    pal = palette if palette else PALETTE
    for row, line in enumerate(sprite):
        for col, ch in enumerate(line):
            if ch in pal and pal[ch] is not None:
                pygame.draw.rect(surface, pal[ch], (x + col * scale, y + row * scale, scale, scale))


def draw_text(surface, text, x, y, size=12, color=(60, 60, 70), center=False):
    font = get_font(size)
    surf = font.render(text, True, color)
    if center:
        rect = surf.get_rect(center=(x, y))
        surface.blit(surf, rect)
    else:
        surface.blit(surf, (x, y))


def draw_bow(surface, x, y, level=0, pull=0.0):
    from palette import BOW_LEVELS
    color = BOW_LEVELS[level]['color']
    pull_px = int(pull * 8)
    cord_x = x - 8 - pull_px

    pygame.draw.line(surface, (140, 120, 100), (x - 8, y - 12), (cord_x, y), 2)
    pygame.draw.line(surface, (140, 120, 100), (cord_x, y), (x - 8, y + 12), 2)
    pygame.draw.arc(surface, color, (x - 16, y - 16, 24, 32), -1.4, 1.4, 3)

    arrow_x = cord_x + 3 if pull > 0.01 else x + 8
    pygame.draw.line(surface, (80, 60, 40), (arrow_x, y), (x + 16, y), 2)
    pygame.draw.polygon(surface, (40, 40, 40), [(x + 16, y), (x + 22, y - 3), (x + 22, y + 3)])