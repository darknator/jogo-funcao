import pygame
import math
from config import *
from palette import *
from sprites import STEVE, TARGET, MARIO_GROUND, GOOMBA
from renderer import draw_sprite, draw_text, draw_bow
import save as savemod

PHASES = [
    {
        'id': '1-1', 'chapter': 1, 'archer': {'x': 0, 'y': 3}, 'target': {'x': 8, 'y': 3, 'r': 0.8},
        'obstacles': [], 'tip': 'Para acertar, a flecha deve manter a altura y = 3.'
    },
    {
        'id': '1-2', 'chapter': 1, 'archer': {'x': 0, 'y': 2}, 'target': {'x': 10, 'y': 2, 'r': 0.8},
        'obstacles': [{'type': 'pipe', 'x': 5, 'y': 0, 'h': 2.5}],
        'tip': 'A flecha deve manter a altura y = 2 para passar por cima do cano.'
    }
]

#
KEYS = [
    ['7', '8', '9', '+', 'C'],
    ['4', '5', '6', '-', '<'],
    ['1', '2', '3', '*', 'x'],
    ['0', '.', '^', '/', '=']
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
            elif ax > phase['target']['x'] + 2 or ay < 0:
                anim['phase'], anim['hit'], anim['impact_start'] = 'impact', False, now
        elif anim['phase'] == 'impact' and (now - anim['impact_start']) > 500:
            result_msg = 'hit' if anim['hit'] else 'miss'
            if not anim['hit']: attempts -= 1
            anim['phase'] = 'done'

        if anim['phase'] in ('fly', 'impact'):
            fx, fy = world_to_px(anim['arrow_x'], anim['arrow_y'])
            pygame.draw.line(surface, (80, 60, 40), (fx - 5, fy), (fx + 5, fy), 2)


        pygame.draw.rect(surface, (40, 40, 50), (0, CARDS_Y - 15, INTERNAL_W, 70))


        pygame.draw.rect(surface, (255, 255, 255), (10, CARDS_Y - 10, 150, 20))
        draw_text(surface, input_text, 15, CARDS_Y - 5, 16, (0, 0, 0))


        mx, my = pygame.mouse.get_pos()
        mx, my = mx // SCALE, my // SCALE
        clicked_key = None

        for r, row in enumerate(KEYS):
            for c, key in enumerate(row):
                kx = 10 + c * 22
                ky = CARDS_Y + 15 + r * 12
                kw, kh = 20, 10

                color = (200, 200, 200)
                if kx <= mx <= kx + kw and ky <= my <= ky + kh:
                    color = (255, 255, 150)
                    if pygame.mouse.get_pressed()[0]:
                        clicked_key = key

                pygame.draw.rect(surface, color, (kx, ky, kw, kh))
                draw_text(surface, key, kx + kw // 2, ky + kh // 2, 10, (0, 0, 0), center=True)


        btn_prev = (130, CARDS_Y + 5, 80, 15)
        btn_fire = (130, CARDS_Y + 25, 80, 15)

        pygame.draw.rect(surface, (69, 123, 157), btn_prev)
        draw_text(surface, "PREVISAO", btn_prev[0] + 40, btn_prev[1] + 7, 10, (255, 255, 255), center=True)

        pygame.draw.rect(surface, (200, 50, 50), btn_fire)
        draw_text(surface, "ATIRAR", btn_fire[0] + 40, btn_fire[1] + 7, 10, (255, 255, 255), center=True)


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
                    pass  #
                else:
                    if len(input_text) < 15: input_text += clicked_key
                pygame.time.wait(100)


        draw_text(surface, f"Tentativas: {attempts}/2", 10, 10, 14, (255, 255, 255))

        
        if result_msg:
            overlay = pygame.Surface((INTERNAL_W, INTERNAL_H));
            overlay.set_alpha(180);
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            msg = "ACERTOU!" if result_msg == 'hit' else "ERROU!"
            color = (42, 157, 143) if result_msg == 'hit' else (230, 57, 70)
            draw_text(surface, msg, INTERNAL_W // 2, 80, 30, color, center=True)
            draw_text(surface, phase['tip'], INTERNAL_W // 2, 120, 14, (255, 255, 255), center=True)
            draw_text(surface, "Clique para continuar", INTERNAL_W // 2, 180, 12, (200, 200, 200), center=True)

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