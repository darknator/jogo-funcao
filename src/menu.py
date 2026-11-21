import pygame
from config import INTERNAL_W
from palette import (CHAPTER_COLORS, CHAPTER_NAMES, UI_BG, UI_HIGHLIGHT,
                     UI_SHADOW, UI_TEXT, UI_TEXT_SHADOW, UI_GOLD, BTN_PRACTICE)
from renderer import draw_text

# Tamanho dos botões (menus de mundos)
TILE_W, TILE_H = 180, 120
TILE_GAP_X, TILE_GAP_Y = 20, 20
GRID_COLS = 2


def draw_mc_button(surface, x, y, w, h, text, color, hover=False):
    pygame.draw.rect(surface, (20, 20, 20), (x, y, w, h))
    face_color = tuple(min(255, c + 30) for c in color) if hover else color
    pygame.draw.rect(surface, face_color, (x + 4, y + 4, w - 8, h - 8))

    pygame.draw.line(surface, UI_HIGHLIGHT, (x + 4, y + 4), (x + w - 6, y + 4), 3)
    pygame.draw.line(surface, UI_HIGHLIGHT, (x + 4, y + 4), (x + 4, y + h - 6), 3)
    pygame.draw.line(surface, UI_SHADOW, (x + w - 4, y + 4), (x + w - 4, y + h - 4), 3)
    pygame.draw.line(surface, UI_SHADOW, (x + 4, y + h - 4), (x + w - 4, y + h - 4), 3)

    draw_text(surface, text, x + w // 2, y + h // 2, 32, (255, 255, 255), center=True)


def draw_main_menu(surface, mouse_pos, scale):
    surface.fill(UI_BG)
    for y in range(0, 480, 16):
        for x in range(0, 640, 16):
            if (x + y) % 32 == 0:
                pygame.draw.rect(surface, (40, 40, 40), (x, y, 8, 8))

    draw_text(surface, "FUNCTION ARCHER", INTERNAL_W // 2, 60, 60, UI_GOLD, center=True)
    draw_text(surface, "O Jogo das Funcoes", INTERNAL_W // 2, 110, 28, UI_TEXT, center=True)

    mx, my = mouse_pos[0] // scale, mouse_pos[1] // scale

    btn_jogar = (INTERNAL_W // 2 - 120, 170, 240, 70)
    btn_praticar = (INTERNAL_W // 2 - 120, 260, 240, 70)
    btn_aprender = (INTERNAL_W // 2 - 120, 350, 240, 70)

    hover_jogar = (btn_jogar[0] <= mx <= btn_jogar[0] + btn_jogar[2] and
                   btn_jogar[1] <= my <= btn_jogar[1] + btn_jogar[3])
    hover_praticar = (btn_praticar[0] <= mx <= btn_praticar[0] + btn_praticar[2] and
                      btn_praticar[1] <= my <= btn_praticar[1] + btn_praticar[3])
    hover_aprender = (btn_aprender[0] <= mx <= btn_aprender[0] + btn_aprender[2] and
                      btn_aprender[1] <= my <= btn_aprender[1] + btn_aprender[3])

    draw_mc_button(surface, *btn_jogar, "JOGAR", (69, 123, 157), hover_jogar)
    draw_mc_button(surface, *btn_praticar, "PRATICAR", BTN_PRACTICE, hover_praticar)
    draw_mc_button(surface, *btn_aprender, "APRENDER", (90, 143, 95), hover_aprender)

    return btn_jogar, btn_praticar, btn_aprender


def draw_practice_select(surface, mouse_pos, scale):
    surface.fill(UI_BG)
    for y in range(0, 480, 16):
        for x in range(0, 640, 16):
            if (x + y) % 32 == 0:
                pygame.draw.rect(surface, (40, 40, 40), (x, y, 8, 8))

    draw_text(surface, "MODO PRATICAR", INTERNAL_W // 2, 60, 44, UI_GOLD, center=True)
    draw_text(surface, "O que voce quer praticar?", INTERNAL_W // 2, 110, 24, UI_TEXT, center=True)

    mx, my = mouse_pos[0] // scale, mouse_pos[1] // scale

    btn_func = (INTERNAL_W // 2 - 200, 180, 180, 120)
    btn_deriv = (INTERNAL_W // 2 + 20, 180, 180, 120)
    btn_voltar = (INTERNAL_W // 2 - 100, 350, 200, 60)

    hover_func = (btn_func[0] <= mx <= btn_func[0] + btn_func[2] and
                  btn_func[1] <= my <= btn_func[1] + btn_func[3])
    hover_deriv = (btn_deriv[0] <= mx <= btn_deriv[0] + btn_deriv[2] and
                   btn_deriv[1] <= my <= btn_deriv[1] + btn_deriv[3])
    hover_voltar = (btn_voltar[0] <= mx <= btn_voltar[0] + btn_voltar[2] and
                    btn_voltar[1] <= my <= btn_voltar[1] + btn_voltar[3])

    draw_mc_button(surface, *btn_func, "FUNCOES", CHAPTER_COLORS[0], hover_func)
    draw_mc_button(surface, *btn_deriv, "DERIVADAS", CHAPTER_COLORS[1], hover_deriv)
    draw_mc_button(surface, *btn_voltar, "VOLTAR", (100, 100, 100), hover_voltar)

    draw_text(surface, "[ ESC ] Voltar ao Menu Principal", INTERNAL_W // 2, 440, 18, (150, 150, 150), center=True)

    return btn_func, btn_deriv, btn_voltar


def get_tiles():
    # Calcula o centro para deixar a grade 2x2 perfeitamente alinhada
    total_w = GRID_COLS * TILE_W + (GRID_COLS - 1) * TILE_GAP_X
    start_x = (INTERNAL_W - total_w) // 2
    start_y = 110 # Posiciona um pouco mais abaixo do titulo

    return [
        (start_x + (i % GRID_COLS) * (TILE_W + TILE_GAP_X),
         start_y + (i // GRID_COLS) * (TILE_H + TILE_GAP_Y),
         TILE_W, TILE_H)
        for i in range(4)
    ]


def draw_lock_icon(surface, cx, cy, color=(200, 200, 200)):
    pygame.draw.rect(surface, color, (cx - 8, cy, 16, 14))
    pygame.draw.rect(surface, color, (cx - 4, cy - 8, 8, 10), 3)
    pygame.draw.rect(surface, (30, 30, 30), (cx - 2, cy + 4, 4, 6))


def draw_chapter_select(surface, save_data, mouse_pos, scale):
    surface.fill(UI_BG)
    for y in range(0, 480, 16):
        for x in range(0, 640, 16):
            if (x + y) % 32 == 0:
                pygame.draw.rect(surface, (40, 40, 40), (x, y, 8, 8))

    draw_text(surface, "SELECIONE O MUNDO", INTERNAL_W // 2, 50, 40, UI_GOLD, center=True)
    
    mx, my = mouse_pos[0] // scale, mouse_pos[1] // scale
    
    for i, (x, y, w, h) in enumerate(get_tiles()):
        ch = i + 1
        
        if ch <= 2:
            unlocked = ch == 1 or (ch - 1) in save_data['chapters_completed']
            color = CHAPTER_COLORS[i] if unlocked else tuple(c // 3 for c in CHAPTER_COLORS[i])
            hover = x <= mx <= x + w and y <= my <= y + h

            pygame.draw.rect(surface, (20, 20, 20), (x, y, w, h))
            pygame.draw.rect(surface, color, (x + 4, y + 4, w - 8, h - 8))
            
            if hover and unlocked:
                pygame.draw.rect(surface, (255, 255, 255), (x + 4, y + 4, w - 8, h - 8), 3)

            draw_text(surface, str(ch), x + w // 2, y + 35, 40, (255, 255, 255), center=True)

            if unlocked:
                draw_text(surface, CHAPTER_NAMES[i], x + w // 2, y + h - 30, 20, (255, 255, 255), center=True)
                stars = save_data['stars'].get(str(ch), 0)
                if stars > 0:
                    for s in range(3):
                        sc = UI_GOLD if s < stars else (80, 80, 80)
                        pygame.draw.circle(surface, sc, (x + w - 40 + s * 12, y + 20), 5)
            else:
                draw_text(surface, "BLOQUEADO", x + w // 2, y + h - 30, 18, (150, 150, 150), center=True)
        
        else:
            pygame.draw.rect(surface, (20, 20, 20), (x, y, w, h))
            pygame.draw.rect(surface, (40, 40, 50), (x + 4, y + 4, w - 8, h - 8))
            
            draw_lock_icon(surface, x + w // 2, y + h // 2 - 10, (100, 100, 100))
            draw_text(surface, "EM BREVE", x + w // 2, y + h - 30, 18, (100, 100, 100), center=True)
            draw_text(surface, str(ch), x + 15, y + 15, 24, (60, 60, 70))

    # BOTÃO VOLTAR CLICÁVEL
    btn_voltar = (INTERNAL_W // 2 - 100, 390, 200, 50)
    hover_voltar = (btn_voltar[0] <= mx <= btn_voltar[0] + btn_voltar[2] and
                    btn_voltar[1] <= my <= btn_voltar[1] + btn_voltar[3])
    
    draw_mc_button(surface, *btn_voltar, "VOLTAR", (100, 100, 100), hover_voltar)
    draw_text(surface, "[ ESC ] Voltar", INTERNAL_W // 2, 460, 16, (150, 150, 150), center=True)

    return btn_voltar


def hit_test(mouse_pos, scale, is_main_menu=False):
    mx, my = mouse_pos[0] // scale, mouse_pos[1] // scale
    if is_main_menu:
        if 170 <= my <= 240 and 200 <= mx <= 440:
            return "jogar"
        if 260 <= my <= 330 and 200 <= mx <= 440:
            return "praticar"
        if 350 <= my <= 420 and 200 <= mx <= 440:
            return "aprender"
        return None
    else:
        for i, (x, y, w, h) in enumerate(get_tiles()):
            if x <= mx <= x + w and y <= my <= y + h:
                if i + 1 <= 2:
                    return i + 1
                else:
                    return None
        return None