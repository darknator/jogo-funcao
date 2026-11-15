import pygame
from config import INTERNAL_W
from palette import (CHAPTER_COLORS, CHAPTER_NAMES, UI_BG, UI_HIGHLIGHT,
                     UI_SHADOW, UI_TEXT, UI_TEXT_SHADOW, UI_GOLD)
from renderer import draw_text

TILE_W, TILE_H, TILE_GAP, GRID_COLS = 60, 55, 8, 4


def draw_mc_button(surface, x, y, w, h, text, color, hover=False):
    pygame.draw.rect(surface, (20, 20, 20), (x, y, w, h))
    face_color = tuple(min(255, c + 30) for c in color) if hover else color
    pygame.draw.rect(surface, face_color, (x + 2, y + 2, w - 4, h - 4))

    pygame.draw.line(surface, UI_HIGHLIGHT, (x + 2, y + 2), (x + w - 3, y + 2), 2)
    pygame.draw.line(surface, UI_HIGHLIGHT, (x + 2, y + 2), (x + 2, y + h - 3), 2)
    pygame.draw.line(surface, UI_SHADOW, (x + w - 2, y + 2), (x + w - 2, y + h - 2), 2)
    pygame.draw.line(surface, UI_SHADOW, (x + 2, y + h - 2), (x + w - 2, y + h - 2), 2)

    draw_text(surface, text, x + w // 2, y + h // 2, 20, (255, 255, 255), center=True)


def draw_main_menu(surface, mouse_pos, scale):
    surface.fill(UI_BG)
    # Fundo texturizado
    for y in range(0, 240, 8):
        for x in range(0, 320, 8):
            if (x + y) % 16 == 0: pygame.draw.rect(surface, (40, 40, 40), (x, y, 4, 4))

    draw_text(surface, "FUNCTION ARCHER", INTERNAL_W // 2, 40, 30, UI_GOLD, center=True)
    draw_text(surface, "O Jogo das Funcoes", INTERNAL_W // 2, 70, 14, UI_TEXT, center=True)

    mx, my = mouse_pos[0] // scale, mouse_pos[1] // scale

    btn_jogar = (INTERNAL_W // 2 - 60, 110, 120, 40)
    btn_aprender = (INTERNAL_W // 2 - 60, 160, 120, 40)

    hover_jogar = btn_jogar[0] <= mx <= btn_jogar[0] + btn_jogar[2] and btn_jogar[1] <= my <= btn_jogar[1] + btn_jogar[
        3]
    hover_aprender = btn_aprender[0] <= mx <= btn_aprender[0] + btn_aprender[2] and btn_aprender[1] <= my <= \
                     btn_aprender[1] + btn_aprender[3]

    draw_mc_button(surface, *btn_jogar, "JOGAR", (69, 123, 157), hover_jogar)
    draw_mc_button(surface, *btn_aprender, "APRENDER", (90, 143, 95), hover_aprender)

    return btn_jogar, btn_aprender


def get_tiles():
    total_w = GRID_COLS * TILE_W + (GRID_COLS - 1) * TILE_GAP
    start_x = (INTERNAL_W - total_w) // 2
    return [
        (start_x + (i % GRID_COLS) * (TILE_W + TILE_GAP), 60 + (i // GRID_COLS) * (TILE_H + TILE_GAP), TILE_W, TILE_H)
        for i in range(8)]


def draw_chapter_select(surface, save_data, mouse_pos, scale):
    surface.fill(UI_BG)
    for y in range(0, 240, 8):
        for x in range(0, 320, 8):
            if (x + y) % 16 == 0: pygame.draw.rect(surface, (40, 40, 40), (x, y, 4, 4))

    draw_text(surface, "SELECIONE O MUNDO", INTERNAL_W // 2, 20, 20, UI_GOLD, center=True)
    draw_text(surface, "[ ESC ] Voltar", INTERNAL_W // 2, 220, 12, UI_TEXT, center=True)

    mx, my = mouse_pos[0] // scale, mouse_pos[1] // scale
    for i, (x, y, w, h) in enumerate(get_tiles()):
        ch = i + 1
        unlocked = ch == 1 or (ch - 1) in save_data['chapters_completed']
        hover = x <= mx <= x + w and y <= my <= y + h

        color = CHAPTER_COLORS[i] if unlocked else tuple(c // 3 for c in CHAPTER_COLORS[i])

        # Botão do mundo
        pygame.draw.rect(surface, (20, 20, 20), (x, y, w, h))
        pygame.draw.rect(surface, color, (x + 2, y + 2, w - 4, h - 4))
        if hover and unlocked:
            pygame.draw.rect(surface, (255, 255, 255), (x + 2, y + 2, w - 4, h - 4), 2)

        draw_text(surface, str(ch), x + w // 2, y + 15, 20, (255, 255, 255), center=True)
        if unlocked:
            draw_text(surface, CHAPTER_NAMES[i][:8], x + w // 2, y + h - 15, 8, (255, 255, 255), center=True)
        else:
            draw_text(surface, "LOCK", x + w // 2, y + h - 15, 10, (150, 150, 150), center=True)


def hit_test(mouse_pos, scale, is_main_menu=False):
    mx, my = mouse_pos[0] // scale, mouse_pos[1] // scale
    if is_main_menu:
        if 110 <= my <= 150 and 100 <= mx <= 220: return "jogar"
        if 160 <= my <= 200 and 100 <= mx <= 220: return "aprender"
        return None
    else:
        for i, (x, y, w, h) in enumerate(get_tiles()):
            if x <= mx <= x + w and y <= my <= y + h: return i + 1
        return None