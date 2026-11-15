import pygame
from config import INTERNAL_W
from palette import UI_BG, UI_GOLD, UI_TEXT, UI_TEXT_SHADOW
from renderer import draw_text

TOPICS = [
    ("Funcoes", ["y = c", "y = ax + b", "y = ax^2 + bx + c"]),
    ("Limites", ["O valor que a funcao", "se aproxima quando x", "tende a um numero."]),
    ("Derivadas", ["A taxa de variacao", "instantanea.", "f'(x)"]),
    ("Integrais", ["A area sob a curva.", "Soma infinita de", "pequenas partes."])
]


def draw(surface):
    surface.fill(UI_BG)


    draw_text(surface, "APRENDER MATEMATICA", INTERNAL_W // 2, 20, 24, UI_GOLD, center=True)


    for i, (title, lines) in enumerate(TOPICS):
        x = 10 + (i % 2) * 155
        y = 60 + (i // 2) * 75


        pygame.draw.rect(surface, (50, 50, 60), (x, y, 145, 65))
        pygame.draw.rect(surface, (100, 100, 110), (x, y, 145, 65), 2)

        draw_text(surface, title, x + 72, y + 12, 14, (255, 255, 255), center=True)

        for j, line in enumerate(lines):
            draw_text(surface, line, x + 72, y + 30 + j * 12, 10, (200, 200, 200), center=True)


    draw_text(surface, "[ ESC ] Voltar ao Menu", INTERNAL_W // 2, 220, 12, UI_TEXT, center=True)