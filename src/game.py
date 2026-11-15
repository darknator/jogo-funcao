import pygame
import math
from config import *
from palette import *
from sprites import STEVE, TARGET, MARIO_GROUND
from renderer import draw_sprite, draw_text, draw_bow

PHASES = [
    {
        'id': '1-1', 'chapter': 1, 'archer': {'x': 0, 'y': 3}, 'target': {'x': 8, 'y': 3, 'r': 0.8},
        'obstacles': [], 'tip': 'A flecha precisa manter a altura exata de y = 3.'
    },
    {
        'id': '1-2', 'chapter': 1, 'archer': {'x': 0, 'y': 2}, 'target': {'x': 10, 'y': 2, 'r': 0.8},
        'obstacles': [{'type': 'pipe', 'x': 5, 'y': 0, 'h': 2.5}],
        'tip': 'Para passar pelo cano, y deve ser constante em 2.'
    }
]

KEYS = [
    ['7', '8', '9', '^', 'C'],
    ['4', '5', '6', '*', '<'],
    ['1', '2', '3', '-', 'x'],
    ['0', '.', '+', '/', '=']
]


def safe_eval(eq_str, x_val):
    try:
        eq = eq_str.replace('^', '**')
        return eval(eq, {"__builtins__": None}, {"x": x_val, "math": math})
    except:
        return -99


def world_to_px(x, y): return (GAME_X + int(x * GAME_UNIT), GAME_Y - int(y * GAME_UNIT))


def draw_mario_bg(surface):

    surface.fill(MARIO_SKY)


    for cx, cy in [(30, 40), (150, 60), (260, 30)]:
        pygame.draw.rect(surface, (255, 255, 255), (cx, cy, 30, 10))
        pygame.draw.rect(surface, (255, 255, 255), (cx + 5, cy - 5, 20, 10))
        pygame.draw.rect(surface, (255, 255, 255), (cx + 10, cy - 10, 10, 10))


    for bx, by in [(10, GAME_Y - 15), (120, GAME_Y - 20), (250, GAME_Y - 12)]:
        pygame.draw.rect(surface, MARIO_PIPE_GREEN, (bx, by, 40, 20))
        pygame.draw.circle(surface, MARIO_PIPE_GREEN, (bx + 10, by), 10)
        pygame.draw.circle(surface, MARIO_PIPE_GREEN, (bx + 30, by), 10)
        pygame.draw.circle(surface, MARIO_PIPE_GREEN, (bx + 20, by - 10), 15)


    for gx in range(0, 22):
        px, _ = world_to_px(gx, 0)
        pygame.draw.line(surface, (150, 180, 240), (px, 0), (px, GAME_Y), 1)

    for gy in range(0, 11):
        _, py = world_to_px(0, gy)
        pygame.draw.line(surface, (150, 180, 240), (GAME_X, py), (INTERNAL_W, py), 1)


    _, y0 = world_to_px(0, 0)
    pygame.draw.line(surface, (80, 80, 80), (GAME_X, y0), (INTERNAL_W, y0), 2)  # Eixo X
    pygame.draw.line(surface, (80, 80, 80), (GAME_X, 0), (GAME_X, y0), 2)  # Eixo Y


    ground_pal = {'L': MARIO_GROUND_LIGHT, 'D': MARIO_GROUND_MAIN}
    for x in range(0, INTERNAL_W, 16):
        for y in range(GAME_Y, INTERNAL_H, 16):
            draw_sprite(surface, MARIO_GROUND, x, y, ground_pal)
    pygame.draw.line(surface, (0, 0, 0), (0, GAME_Y), (INTERNAL_W, GAME_Y), 2)


def draw_obstacle(surface, obs):
    px, py = world_to_px(obs['x'], obs['y'])
    if obs['type'] == 'pipe':
        pipe_w = 16;
        pipe_h = int(obs['h'] * GAME_UNIT)
        pygame.draw.rect(surface, MARIO_PIPE_GREEN, (px, py - pipe_h, pipe_w, pipe_h))
        pygame.draw.rect(surface, MARIO_PIPE_DARK, (px + pipe_w - 4, py - pipe_h, 4, pipe_h))
        pygame.draw.rect(surface, MARIO_PIPE_GREEN, (px - 2, py - pipe_h - 8, pipe_w + 4, 8))
        pygame.draw.rect(surface, MARIO_PIPE_DARK, (px + pipe_w - 2, py - pipe_h - 8, 4, 8))
        pygame.draw.rect(surface, (0, 0, 0), (px - 2, py - pipe_h - 8, pipe_w + 4, 8), 1)


def play(window, surface, clock, chapter_num):
    phase = PHASES[0]
    input_text = "y="
    show_preview = False
    anim = {'phase': 'idle', 'pull': 0, 'start': 0, 'arrow_x': 0, 'arrow_y': 0, 'hit': False, 'impact_start': 0}
    result_msg = None
    error_reason = ""
    attempts = 2

    while True:
        clock.tick(60)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return 'menu'
                if event.key == pygame.K_RETURN and anim['phase'] == 'idle' and result_msg is None:
                    anim['phase'] = 'pull';
                    anim['start'] = now
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1] if len(input_text) > 2 else "y="

        draw_mario_bg(surface)
        for obs in phase['obstacles']: draw_obstacle(surface, obs)

        ax, ay = world_to_px(phase['archer']['x'], phase['archer']['y'])
        draw_sprite(surface, STEVE, ax - 9, ay - 8)
        draw_bow(surface, ax, ay, 0, anim['pull'] if anim['phase'] == 'pull' else 0)
        tx, ty = world_to_px(phase['target']['x'], phase['target']['y'])
        draw_sprite(surface, TARGET, tx - 8, ty - 8)

        if show_preview and anim['phase'] == 'idle' and result_msg is None:
            try:
                expr = input_text.replace("y=", "")
                for px_x in range(0, 15):
                    for step in range(2):
                        px_val = px_x + step * 0.5
                        py_val = safe_eval(expr, px_val)
                        if -5 < py_val < 20:
                            sx, sy = world_to_px(px_val, py_val)
                            pygame.draw.circle(surface, (106, 76, 147), (sx, sy), 1)
            except:
                pass

        if anim['phase'] == 'pull':
            t = (now - anim['start']) / 300.0
            anim['pull'] = min(1, t)
            if t >= 1.1: anim['phase'], anim['start'] = 'fly', now
        elif anim['phase'] == 'fly':
            t = (now - anim['start']) / 1000.0
            expr = input_text.replace("y=", "")
            ax = phase['archer']['x'] + t * 12
            ay = safe_eval(expr, ax)
            anim['arrow_x'], anim['arrow_y'] = ax, ay

            if math.hypot(ax - phase['target']['x'], ay - phase['target']['y']) < phase['target']['r']:
                anim['phase'], anim['hit'], anim['impact_start'] = 'impact', True, now
            elif ax > phase['target']['x'] + 2 or ay < -2:
                anim['phase'], anim['hit'], anim['impact_start'] = 'impact', False, now

        elif anim['phase'] == 'impact' and (now - anim['impact_start']) > 500:
            result_msg = 'hit' if anim['hit'] else 'miss'
            if not anim['hit']:
                attempts -= 1
                expr = input_text.replace("y=", "")
                y_no_alvo = safe_eval(expr, phase['target']['x'])

                if y_no_alvo == -99:
                    error_reason = "Erro na sintaxe! Verifique se digitou a funcao corretamente."
                elif y_no_alvo < phase['target']['y'] - phase['target']['r']:
                    error_reason = f"Passou por BAIXO. No alvo (x={phase['target']['x']}), ela estava em y={y_no_alvo:.1f}. Aumente a altura."
                elif y_no_alvo > phase['target']['y'] + phase['target']['r']:
                    error_reason = f"Passou por CIMA. No alvo (x={phase['target']['x']}), ela estava em y={y_no_alvo:.1f}. Diminua a altura."
                else:
                    error_reason = "A flecha caiu antes ou bateu em um obstaculo!"
            anim['phase'] = 'done'

        if anim['phase'] in ('fly', 'impact'):
            fx, fy = world_to_px(anim['arrow_x'], anim['arrow_y'])
            pygame.draw.line(surface, (80, 60, 40), (fx - 5, fy), (fx + 5, fy), 2)


        pygame.draw.rect(surface, (30, 30, 40), (0, 160, INTERNAL_W, 80))
        pygame.draw.line(surface, (100, 100, 110), (0, 160), (INTERNAL_W, 160), 2)

        pygame.draw.rect(surface, (255, 255, 255), (10, 165, 150, 22))
        pygame.draw.rect(surface, (100, 100, 100), (10, 165, 150, 22), 1)
        draw_text(surface, input_text, 15, 172, 18, (0, 0, 0))

        mx, my = pygame.mouse.get_pos()
        mx, my = mx // SCALE, my // SCALE
        clicked_key = None

        for r, row in enumerate(KEYS):
            for c, key in enumerate(row):
                kx = 10 + c * 24
                ky = 192 + r * 11
                kw, kh = 22, 9

                color = (220, 220, 220)
                text_color = (0, 0, 0)

                if kx <= mx <= kx + kw and ky <= my <= ky + kh:
                    color = (255, 255, 150)
                    if pygame.mouse.get_pressed()[0]: clicked_key = key

                pygame.draw.rect(surface, color, (kx, ky, kw, kh))
                pygame.draw.rect(surface, (150, 150, 150), (kx, ky, kw, kh), 1)
                draw_text(surface, key, kx + kw // 2, ky + kh // 2, 11, text_color, center=True)

        btn_prev = (165, 170, 140, 25)
        btn_fire = (165, 205, 140, 25)

        pygame.draw.rect(surface, (69, 123, 157), btn_prev)
        pygame.draw.rect(surface, (100, 160, 200), btn_prev, 2)
        draw_text(surface, "PREVISAO", btn_prev[0] + 70, btn_prev[1] + 12, 14, (255, 255, 255), center=True)

        pygame.draw.rect(surface, (200, 50, 50), btn_fire)
        pygame.draw.rect(surface, (255, 100, 100), btn_fire, 2)
        draw_text(surface, "ATIRAR", btn_fire[0] + 70, btn_fire[1] + 12, 14, (255, 255, 255), center=True)

        if pygame.mouse.get_pressed()[0]:
            if btn_prev[0] <= mx <= btn_prev[0] + btn_prev[2] and btn_prev[1] <= my <= btn_prev[1] + btn_prev[3]:
                show_preview = not show_preview
                pygame.time.wait(150)
            elif btn_fire[0] <= mx <= btn_fire[0] + btn_fire[2] and btn_fire[1] <= my <= btn_fire[1] + btn_fire[3]:
                if anim['phase'] == 'idle' and result_msg is None:
                    anim['phase'] = 'pull';
                    anim['start'] = now
                    show_preview = False
                pygame.time.wait(150)
            elif clicked_key:
                if clicked_key == 'C':
                    input_text = "y="
                elif clicked_key == '<':
                    input_text = input_text[:-1] if len(input_text) > 2 else "y="
                elif clicked_key == '=':
                    pass
                else:
                    if len(input_text) < 15: input_text += clicked_key
                pygame.time.wait(100)

        pygame.draw.rect(surface, (0, 0, 0), (0, 0, 120, 20))
        draw_text(surface, f"Tentativas: {attempts}/2", 5, 5, 16, (255, 255, 255))

        if result_msg:
            overlay = pygame.Surface((INTERNAL_W, INTERNAL_H));
            overlay.set_alpha(200);
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            msg = "ACERTOU!" if result_msg == 'hit' else "ERROU!"
            color = (42, 157, 143) if result_msg == 'hit' else (230, 57, 70)

            draw_text(surface, msg, INTERNAL_W // 2, 70, 30, color, center=True)

            final_tip = error_reason if result_msg == 'miss' else phase['tip']

            font = pygame.font.SysFont('Arial', 12)
            words = final_tip.split(' ')
            lines, current = [], ""
            for w in words:
                if font.size(current + w + " ")[0] < 280:
                    current += w + " "
                else:
                    lines.append(current); current = w + " "
            lines.append(current)

            for i, line in enumerate(lines):
                draw_text(surface, line, INTERNAL_W // 2, 110 + i * 18, 12, (255, 255, 255), center=True)

            draw_text(surface, "Clique para continuar", INTERNAL_W // 2, 200, 14, (200, 200, 200), center=True)

            if pygame.mouse.get_pressed()[0]:
                if result_msg == 'hit':
                    return 'menu'
                elif attempts <= 0:
                    return 'menu'
                else:
                    attempts, result_msg, show_preview = 2, None, False
                    anim = {'phase': 'idle', 'pull': 0, 'start': 0, 'arrow_x': 0, 'arrow_y': 0, 'hit': False,
                            'impact_start': 0}
                pygame.time.wait(200)

        scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
        window.blit(scaled, (0, 0))
        pygame.display.flip()