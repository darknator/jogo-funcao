import pygame
from palette import PALETTE


def draw_sprite(surface, sprite, x, y, palette=None):
    pal = palette if palette else PALETTE
    for row, line in enumerate(sprite):
        for col, ch in enumerate(line):
            if ch in pal and pal[ch] is not None:
                pygame.draw.rect(surface, pal[ch], (x + col, y + row, 1, 1))



def draw_text(surface, text, x, y, size=12, color=(60, 60, 70), center=False):

    font = pygame.font.SysFont('Arial', size, bold=True)
    surf = font.render(text, True, color)
    if center:
        rect = surf.get_rect(center=(x, y))
        surface.blit(surf, rect)
    else:
        surface.blit(surf, (x, y))


def draw_bow(surface, x, y, level=0, pull=0.0):
    from palette import BOW_LEVELS
    color = BOW_LEVELS[level]['color']
    pull_px = int(pull * 6)
    cord_x = x - 6 - pull_px

    pygame.draw.line(surface, (140, 120, 100), (x - 6, y - 8), (cord_x, y), 1)
    pygame.draw.line(surface, (140, 120, 100), (cord_x, y), (x - 6, y + 8), 1)
    pygame.draw.arc(surface, color, (x - 12, y - 12, 16, 24), -1.4, 1.4, 2)

    arrow_x = cord_x + 2 if pull > 0.01 else x + 6
    pygame.draw.line(surface, (80, 60, 40), (arrow_x, y), (x + 10, y), 1)
    pygame.draw.polygon(surface, (40, 40, 40), [(x + 10, y), (x + 13, y - 2), (x + 13, y + 2)])