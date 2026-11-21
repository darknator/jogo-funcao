import pygame
from config import INTERNAL_W
from palette import UI_BG, UI_GOLD, UI_TEXT
from renderer import draw_text
from menu import draw_mc_button

TOPICS_DATA = [
    {
        "title": "Funções",
        "desc": "O que é uma função e como ela dita a trajetória.",
        "content": (
            "Uma função é uma regra que transforma um número de entrada (x) em um número de saída (y).\n\n"
            "No jogo, a flecha segue a função y = f(x). O 'x' é a distância horizontal e o 'y' é a altura da flecha naquele ponto.\n\n"
            "Se y = 3 (função constante), a flecha voa reta na altura 3.\n"
            "Se y = 2*x + 1 (função afim), a flecha sobe 2 unidades para cada 1 unidade que avança.\n\n"
            "Dica: Use o botão 'PREVISÃO' no jogo para ver o desenho da sua função antes de atirar!"
        )
    },
    {
        "title": "Derivadas",
        "desc": "A inclinação da trajetória em cada ponto.",
        "content": (
            "A derivada mede a taxa de variação: quão rápido o 'y' muda quando o 'x' muda.\n\n"
            "Se a função é a sua trajetória, a derivada é a INCLINAÇÃO da flecha naquele exato momento.\n\n"
            "No capítulo 2 do jogo, você recebe uma função f(x) e precisa digitar a derivada f'(x). A flecha segue a curva da derivada.\n\n"
            "Regras básicas:\n"
            "- Derivada de constante: 0\n"
            "- Derivada de x: 1\n"
            "- Derivada de a*x: a\n"
            "- Derivada de x^n: n*x^(n-1)\n"
            "- Derivada de e^x: e^x\n\n"
            "Exemplo: se f(x) = x^2, então f'(x) = 2*x. A flecha vai seguir a reta y = 2*x."
        )
    },
    {
        "title": "Limites",
        "desc": "Para onde a função está indo?",
        "content": (
            "O limite é o valor para o qual a função 'tende' quando x se aproxima de um certo número.\n\n"
            "Imagine que você caminha em direção a uma parede. Você chega muito perto, mas não atravessa. O limite é a parede.\n\n"
            "No futuro do jogo, os alvos começarão a se mover. Para acertar, você não vai mirar onde ele está, mas sim onde ele VAI ESTAR (o limite da trajetória).\n\n"
            "Limites também ajudam a entender o que acontece quando as coisas explodem (tendem ao infinito)."
        )
    },
    {
        "title": "Integrais",
        "desc": "A área embaixo do voo da flecha.",
        "content": (
            "A integral é o cálculo da área sob a curva de uma função.\n\n"
            "Imagine pintar todo o espaço entre a trajetória da flecha e o chão. A integral calcula esse espaço.\n\n"
            "Na prática, a integral acumula coisas. Se a função for a velocidade de um carro, a integral da velocidade pelo tempo é a distância total percorrida.\n\n"
            "A integral definida vai do ponto A ao ponto B (como do arqueiro até o alvo). A integral indefinida gera uma nova função."
        )
    }
]


def wrap_text(text, font, max_width):
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                if current_line.strip():
                    lines.append(current_line)
                current_line = word + " "
        if current_line.strip():
            lines.append(current_line)
    return lines


def draw(surface, state, mouse_pos, scale):
    surface.fill(UI_BG)
    for y in range(0, 480, 16):
        for x in range(0, 640, 16):
            if (x + y) % 32 == 0:
                pygame.draw.rect(surface, (40, 40, 40), (x, y, 8, 8))

    mx, my = mouse_pos[0] // scale, mouse_pos[1] // scale
    action = None

    if state == 'grid':
        draw_text(surface, "APRENDER", INTERNAL_W // 2, 50, 48, UI_GOLD, center=True)
        draw_text(surface, "Escolha um topico para estudar:", INTERNAL_W // 2, 90, 24, UI_TEXT, center=True)

        for i, topic in enumerate(TOPICS_DATA):
            x = 20 + (i % 2) * 310
            y = 130 + (i // 2) * 130

            hover = x <= mx <= x + 290 and y <= my <= y + 110
            color = (70, 70, 80) if hover else (50, 50, 60)

            pygame.draw.rect(surface, color, (x, y, 290, 110))
            pygame.draw.rect(surface, (150, 150, 160) if hover else (100, 100, 110), (x, y, 290, 110), 3)

            draw_text(surface, topic["title"], x + 145, y + 24, 32, (255, 255, 255), center=True)

            font_desc = pygame.font.SysFont('Arial', 18)
            lines = wrap_text(topic["desc"], font_desc, 270)
            for j, line in enumerate(lines[:3]):
                draw_text(surface, line, x + 145, y + 60 + j * 24, 18, (200, 200, 200), center=True)

            if pygame.mouse.get_pressed()[0] and hover:
                action = i
                pygame.time.wait(200)

        # BOTÃO VOLTAR
        btn_voltar = (INTERNAL_W // 2 - 100, 410, 200, 50)
        hover_voltar = (btn_voltar[0] <= mx <= btn_voltar[0] + btn_voltar[2] and
                        btn_voltar[1] <= my <= btn_voltar[1] + btn_voltar[3])
        
        draw_mc_button(surface, *btn_voltar, "VOLTAR", (100, 100, 100), hover_voltar)
        draw_text(surface, "[ ESC ] Voltar", INTERNAL_W // 2, 470, 16, (150, 150, 150), center=True)
        
        if hover_voltar and pygame.mouse.get_pressed()[0]:
            action = "voltar"
            pygame.time.wait(200)

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return "voltar"

    else:
        if not (isinstance(state, int) and 0 <= state < len(TOPICS_DATA)):
            return "voltar_lista"
        topic = TOPICS_DATA[state]

        draw_text(surface, topic["title"].upper(), INTERNAL_W // 2, 40, 44, UI_GOLD, center=True)

        pygame.draw.rect(surface, (240, 240, 240), (30, 80, 580, 320))
        pygame.draw.rect(surface, (100, 100, 100), (30, 80, 580, 320), 3)

        font_content = pygame.font.SysFont('Arial', 22)
        lines = wrap_text(topic["content"], font_content, 540)

        y_offset = 100
        for line in lines:
            if y_offset > 380: break
            surf = font_content.render(line, True, (30, 30, 30))
            surface.blit(surf, (50, y_offset))
            y_offset += 28

        # BOTÃO VOLTAR A LISTA
        btn_voltar = (INTERNAL_W // 2 - 100, 410, 200, 50)
        hover_voltar = (btn_voltar[0] <= mx <= btn_voltar[0] + btn_voltar[2] and
                        btn_voltar[1] <= my <= btn_voltar[1] + btn_voltar[3])
        
        draw_mc_button(surface, *btn_voltar, "VOLTAR", (100, 100, 100), hover_voltar)
        draw_text(surface, "[ ESC ] Voltar a lista", INTERNAL_W // 2, 470, 16, (150, 150, 150), center=True)

        if hover_voltar and pygame.mouse.get_pressed()[0]:
            pygame.time.wait(200)
            return "voltar_lista"

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.time.wait(200)
            return "voltar_lista"

    return action