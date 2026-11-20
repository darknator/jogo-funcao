import pygame
import math
import ast
import re
from config import *
from palette import *
from sprites import STEVE, TARGET, MARIO_GROUND
from renderer import draw_sprite, draw_text, draw_bow
import save as savemod

    
PHASES = [
    {
        'id': '1-1', 'chapter': 1, 'tipo': 'Constante',
        'archer': {'x': 0, 'y': 3}, 'target': {'x': 8, 'y': 3, 'r': 0.8},
        'obstacles': [],
        'goal': 'A flecha voa reta, sempre na mesma altura do alvo. Digite só o número.',
        'dominio': 'R', 'imagem': '{3}', 'solution': 'y=3',
        'tip': 'Função constante: y = c. A flecha voa reta, sempre na altura 3, não importa o valor de x.',
        'miss_hint': 'Na função constante não aparece x: o número que você digita é a altura da flecha.'
    },
    {
        'id': '1-2', 'chapter': 1, 'tipo': 'Linear',
        'archer': {'x': 0, 'y': 0}, 'target': {'x': 4, 'y': 8, 'r': 0.8},
        'obstacles': [{'type': 'pipe', 'x': 2, 'y': 0, 'h': 2.5}],
        'goal': 'A reta sai de (0,0) e passa pelo alvo. Quanto y sobe para cada 1 de x? Use y=a*x.',
        'dominio': 'R', 'imagem': 'R', 'solution': 'y=2*x',
        'tip': 'Função linear: y = a*x. Passa pela origem (0,0) e sobe a unidades a cada 1 em x. Aqui a = 2.',
        'miss_hint': 'Na linear a reta sai da origem. Divida a altura do alvo pela distância dele: a = y / x.'
    },
    {
        'id': '1-3', 'chapter': 1, 'tipo': 'Afim',
        'archer': {'x': 0, 'y': 2}, 'target': {'x': 8, 'y': 6, 'r': 0.8},
        'obstacles': [{'type': 'pipe', 'x': 3, 'y': 0, 'h': 2.5}],
        'goal': 'A reta sai de y=2 (esse é o b) e chega ao alvo. Falta achar a inclinação a em y=a*x+b.',
        'dominio': 'R', 'imagem': 'R', 'solution': 'y=0.5*x+2',
        'tip': 'Função afim: y = a*x + b. O b é a altura de saída (y quando x=0) e o a é a inclinação. Aqui a = 0,5 e b = 2.',
        'miss_hint': 'Em y = a*x + b: b = altura do arqueiro; a = (subida até o alvo) / (distância até o alvo).'
    },
    {
        'id': '1-4', 'chapter': 1, 'tipo': 'Quadrática',
        'archer': {'x': 0, 'y': 0}, 'target': {'x': 6, 'y': 0, 'r': 0.8},
        'obstacles': [{'type': 'pipe', 'x': 3, 'y': 0, 'h': 6}],
        'goal': 'Parábola: sai do chão, passa por cima do cano e volta ao chão no alvo (raízes 0 e 6).',
        'dominio': 'R', 'imagem': '(-inf, 9]', 'solution': 'y=6*x-x^2',
        'tip': 'Função quadrática: y = a*x^2 + b*x + c. Arqueiro e alvo estão no chão (y=0): são as raízes 0 e 6. Com a<0 a parábola abre para baixo e o vértice (3, 9) é o ponto mais alto.',
        'miss_hint': 'Raízes 0 e 6: y = -x*(x-6) = 6*x - x^2. O sinal negativo (a < 0) faz a flecha subir e depois descer.'
    },
    {
        'id': '1-5', 'chapter': 1, 'tipo': 'Exponencial',
        'archer': {'x': 0, 'y': 1}, 'target': {'x': 3, 'y': 8, 'r': 0.8},
        'obstacles': [{'type': 'pipe', 'x': 2, 'y': 0, 'h': 2.5}],
        'goal': 'A curva começa em y=1 e a cada passo em x o valor é multiplicado pela base a em y=a^x.',
        'dominio': 'R', 'imagem': '(0, +inf)', 'solution': 'y=2^x',
        'tip': 'Função exponencial: y = a^x. Em x=0 vale sempre 1 e a cada passo em x o valor é multiplicado por a. Com a = 2: 1, 2, 4, 8.',
        'miss_hint': 'Em y = a^x a flecha começa em y=1. Teste qual base a faz y chegar a 8 quando x=3 (a*a*a = 8).'
    }
]

START_TOL = 0.6
MAX_EXPR_LEN = 22

KEYS = [
    ['7', '8', '9', '^', 'C', '('],
    ['4', '5', '6', '*', '<', ')'],
    ['1', '2', '3', '-', 'x', 'abs('],
    ['0', '.', '+', '/', 'exp(']
]
TYPEABLE = set('0123456789.+-*/^()x')


ALLOWED_FUNCS = {'abs': abs, 'exp': math.exp, 'sqrt': math.sqrt, 'sin': math.sin,
                 'cos': math.cos, 'tan': math.tan, 'log': math.log}
ALLOWED_NAMES = {'x', 'e', 'pi'}
_BIN_OPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod)
_UNARY_OPS = (ast.UAdd, ast.USub)
_TOKEN_RE = re.compile(r'\d+\.?\d*|\.\d+|abs|exp|sqrt|sin|cos|tan|log|pi|e|x|\*\*|[-+*/%()]|\S')


def normalize_expr(text):

    s = text.strip().lower().replace(' ', '').replace(',', '.').replace('^', '**')
    tokens = _TOKEN_RE.findall(s)
    out = []
    for i, tok in enumerate(tokens):
        if i > 0:
            prev = tokens[i - 1]
            prev_value = prev == ')' or prev in ALLOWED_NAMES or prev[0].isdigit() or prev[0] == '.'
            next_start = tok == '(' or tok in ALLOWED_NAMES or tok in ALLOWED_FUNCS
            next_number = tok[0].isdigit() or tok[0] == '.'
            if prev_value and (next_start or (next_number and not (prev[0].isdigit() or prev[0] == '.'))):
                out.append('*')
        out.append(tok)
    return ''.join(out)


def _validate(node):
    if isinstance(node, ast.Expression):
        return _validate(node.body)
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (int, float)) and not isinstance(node.value, bool)
    if isinstance(node, ast.Name):
        return node.id in ALLOWED_NAMES
    if isinstance(node, ast.BinOp):
        return isinstance(node.op, _BIN_OPS) and _validate(node.left) and _validate(node.right)
    if isinstance(node, ast.UnaryOp):
        return isinstance(node.op, _UNARY_OPS) and _validate(node.operand)
    if isinstance(node, ast.Call):
        return (isinstance(node.func, ast.Name) and node.func.id in ALLOWED_FUNCS
                and len(node.args) == 1 and not node.keywords and _validate(node.args[0]))
    return False


class _ToFloat(ast.NodeTransformer):


    def visit_Constant(self, node):
        return ast.copy_location(ast.Constant(float(node.value)), node)


def compile_expr(text):

    expr = normalize_expr(text)
    if not expr:
        return None, "Digite uma função depois de y=. Exemplo: y=2*x+1"
    try:
        tree = ast.parse(expr, mode='eval')
    except (SyntaxError, ValueError, MemoryError, RecursionError):
        return None, "Erro de sintaxe! Verifique se digitou a função corretamente."
    if not _validate(tree):
        return None, "Símbolo não permitido. Use números, x, + - * / ^, parênteses, abs( e exp(."
    code = compile(ast.fix_missing_locations(_ToFloat().visit(tree)), '<funcao>', 'eval')
    env = {'e': math.e, 'pi': math.pi, **ALLOWED_FUNCS}

    def f(x):
        try:
            v = eval(code, {'__builtins__': {}}, {**env, 'x': float(x)})
        except (ArithmeticError, ValueError, TypeError):
            return None
        if not isinstance(v, float) or math.isnan(v) or math.isinf(v):
            return None
        return v

    return f, None


def safe_eval(eq_str, x_val):

    f, err = compile_expr(eq_str)
    return None if err else f(x_val)


def hits_obstacle(obs, x, y):

    if obs['type'] == 'pipe':  # corpo + borda do cano (a borda tem 8 px a mais no topo)
        return (obs['x'] - 2 / GAME_UNIT <= x <= obs['x'] + 18 / GAME_UNIT and
                obs['y'] <= y <= obs['y'] + obs['h'] + 8 / GAME_UNIT)
    return False


def evaluate_shot(phase, text, step=0.02):

    ax, ay = phase['archer']['x'], phase['archer']['y']
    tx, ty, r = phase['target']['x'], phase['target']['y'], phase['target']['r']

    def miss(kind, stop_x, reason, f=None):
        return {'hit': False, 'kind': kind, 'stop_x': stop_x, 'reason': reason, 'f': f}

    f, err = compile_expr(text)
    if err:
        return miss('syntax', ax, err)
    y0 = f(ax)
    if y0 is None:
        return miss('undefined', ax, f"A função não existe em x={ax:g}, onde o arqueiro está.", f)
    if abs(y0 - ay) > START_TOL:
        return miss('start', ax, f"A flecha precisa sair do arqueiro: em x={ax:g} sua função dá y={y0:.1f}, "
                                 f"mas o arqueiro está em y={ay:g}.", f)

    for i in range(int(round((tx + 2 - ax) / step)) + 1):
        x = ax + i * step
        y = f(x)
        if y is None:
            return miss('undefined', x, f"A função não existe em x={x:.1f} (divisão por zero ou raiz de negativo).", f)
        for obs in phase['obstacles']:
            if hits_obstacle(obs, x, y):
                return miss('obstacle', x, f"A flecha bateu no cano em x={x:.1f} (y={y:.1f}). "
                                           f"O cano chega até y={obs['y'] + obs['h']:g}: passe acima dele.", f)
        if math.hypot(x - tx, y - ty) < r:
            return {'hit': True, 'kind': 'hit', 'stop_x': x, 'reason': '', 'f': f}
        if y < -0.1:
            return miss('ground', x, f"A flecha caiu no chão em x={x:.1f}, antes de chegar ao alvo.", f)

    yt = f(tx)
    if yt is not None and yt < ty - r:
        return miss('low', tx + 2, f"Passou por BAIXO. No alvo (x={tx:g}), ela estava em y={yt:.1f}. Aumente a altura.",
                    f)
    if yt is not None and yt > ty + r:
        return miss('high', tx + 2, f"Passou por CIMA. No alvo (x={tx:g}), ela estava em y={yt:.1f}. Diminua a altura.",
                    f)
    return miss('high', tx + 2, "A flecha não acertou o alvo.", f)


def phases_for(chapter):
    return [p for p in PHASES if p['chapter'] == chapter]


def has_phases(chapter):
    return bool(phases_for(chapter))


def stars_for(errors):
    """3 estrelas sem erros, 2 com ate 2 erros, 1 nos demais casos."""
    return 3 if errors == 0 else 2 if errors <= 2 else 1


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


def draw_arrow(surface, f, x, y):

    fx, fy = world_to_px(x, y)
    ux, uy = 1.0, 0.0
    if f is not None:
        y1, y2 = f(x - 0.05), f(x + 0.05)
        if y1 is not None and y2 is not None:
            dx, dy = 0.1 * GAME_UNIT, -(y2 - y1) * GAME_UNIT
            n = math.hypot(dx, dy)
            ux, uy = dx / n, dy / n
    tail = (fx - ux * 6, fy - uy * 6)
    tip = (fx + ux * 5, fy + uy * 5)
    pygame.draw.line(surface, (80, 60, 40), tail, tip, 2)
    # ponta da flecha
    px_, py_ = -uy, ux
    pygame.draw.polygon(surface, (40, 40, 40), [(tip[0] + ux * 3, tip[1] + uy * 3),
                                                (tip[0] + px_ * 2, tip[1] + py_ * 2),
                                                (tip[0] - px_ * 2, tip[1] - py_ * 2)])


def new_anim():
    return {'phase': 'idle', 'pull': 0, 'start': 0, 'arrow_x': 0, 'arrow_y': 0, 'hit': False, 'impact_start': 0}


_font_cache = {}


def wrap_lines(text, size, max_w):

    if size not in _font_cache:
        _font_cache[size] = pygame.font.SysFont('Arial', size, bold=True)
    font = _font_cache[size]
    lines, current = [], ""
    for w in text.split(' '):
        if font.size(current + w)[0] < max_w:
            current += w + " "
        else:
            lines.append(current.strip())
            current = w + " "
    lines.append(current.strip())
    return lines


def play(window, surface, clock, chapter_num):

    phases = phases_for(chapter_num)
    if not phases:
        return 'menu'
    phase_idx = 0
    phase = phases[phase_idx]
    input_text = "y="
    show_preview = False
    anim = new_anim()
    result_msg = None
    error_reason = ""
    attempts = 2
    errors = 0
    shot = None

    while True:
        clock.tick(60)
        now = pygame.time.get_ticks()
        continue_key = False
        click_pos = None
        can_type = anim['phase'] == 'idle' and result_msg is None

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_pos = (event.pos[0] // SCALE, event.pos[1] // SCALE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return 'menu'
                if event.key == pygame.K_RETURN:
                    if result_msg is not None:
                        continue_key = True
                    elif can_type:
                        anim['phase'] = 'pull'
                        anim['start'] = now
                        show_preview = False
                elif event.key == pygame.K_BACKSPACE and can_type:
                    input_text = input_text[:-1] if len(input_text) > 2 else "y="
                elif can_type and event.unicode and len(input_text) < MAX_EXPR_LEN:
                    ch = event.unicode.lower()
                    if ch == ',':
                        ch = '.'
                    if ch in TYPEABLE:
                        input_text += ch

        draw_mario_bg(surface)
        for obs in phase['obstacles']: draw_obstacle(surface, obs)

        ax, ay = world_to_px(phase['archer']['x'], phase['archer']['y'])
        draw_sprite(surface, STEVE, ax - 9, ay - 8)
        draw_bow(surface, ax, ay, 0, anim['pull'] if anim['phase'] == 'pull' else 0)
        tx, ty = world_to_px(phase['target']['x'], phase['target']['y'])
        draw_sprite(surface, TARGET, tx - 8, ty - 8)

        if show_preview and anim['phase'] == 'idle' and result_msg is None:
            f_prev, _ = compile_expr(input_text[2:])
            if f_prev:
                for i in range(0, 72):
                    px_val = i * 0.25
                    py_val = f_prev(px_val)
                    if py_val is not None and -0.5 < py_val < 10.5:
                        sx, sy = world_to_px(px_val, py_val)
                        pygame.draw.circle(surface, (106, 76, 147), (sx, sy), 1)

        if anim['phase'] == 'pull':
            t = (now - anim['start']) / 300.0
            anim['pull'] = min(1, t)
            if t >= 1.1:

                shot = evaluate_shot(phase, input_text[2:])
                anim['arrow_x'], anim['arrow_y'] = phase['archer']['x'], phase['archer']['y']
                anim['phase'], anim['start'] = 'fly', now
        elif anim['phase'] == 'fly':
            t = (now - anim['start']) / 1000.0
            f = shot['f']
            arrow_x = phase['archer']['x'] + t * 12
            finished = f is None or arrow_x >= shot['stop_x']
            if finished:
                arrow_x = shot['stop_x']
            arrow_y = f(arrow_x) if f else None
            anim['arrow_x'] = arrow_x
            anim['arrow_y'] = arrow_y if arrow_y is not None else anim['arrow_y']
            if finished:
                anim['phase'], anim['hit'], anim['impact_start'] = 'impact', shot['hit'], now

        elif anim['phase'] == 'impact' and (now - anim['impact_start']) > 500:
            result_msg = 'hit' if anim['hit'] else 'miss'
            if not anim['hit']:
                attempts -= 1
                errors += 1
                error_reason = shot['reason']
            anim['phase'] = 'done'

        if anim['phase'] in ('fly', 'impact'):
            draw_arrow(surface, shot['f'] if shot else None, anim['arrow_x'], anim['arrow_y'])

        pygame.draw.rect(surface, (30, 30, 40), (0, 160, INTERNAL_W, 80))
        pygame.draw.line(surface, (100, 100, 110), (0, 160), (INTERNAL_W, 160), 2)

        pygame.draw.rect(surface, (255, 255, 255), (10, 165, 150, 22))
        pygame.draw.rect(surface, (100, 100, 100), (10, 165, 150, 22), 1)
        draw_text(surface, input_text, 15, 172 if len(input_text) <= 14 else 175, 14 if len(input_text) <= 14 else 10,
                  (0, 0, 0))

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
                if click_pos and can_type and kx <= click_pos[0] <= kx + kw and ky <= click_pos[1] <= ky + kh:
                    clicked_key = key

                pygame.draw.rect(surface, color, (kx, ky, kw, kh))
                pygame.draw.rect(surface, (150, 150, 150), (kx, ky, kw, kh), 1)
                draw_text(surface, key, kx + kw // 2, ky + kh // 2, 11 if len(key) == 1 else 8, text_color, center=True)

        btn_prev = (165, 170, 140, 25)
        btn_fire = (165, 205, 140, 25)

        pygame.draw.rect(surface, (69, 123, 157), btn_prev)
        pygame.draw.rect(surface, (100, 160, 200), btn_prev, 2)
        draw_text(surface, "PREVISAO", btn_prev[0] + 70, btn_prev[1] + 12, 14, (255, 255, 255), center=True)

        pygame.draw.rect(surface, (200, 50, 50), btn_fire)
        pygame.draw.rect(surface, (255, 100, 100), btn_fire, 2)
        draw_text(surface, "ATIRAR", btn_fire[0] + 70, btn_fire[1] + 12, 14, (255, 255, 255), center=True)

        def inside(btn):
            return click_pos and btn[0] <= click_pos[0] <= btn[0] + btn[2] and btn[1] <= click_pos[1] <= btn[1] + btn[3]

        if click_pos and result_msg is None:
            if inside(btn_prev):
                show_preview = not show_preview
            elif inside(btn_fire):
                if anim['phase'] == 'idle':
                    anim['phase'] = 'pull'
                    anim['start'] = now
                    show_preview = False
            elif clicked_key:
                if clicked_key == 'C':
                    input_text = "y="
                elif clicked_key == '<':
                    input_text = input_text[:-1] if len(input_text) > 2 else "y="
                elif len(input_text) + len(clicked_key) <= MAX_EXPR_LEN:
                    input_text += clicked_key


        pygame.draw.rect(surface, (0, 0, 0), (0, 0, INTERNAL_W, 20))
        draw_text(surface, f"Fase {phase['id']} - {phase['tipo']}", 5, 4, 14, (255, 255, 255))
        draw_text(surface, f"Tentativas: {attempts}/2", INTERNAL_W - 100, 4, 14, (255, 255, 255))


        pygame.draw.rect(surface, (20, 20, 30), (168, 24, 148, 66))
        pygame.draw.rect(surface, (255, 220, 100), (168, 24, 148, 66), 1)
        draw_text(surface, f"Arqueiro: (x={phase['archer']['x']:g}, y={phase['archer']['y']:g})", 172, 27, 9,
                  (255, 255, 255))
        draw_text(surface, f"Alvo:     (x={phase['target']['x']:g}, y={phase['target']['y']:g})", 172, 38, 9,
                  (255, 255, 255))
        for i, line in enumerate(wrap_lines(phase['goal'], 9, 138)[:3]):
            draw_text(surface, line, 172, 51 + i * 10, 9, (255, 220, 100))

        if result_msg:
            overlay = pygame.Surface((INTERNAL_W, INTERNAL_H));
            overlay.set_alpha(200);
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            msg = "ACERTOU!" if result_msg == 'hit' else "ERROU!"
            color = (42, 157, 143) if result_msg == 'hit' else (230, 57, 70)

            draw_text(surface, msg, INTERNAL_W // 2, 70, 30, color, center=True)

            if result_msg == 'hit':

                lines = wrap_lines(phase['tip'], 11, 290)[:4]
                for i, line in enumerate(lines):
                    draw_text(surface, line, INTERNAL_W // 2, 105 + i * 15, 11, (255, 255, 255), center=True)
                draw_text(surface, f"Tipo: {phase['tipo']}   |   D = {phase['dominio']}   |   Im = {phase['imagem']}",
                          INTERNAL_W // 2, 175, 11, (255, 220, 100), center=True)
            else:
                reason_lines = wrap_lines(error_reason, 11, 290)[:3]
                hint_lines = wrap_lines(phase['miss_hint'], 10, 290)[:3]
                for i, line in enumerate(reason_lines):
                    draw_text(surface, line, INTERNAL_W // 2, 105 + i * 14, 11, (255, 255, 255), center=True)
                for i, line in enumerate(hint_lines):
                    draw_text(surface, line, INTERNAL_W // 2, 105 + (len(reason_lines) + i) * 14 + 6, 10,
                              (255, 220, 100), center=True)

            draw_text(surface, "Clique ou ENTER para continuar", INTERNAL_W // 2, 205, 12, (200, 200, 200), center=True)

            if click_pos or continue_key:
                if result_msg == 'hit':
                    if phase_idx + 1 >= len(phases):

                        data = savemod.load()
                        savemod.complete_chapter(data, chapter_num, stars_for(errors))
                        return 'menu'
                    phase_idx += 1
                    phase = phases[phase_idx]
                    input_text = "y="
                    attempts, result_msg, show_preview = 2, None, False
                    anim = new_anim()
                elif attempts <= 0:
                    return 'menu'
                else:

                    result_msg, show_preview = None, False
                    anim = new_anim()

        scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
        window.blit(scaled, (0, 0))
        pygame.display.flip()