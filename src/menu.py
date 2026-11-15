import pygame
from config import INTERNAL_W
from palette import (CHAPTER_COLORS, CHAPTER_NAMES, UI_BG, UI_HIGHLIGHT,
                     UI_SHADOW, UI_TEXT, UI_TEXT_SHADOW, UI_GOLD)

TILE_W, TILE_H, TILE_GAP, GRID_COLS = 60, 55, 8, 4


def get_tiles():
    total_w = GRID_COLS * TILE_W + (GRID_COLS - 1) * TILE_GAP
    start_x = (INTERNAL_W - total_w) // 2
    tiles = []
    for i in range(8):
        col, row = i % GRID_COLS, i // GRID_COLS
        x = start_x + col * (TILE_W + TILE_GAP)
        y = 60 + row * (TILE_H + TILE_GAP)
        tiles.append((x, y, TILE_W, TILE_H))
    return tiles


def draw_mc_button(surface, x, y, w, h, title, subtitle, color, locked, stars=0):
    pygame.draw.rect(surface, (20, 20, 20), (x, y, w, h))
    face_color = color if not locked else tuple(c // 3 for c in color)
    pygame.draw.rect(surface, face_color, (x + 2, y + 2, w - 4, h - 4))

    pygame.draw.line(surface, UI_HIGHLIGHT, (x + 2, y + 2), (x + w - 3, y + 2), 2)
    pygame.draw.line(surface, UI_HIGHLIGHT, (x + 2, y + 2), (x + 2, y + h - 3), 2)
    pygame.draw.line(surface, UI_SHADOW, (x + w - 2, y + 2), (x + w - 2, y + h - 2), 2)
    pygame.draw.line(surface, UI_SHADOW, (x + 2, y + h - 2), (x + w - 2, y + h - 2), 2)

    font_big = pygame.font.Font(None, 24)
    text = font_big.render(title, False, UI_TEXT)
    t_shadow = font_big.render(title, False, UI_TEXT_SHADOW)
    text_x = x + (w - text.get_width()) // 2
    surface.blit(t_shadow, (text_x + 1, y + 9))
    surface.blit(text, (text_x, y + 8))

    if not locked and subtitle:
        font_small = pygame.font.Font(None, 10)
        s_text = font_small.render(subtitle, False, UI_TEXT)
        surface.blit(s_text, (x + (w - s_text.get_width()) // 2, y + h - 20))

    if locked:
        pygame.draw.rect(surface, (80, 80, 80), (x + w // 2 - 5, y + h // 2 + 5, 10, 8))
        pygame.draw.arc(surface, (80, 80, 80), (x + w // 2 - 5, y + h // 2 - 2, 10, 10), 0, 3.14, 2)
    else:
        for s in range(3):
            star_color = UI_GOLD if s < stars else (60, 60, 60)
            pygame.draw.polygon(surface, star_color, [
                (x + 15 + s * 12, y + h - 10), (x + 18 + s * 12, y + h - 5), (x + 24 + s * 12, y + h - 5),
                (x + 19 + s * 12, y + h), (x + 21 + s * 12, y + h + 5), (x + 15 + s * 12, y + h + 1),
                (x + 9 + s * 12, y + h + 5), (x + 11 + s * 12, y + h), (x + 6 + s * 12, y + h - 5),
                (x + 12 + s * 12, y + h - 5)
            ])


def draw(surface, save_data):
    surface.fill(UI_BG)
    for y in range(0, 240, 8):
        for x in range(0, 320, 8):
            if (x + y) % 16 == 0:
                pygame.draw.rect(surface, (40, 40, 40), (x, y, 4, 4))

    font_title = pygame.font.Font(None, 30)
    t1 = font_title.render("FUNCTION ARCHER", False, UI_GOLD)
    t1_s = font_title.render("FUNCTION ARCHER", False, UI_TEXT_SHADOW)
    surface.blit(t1_s, ((INTERNAL_W - t1.get_width()) // 2 + 2, 17))
    surface.blit(t1, ((INTERNAL_W - t1.get_width()) // 2, 15))

    for i, (x, y, w, h) in enumerate(get_tiles()):
        chapter_num = i + 1
        unlocked = chapter_num == 1 or (chapter_num - 1) in save_data['chapters_completed']
        draw_mc_button(surface, x, y, w, h, str(chapter_num), CHAPTER_NAMES[i],
                       CHAPTER_COLORS[i], not unlocked, save_data['stars'].get(str(chapter_num), 0))


def hit_test(mouse_pos, scale):
    mx, my = mouse_pos[0] // scale, mouse_pos[1] // scale
    for i, (x, y, w, h) in enumerate(get_tiles()):
        if x <= mx <= x + w and y <= my <= y + h: return i + 1
    return None