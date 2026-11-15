import pygame
from config import INTERNAL_W
from palette import UI_BG, UI_GOLD, UI_TEXT
from renderer import draw_text


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
        "title": "Derivadas",
        "desc": "A velocidade instantânea e a inclinação.",
        "content": (
            "A derivada mede a taxa de variação. Ou seja, quão rápido o 'y' muda quando o 'x' muda.\n\n"
            "Se a função for a sua trajetória, a derivada é a INCLINAÇÃO da flecha naquele exato momento.\n\n"
            "Quando a flecha está subindo, a derivada é positiva. Quando está caindo, negativa.\n"
            "No topo da curva (o vértice da parábola), a derivada é zero (a flecha fica paralela ao chão por um instante).\n\n"
            "Na física, a derivada da posição é a velocidade, e a derivada da velocidade é a aceleração."
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
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
    return lines


def draw(surface, state, mouse_pos, scale):
    """Retorna a ação 'voltar' ou 'detalhe_X' ou None"""
    surface.fill(UI_BG)

    # Fundo texturizado sutil
    for y in range(0, 240, 8):
        for x in range(0, 320, 8):
            if (x + y) % 16 == 0: pygame.draw.rect(surface, (40, 40, 40), (x, y, 4, 4))

    if state == 'grid':
        draw_text(surface, "APRENDER", INTERNAL_W // 2, 25, 24, UI_GOLD, center=True)
        draw_text(surface, "Escolha um topico para estudar:", INTERNAL_W // 2, 45, 12, UI_TEXT, center=True)

        mx, my = mouse_pos[0] // scale, mouse_pos[1] // scale
        action = None

        for i, topic in enumerate(TOPICS_DATA):
            x = 10 + (i % 2) * 155
            y = 65 + (i // 2) * 75

            hover = x <= mx <= x + 145 and y <= my <= y + 65
            color = (70, 70, 80) if hover else (50, 50, 60)

            pygame.draw.rect(surface, color, (x, y, 145, 65))
            pygame.draw.rect(surface, (150, 150, 160) if hover else (100, 100, 110), (x, y, 145, 65), 2)

            draw_text(surface, topic["title"], x + 72, y + 12, 16, (255, 255, 255), center=True)


            font_desc = pygame.font.SysFont('Arial', 9)
            lines = wrap_text(topic["desc"], font_desc, 135)
            for j, line in enumerate(lines[:3]):
                draw_text(surface, line, x + 72, y + 32 + j * 12, 9, (200, 200, 200), center=True)

            draw_text(surface, "[ Clique para ler ]", x + 72, y + 55, 8, (255, 255, 150) if hover else (150, 150, 150),
                      center=True)

            if pygame.mouse.get_pressed()[0] and hover:
                action = i
                pygame.time.wait(200)

        draw_text(surface, "[ ESC ] Voltar ao Menu Principal", INTERNAL_W // 2, 225, 12, UI_TEXT, center=True)


        if action is not None:
            return action
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return "voltar"

    else:

        topic = TOPICS_DATA[state]

        draw_text(surface, topic["title"].upper(), INTERNAL_W // 2, 20, 22, UI_GOLD, center=True)


        pygame.draw.rect(surface, (240, 240, 240), (15, 45, 290, 165))
        pygame.draw.rect(surface, (100, 100, 100), (15, 45, 290, 165), 2)


        font_content = pygame.font.SysFont('Arial', 11)
        lines = wrap_text(topic["content"], font_content, 270)

        y_offset = 55
        for line in lines:
            if y_offset > 195: break  # Não deixa o texto vazar do quadro
            surf = font_content.render(line, True, (30, 30, 30))
            surface.blit(surf, (25, y_offset))
            y_offset += 14

        draw_text(surface, "[ ESC ] Voltar a lista", INTERNAL_W // 2, 225, 12, UI_TEXT, center=True)

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.time.wait(200)
            return "voltar_lista"

    return None