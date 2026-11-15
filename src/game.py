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
        'obstacles': [],
        'options': [{'a': 0, 'b': 0, 'c': 3}, {'a': 0, 'b': 0.3, 'c': 3}, {'a': 0, 'b': -0.2, 'c': 3}],
        'correct': 0, 'tip': 'y = 3 e uma constante! A flecha mantem a mesma altura.',
    },
    {
        'id': '1-2', 'chapter': 1, 'archer': {'x': 0, 'y': 2}, 'target': {'x': 10, 'y': 2, 'r': 0.8},
        'obstacles': [{'type': 'pipe', 'x': 5, 'y': 0, 'h': 2.5}],
        'options': [{'a': 0, 'b': 0.4, 'c': 2}, {'a': 0, 'b': 0, 'c': 2}, {'a': 0, 'b': -0.4, 'c': 2}],
        'correct': 1, 'tip': 'b = 0 -> a flecha nao sobe nem desce. Passa por cima do cano.',
    }
]

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
        pipe_w = 16; pipe_h = int(obs['h'] * GAME_UNIT)
        pygame.draw.rect(surface, MARIO_PIPE_GREEN, (px, py - pipe_h, pipe_w, pipe_h))
        pygame.draw.rect(surface, MARIO_PIPE_DARK, (px + pipe_w - 4, py - pipe_h, 4, pipe_h))
        pygame.draw.rect(surface, MARIO_PIPE_GREEN, (px - 2, py - pipe_h - 8, pipe_w + 4, 8))
        pygame.draw.rect(surface, MARIO_PIPE_DARK, (px + pipe_w - 2, py - pipe_h - 8, 4, 8))
        pygame.draw.rect(surface, (0,0,0), (px - 2, py - pipe_h - 8, pipe_w + 4, 8), 1)
    elif obs['type'] == 'goomba':
        draw_sprite(surface, GOOMBA, px - 8, py - 16, {'M': MARIO_GOOMBA, 'W': (255,255,255)})

def play(window, surface, clock, chapter_num):
    phase = PHASES[0] # Para simplificar, joga a primeira fase direto
    selected, attempts = None, 2
    timer_start = pygame.time.get_ticks()
    anim = {'phase': 'idle', 'pull': 0, 'start': 0, 'arrow_x': 0, 'arrow_y': 0, 'hit': False, 'impact_start': 0}
    result_msg, result_time = None, 0

    while True:
        dt = clock.tick(60) / 1000.0
        now = pygame.time.get_ticks()
        elapsed = (now - timer_start) / 1000.0
        remaining = max(0, TIMER_TOTAL - elapsed)
        thinking = elapsed < TIMER_THINKING

        if remaining <= 0 and anim['phase'] == 'idle' and result_msg is None:
            result_msg, result_time = 'timeout', now

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return 'menu'
            if event.type == pygame.MOUSEBUTTONDOWN and anim['phase'] == 'idle' and not thinking and result_msg is None:
                mx, my = event.pos[0] // 4, event.pos[1] // 4
                if CARDS_Y <= my <= CARDS_Y + CARD_H:
                    for i in range(3):
                        cx = 5 + i * (CARD_W + 5)
                        if cx <= mx <= cx + CARD_W: selected = i

        if anim['phase'] == 'pull':
            t = (now - anim['start']) / 300.0
            anim['pull'] = min(1, t)
            if t >= 1.1: anim['phase'], anim['start'] = 'fly', now
        elif anim['phase'] == 'fly':
            t = (now - anim['start']) / 1000.0
            f = phase['options'][selected]
            ax = phase['archer']['x'] + t * 12
            ay = f['a'] * ax**2 + f['b'] * ax + f['c']
            anim['arrow_x'], anim['arrow_y'] = ax, ay
            if math.hypot(ax - phase['target']['x'], ay - phase['target']['y']) < phase['target']['r']:
                anim['phase'], anim['hit'], anim['impact_start'] = 'impact', True, now
            elif ax > phase['target']['x'] + 2 or ay < 0:
                anim['phase'], anim['hit'], anim['impact_start'] = 'impact', False, now
        elif anim['phase'] == 'impact' and (now - anim['impact_start']) > 500:
            result_msg = 'hit' if anim['hit'] else 'miss'
            if not anim['hit']: attempts -= 1
            result_time = now
            anim['phase'] = 'done'

        draw_mario_bg(surface)
        for obs in phase['obstacles']: draw_obstacle(surface, obs)
        ax, ay = world_to_px(phase['archer']['x'], phase['archer']['y'])
        draw_sprite(surface, STEVE, ax - 9, ay - 8)
        draw_bow(surface, ax, ay, 0, anim['pull'] if anim['phase'] == 'pull' else 0)
        tx, ty = world_to_px(phase['target']['x'], phase['target']['y'])
        draw_sprite(surface, TARGET, tx - 8, ty - 8)

        if anim['phase'] in ('fly', 'impact'):
            fx, fy = world_to_px(anim['arrow_x'], anim['arrow_y'])
            pygame.draw.line(surface, (80, 60, 40), (fx - 5, fy), (fx + 5, fy), 2)

        # Cards
        for i, opt in enumerate(phase['options']):
            x, y = 5 + i * (CARD_W + 5), CARDS_Y
            border = (106, 76, 147) if i == selected else (180, 180, 180)
            pygame.draw.rect(surface, border, (x, y, CARD_W, CARD_H), 2)
            pygame.draw.rect(surface, (255, 255, 255), (x + 2, y + 2, CARD_W - 4, CARD_H - 4))
            eq = f"y={opt['c']}" if opt['b'] == 0 else f"y={opt['b']}x+{opt['c']}"
            draw_text(surface, chr(65+i), x + 5, y + 4, 14, (106, 76, 147))
            draw_text(surface, eq, x + 8, y + 24, 14, (40, 40, 50))

        color = (42, 157, 143) if remaining > 30 else (230, 57, 70)
        draw_text(surface, f"{int(remaining)}s", INTERNAL_W - 35, 5, 14, color)
        draw_text(surface, f"Tentativas: {attempts}/2", 5, 5, 12, (60, 60, 70))

        if result_msg:
            overlay = pygame.Surface((INTERNAL_W, INTERNAL_H)); overlay.set_alpha(180); overlay.fill((0,0,0))
            surface.blit(overlay, (0, 0))
            msg = "ACERTOU!" if result_msg == 'hit' else ("TEMPO ESGOTADO!" if result_msg == 'timeout' else "ERROU!")
            draw_text(surface, msg, 100, 80, 24, (255, 255, 255))
            draw_text(surface, phase['tip'], 20, 120, 12, (255, 255, 255))
            draw_text(surface, "Clique para continuar", 85, 200, 14, (200, 200, 200))
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: return 'quit'
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
                        if result_msg == 'hit': return 'menu'
                        elif attempts <= 0: return 'menu'
                        else:
                            timer_start, selected, result_msg = pygame.time.get_ticks(), None, None
                            anim = {'phase': 'idle', 'pull': 0, 'start': 0, 'arrow_x': 0, 'arrow_y': 0, 'hit': False, 'impact_start': 0}
                clock.tick(30)

        scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
        window.blit(scaled, (0, 0))
        pygame.display.flip()