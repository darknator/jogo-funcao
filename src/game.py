import pygame
import math
import ast
import re
import os
import random
from config import *
from palette import *
from sprites import STEVE, TARGET, MARIO_GROUND
from renderer import draw_sprite, draw_text, draw_bow
from menu import draw_mc_button
import save as savemod


PHASES = [
    # ================= CAPÍTULO 1: FUNÇÕES =================
    {
        'id': '1-1', 'chapter': 1, 'tipo': 'Constante',
        'archer': {'x': 0, 'y': 3}, 'target': {'x': 8, 'y': 3, 'r': 0.8},
        'obstacles': [],
        'goal': 'A flecha voa reta, sempre na mesma altura do alvo. Digite so o numero.',
        'dominio': 'R', 'imagem': '{3}', 'solution': 'y=3',
        'tip': 'Funcao constante: y = c. A flecha voa reta, sempre na altura 3, nao importa o valor de x.',
        'miss_hint': 'Na funcao constante nao aparece x: o numero que voce digita e a altura da flecha.'
    },
    {
        'id': '1-2', 'chapter': 1, 'tipo': 'Linear',
        'archer': {'x': 0, 'y': 0}, 'target': {'x': 4, 'y': 8, 'r': 0.8},
        'obstacles': [{'type': 'pipe', 'x': 2, 'y': 0, 'h': 2.5}],
        'goal': 'A reta sai de (0,0) e passa pelo alvo. Quanto y sobe para cada 1 de x? Use y=a*x.',
        'dominio': 'R', 'imagem': 'R', 'solution': 'y=2*x',
        'tip': 'Funcao linear: y = a*x. Passa pela origem (0,0) e sobe a unidades a cada 1 em x. Aqui a = 2.',
        'miss_hint': 'Na linear a reta sai da origem. Divida a altura do alvo pela distancia dele: a = y / x.'
    },
    {
        'id': '1-3', 'chapter': 1, 'tipo': 'Afim',
        'archer': {'x': 0, 'y': 2}, 'target': {'x': 8, 'y': 6, 'r': 0.8},
        'obstacles': [{'type': 'pipe', 'x': 3, 'y': 0, 'h': 2.5}],
        'goal': 'A reta sai de y=2 (esse e o b) e chega ao alvo. Falta achar a inclinacao a em y=a*x+b.',
        'dominio': 'R', 'imagem': 'R', 'solution': 'y=0.5*x+2',
        'tip': 'Funcao afim: y = a*x + b. O b e a altura de saida (y quando x=0) e o a e a inclinacao. Aqui a = 0,5 e b = 2.',
        'miss_hint': 'Em y = a*x + b: b = altura do arqueiro; a = (subida ate o alvo) / (distancia ate o alvo).'
    },
    {
        'id': '1-4', 'chapter': 1, 'tipo': 'Quadrática',
        'archer': {'x': 0, 'y': 0}, 'target': {'x': 6, 'y': 0, 'r': 0.8},
        'obstacles': [{'type': 'pipe', 'x': 3, 'y': 0, 'h': 6}],
        'goal': 'Parabola: sai do chao, passa por cima do cano e volta ao chao no alvo (raizes 0 e 6).',
        'dominio': 'R', 'imagem': '(-inf, 9]', 'solution': 'y=6*x-x^2',
        'tip': 'Funcao quadratica: y = a*x^2 + b*x + c. Arqueiro e alvo estao no chao (y=0): sao as raizes 0 e 6. Com a<0 a parabola abre para baixo e o vertice (3, 9) e o ponto mais alto.',
        'miss_hint': 'Raizes 0 e 6: y = -x*(x-6) = 6*x - x^2. O sinal negativo (a < 0) faz a flecha subir e depois descer.'
    },
    {
        'id': '1-5', 'chapter': 1, 'tipo': 'Exponencial',
        'archer': {'x': 0, 'y': 1}, 'target': {'x': 3, 'y': 8, 'r': 0.8},
        'obstacles': [{'type': 'pipe', 'x': 2, 'y': 0, 'h': 2.5}],
        'goal': 'A curva comeca em y=1 e a cada passo em x o valor e multiplicado pela base a em y=a^x.',
        'dominio': 'R', 'imagem': '(0, +inf)', 'solution': 'y=2^x',
        'tip': 'Funcao exponencial: y = a^x. Em x=0 vale sempre 1 e a cada passo em x o valor e multiplicado por a. Com a = 2: 1, 2, 4, 8.',
        'miss_hint': 'Em y = a^x a flecha comeca em y=1. Teste qual base a faz y chegar a 8 quando x=3 (a*a*a = 8).'
    },

    # ================= CAPÍTULO 2: DERIVADAS =================
    {
        'id': '2-1', 'chapter': 2, 'tipo': 'Derivada de reta',
        'archer': {'x': 0, 'y': 2}, 'target': {'x': 6, 'y': 2, 'r': 0.9},
        'obstacles': [],
        'goal': 'Se f(x) = 2*x, qual e a derivada f\'(x)? Digite y = f\'(x). A flecha segue a derivada.',
        'dominio': 'R', 'imagem': 'R', 'solution': 'y=2',
        'tip': 'A derivada de f(x) = 2*x e f\'(x) = 2. A derivada de uma reta e uma constante: a inclinacao da reta.',
        'miss_hint': 'Derivada de a*x e a. Se f(x) = 2*x, entao f\'(x) = 2. Digite y=2.'
    },
    {
        'id': '2-2', 'chapter': 2, 'tipo': 'Derivada de quadrática',
        'archer': {'x': 0, 'y': 0}, 'target': {'x': 5, 'y': 10, 'r': 0.9},
        'obstacles': [{'type': 'pipe', 'x': 2, 'y': 0, 'h': 2.5}],
        'goal': 'Se f(x) = x^2, qual e f\'(x)? A flecha deve subir passando por cima do cano.',
        'dominio': 'R', 'imagem': 'R', 'solution': 'y=2*x',
        'tip': 'Regra do tombo: derivada de x^n e n*x^(n-1). Para x^2, f\'(x) = 2*x. Em x=5, y=10.',
        'miss_hint': 'Derivada de x^2 e 2*x. A reta y=2*x sai da origem e sobe 2 a cada 1 em x.'
    },
    {
        'id': '2-3', 'chapter': 2, 'tipo': 'Derivada de cúbica',
        'archer': {'x': 0, 'y': 0}, 'target': {'x': 1.5, 'y': 6.75, 'r': 0.9},
        'obstacles': [{'type': 'pipe', 'x': 1.2, 'y': 0, 'h': 1.0}],
        'goal': 'Se f(x) = x^3, qual e f\'(x)? A parabola da derivada precisa passar pelo alvo.',
        'dominio': 'R', 'imagem': '[0, +inf)', 'solution': 'y=3*x^2',
        'tip': 'Derivada de x^3 e 3*x^2. E uma parabola que abre para cima. Em x=1.5, y=6.75.',
        'miss_hint': 'A derivada de x^3 e 3*x^2. Em x=1.5, 3*(1.5)^2 = 6.75. Digite y=3*x^2.'
    },
    {
        'id': '2-4', 'chapter': 2, 'tipo': 'Derivada de afim',
        'archer': {'x': 0, 'y': 3}, 'target': {'x': 4, 'y': 3, 'r': 0.9},
        'obstacles': [],
        'goal': 'Se f(x) = 3*x + 1, qual e f\'(x)? A derivada de uma afim e constante.',
        'dominio': 'R', 'imagem': 'R', 'solution': 'y=3',
        'tip': 'A derivada de a*x + b e a. O b desaparece. Se f(x) = 3*x + 1, entao f\'(x) = 3.',
        'miss_hint': 'Derivada de 3*x + 1 e 3. O termo constante (1) some na derivada. Digite y=3.'
    },
    {
        'id': '2-5', 'chapter': 2, 'tipo': 'Derivada de exponencial',
        'archer': {'x': 0, 'y': 1}, 'target': {'x': 2, 'y': 7.4, 'r': 1.0},
        'obstacles': [],
        'goal': 'Se f(x) = e^x, qual e f\'(x)? A derivada da exponencial natural e ela mesma.',
        'dominio': 'R', 'imagem': '(0, +inf)', 'solution': 'y=exp(x)',
        'tip': 'A derivada de e^x e e^x. A funcao e sua propria derivada. No jogo, use exp(x) para e^x. Em x=2, y~7.39.',
        'miss_hint': 'A derivada de e^x e e^x. Digite y=exp(x). Em x=2, exp(2) ~ 7.39.'
    },
]

START_TOL = 0.6

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

BBG_MUNDO2 = None
BG_PRATICA = None
BG_MUNDO3 = {}

# Variáveis globais para a câmera dinâmica
CAMERA_UNIT = GAME_UNIT
CAMERA_Y = GAME_Y
CAMERA_X = GAME_X

def load_bg_image(base_name):
    extensions = ['.png', '.jpg', '.jpeg', '.webp', '.PNG', '.JPG']
    for ext in extensions:
        path = os.path.join(os.path.dirname(__file__), base_name + ext)
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert()
                img_w, img_h = img.get_size()
                scale = max(INTERNAL_W / img_w, INTERNAL_H / img_h)
                new_w, new_h = int(img_w * scale), int(img_h * scale)
                img = pygame.transform.smoothscale(img, (new_w, new_h))
                final_img = pygame.Surface((INTERNAL_W, INTERNAL_H))
                final_img.blit(img, ((INTERNAL_W - new_w) // 2, (INTERNAL_H - new_h) // 2))
                return final_img
            except Exception:
                pass
    return None

def setup_camera(phase):
    """Calcula o zoom e os deslocamentos para que o alvo E o personagem caibam na tela."""
    global CAMERA_UNIT, CAMERA_Y, CAMERA_X
    
    # Pega a altura máxima que precisamos mostrar (alvo ou arqueiro)
    max_y = max(phase['archer']['y'], phase['target']['y'] + phase['target']['r'])
    max_x = max(phase['archer']['x'], phase['target']['x'] + phase['target']['r'])
    
    # Área útil da tela (deixa margem para o teclado virtual embaixo e painel em cima)
    # O chão vai ficar em CAMERA_Y. Queremos que o topo da tela seja y=240 (para caber no painel)
    # e o chão fique em y=280 (para não sumir atrás do teclado).
    
    area_h = 240 # Distância em pixels do topo do gráfico até o chão
    area_w = 580 # Largura máxima em pixels
    
    # Calcula o GAME_UNIT ideal para caber a altura e a largura
    unit_y = area_h / max(max_y, 1) if max_y > 0 else GAME_UNIT
    unit_x = area_w / max(max_x, 1) if max_x > 0 else GAME_UNIT
    
    # Escolhe o menor para garantir que tudo caiba
    CAMERA_UNIT = min(unit_y, unit_x, GAME_UNIT)
    
    # Posiciona o chão na parte de baixo, mas deixando espaço para o teclado virtual
    CAMERA_Y = 280 
    CAMERA_X = GAME_X

def world_to_px(x, y):
    return (CAMERA_X + int(x * CAMERA_UNIT), CAMERA_Y - int(y * CAMERA_UNIT))

def generate_random_phase(mode):
    if mode == 'funcoes':
        templates = [
            {'tipo': 'Constante', 'goal': 'A flecha voa reta. Digite a altura como y=c.', 'solution': f'y={random.randint(2, 10)}'},
            {'tipo': 'Linear', 'goal': 'A reta sai da origem. Digite y=a*x.', 'solution': f'y={random.randint(1, 2)}*x'},
            {'tipo': 'Afim', 'goal': 'A reta sai de y=b. Digite y=a*x+b.', 'solution': f'y={random.choice([0.5, 1])}*x+{random.randint(1, 5)}'},
            {'tipo': 'Quadrática', 'goal': 'Uma parabola. Digite y=a*x^2+b*x+c.', 'solution': f'y={random.randint(1,2)}*x^2-{random.randint(2,4)}*x+{random.randint(2,5)}'},
            {'tipo': 'Exponencial', 'goal': 'Uma curva exponencial. Digite y=a^x.', 'solution': f'y={random.choice([2, 3])}^x'}
        ]
    else:
        templates = [
            {'tipo': 'Derivada de reta', 'goal': 'Derive f(x) = a*x.', 'solution': f'y={random.randint(2, 5)}', 'f_orig': f'{random.randint(2,5)}*x'},
            {'tipo': 'Derivada de quadrática', 'goal': 'Derive f(x) = x^2.', 'solution': 'y=2*x', 'f_orig': 'x^2'},
            {'tipo': 'Derivada de cúbica', 'goal': 'Derive f(x) = x^3.', 'solution': 'y=3*x^2', 'f_orig': 'x^3'},
            {'tipo': 'Derivada de afim', 'goal': 'Derive f(x) = a*x + b.', 'solution': f'y={random.randint(2, 5)}', 'f_orig': f'{random.randint(2,5)}*x+{random.randint(1,3)}'},
        ]
    
    tmpl = random.choice(templates)
    f_compiled, _ = compile_expr(tmpl['solution'].replace('y=', ''))
    
    x_target = random.randint(3, 7)
    y_target = f_compiled(x_target) if f_compiled else 5
    
    if y_target is None or y_target < 1 or y_target > 20:
        x_target = 4
        y_target = f_compiled(x_target) if f_compiled else 4
        
    phase = {
        'id': 'PRATICA', 'chapter': 0, 'tipo': tmpl['tipo'],
        'archer': {'x': 0, 'y': f_compiled(0) if f_compiled and f_compiled(0) is not None else 0},
        'target': {'x': x_target, 'y': y_target, 'r': 0.9},
        'obstacles': [],
        'goal': f"Calcule a resposta! {tmpl['goal']}",
        'dominio': 'R', 'imagem': 'R', 'solution': tmpl['solution'],
        'tip': f"Voce acertou! A resposta correta era {tmpl['solution']}.",
        'miss_hint': f"Dica: Reveja as regras de {tmpl['tipo']}."
    }
    
    if 'f_orig' in tmpl:
        phase['goal'] = f"Se f(x) = {tmpl['f_orig']}, qual e a derivada f'(x)?"
        
    return phase

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
    if isinstance(node, ast.Expression): return _validate(node.body)
    if isinstance(node, ast.Constant): return isinstance(node.value, (int, float)) and not isinstance(node.value, bool)
    if isinstance(node, ast.Name): return node.id in ALLOWED_NAMES
    if isinstance(node, ast.BinOp): return isinstance(node.op, _BIN_OPS) and _validate(node.left) and _validate(node.right)
    if isinstance(node, ast.UnaryOp): return isinstance(node.op, _UNARY_OPS) and _validate(node.operand)
    if isinstance(node, ast.Call): return (isinstance(node.func, ast.Name) and node.func.id in ALLOWED_FUNCS and len(node.args) == 1 and not node.keywords and _validate(node.args[0]))
    return False

class _ToFloat(ast.NodeTransformer):
    def visit_Constant(self, node):
        return ast.copy_location(ast.Constant(float(node.value)), node)

def compile_expr(text):
    expr = normalize_expr(text)
    if not expr: return None, "Digite uma funcao depois de y=."
    try:
        tree = ast.parse(expr, mode='eval')
    except: return None, "Erro de sintaxe!"
    if not _validate(tree): return None, "Simbolo nao permitido."
    code = compile(ast.fix_missing_locations(_ToFloat().visit(tree)), '<funcao>', 'eval')
    env = {'e': math.e, 'pi': math.pi, **ALLOWED_FUNCS}

    def f(x):
        try:
            v = eval(code, {'__builtins__': {}}, {**env, 'x': float(x)})
        except: return None
        if not isinstance(v, float) or math.isnan(v) or math.isinf(v): return None
        return v

    return f, None

def hits_obstacle(obs, x, y):
    if obs['type'] == 'pipe':
        return (obs['x'] - 2 / CAMERA_UNIT <= x <= obs['x'] + 18 / CAMERA_UNIT and
                obs['y'] <= y <= obs['y'] + obs['h'] + 8 / CAMERA_UNIT)
    return False

def evaluate_shot(phase, text, step=0.02):
    ax, ay = phase['archer']['x'], phase['archer']['y']
    tx, ty, r = phase['target']['x'], phase['target']['y'], phase['target']['r']

    def miss(kind, stop_x, reason, f=None):
        return {'hit': False, 'kind': kind, 'stop_x': stop_x, 'reason': reason, 'f': f}

    f, err = compile_expr(text)
    if err: return miss('syntax', ax, err)
    y0 = f(ax)
    if y0 is None: return miss('undefined', ax, f"A funcao nao existe em x={ax:g}.", f)
    if abs(y0 - ay) > START_TOL:
        return miss('start', ax, f"A flecha precisa sair de y={ay:g}. Sua funcao em x=0 da y={y0:.1f}.", f)

    for i in range(int(round((tx + 2 - ax) / step)) + 1):
        x = ax + i * step
        y = f(x)
        if y is None: return miss('undefined', x, f"A funcao nao existe em x={x:.1f}.", f)
        for obs in phase['obstacles']:
            if hits_obstacle(obs, x, y):
                return miss('obstacle', x, f"A flecha bateu no cano!", f)
        if math.hypot(x - tx, y - ty) < r:
            return {'hit': True, 'kind': 'hit', 'stop_x': tx, 'reason': '', 'f': f}
        if y < -0.1: return miss('ground', x, f"A flecha caiu no chao.", f)

    yt = f(tx)
    if yt is not None and yt < ty - r: return miss('low', tx + 2, f"Passou por BAIXO. Aumente a altura.", f)
    if yt is not None and yt > ty + r: return miss('high', tx + 2, f"Passou por CIMA. Diminua a altura.", f)
    return miss('high', tx + 2, "A flecha nao acertou o alvo.", f)

def phases_for(chapter): return [p for p in PHASES if p['chapter'] == chapter]
def has_phases(chapter): return bool(phases_for(chapter))
def stars_for(errors): return 3 if errors == 0 else 2 if errors <= 2 else 1

def draw_grid_overlay(surface):
    overlay = pygame.Surface((INTERNAL_W, INTERNAL_H), pygame.SRCALPHA)
    
    # Calcula até onde a grade precisa ir na tela (para cima e para a direita)
    # Baseado no zoom atual (CAMERA_UNIT) e no tamanho da tela
    max_x = int((INTERNAL_W - CAMERA_X) / CAMERA_UNIT) + 2
    max_y = int(CAMERA_Y / CAMERA_UNIT) + 2
    
    # Desenha as linhas verticais (eixo X)
    for gx in range(0, max_x):
        px, _ = world_to_px(gx, 0)
        # Só desenha se estiver dentro da tela
        if px <= INTERNAL_W:
            pygame.draw.line(overlay, (255, 255, 255, 60), (px, 0), (px, CAMERA_Y), 1)
            
    # Desenha as linhas horizontais (eixo Y)
    for gy in range(0, max_y):
        _, py = world_to_px(0, gy)
        # Só desenha se estiver dentro da tela (acima do chão)
        if py >= 0 and py <= CAMERA_Y:
            pygame.draw.line(overlay, (255, 255, 255, 60), (CAMERA_X, py), (INTERNAL_W, py), 1)
            
    # Desenha os eixos principais (X e Y) um pouco mais fortes
    _, y0 = world_to_px(0, 0)
    pygame.draw.line(overlay, (255, 255, 255, 180), (CAMERA_X, y0), (INTERNAL_W, y0), 2)
    pygame.draw.line(overlay, (255, 255, 255, 180), (CAMERA_X, 0), (CAMERA_X, y0), 2)
    
    surface.blit(overlay, (0, 0))

def draw_mario_bg(surface, chapter_num):
    global BG_MUNDO2, BG_PRATICA, BG_MUNDO3

    if chapter_num == 3:
        fase = getattr(draw_mario_bg, "fase_atual", 0)

        if fase < 2:
            numero_cenario = 1
        elif fase < 4:
            numero_cenario = 2
        else:
            numero_cenario = 3

        if numero_cenario not in BG_MUNDO3:
            BG_MUNDO3[numero_cenario] = load_bg_image(
                f"bg_mundo3_{numero_cenario}"
            )

        imagem = BG_MUNDO3[numero_cenario]

        if imagem is not None:
            surface.blit(imagem, (0, 0))
            draw_grid_overlay(surface)

            ground_pal = {
                'L': MARIO_GROUND_LIGHT,
                'D': MARIO_GROUND_MAIN
            }

            for x in range(0, INTERNAL_W, 32):
                for y in range(CAMERA_Y, INTERNAL_H, 32):
                    draw_sprite(
                        surface, MARIO_GROUND,
                        x, y, ground_pal, scale=2
                    )

            pygame.draw.line(
                surface, (0, 0, 0),
                (0, CAMERA_Y), (INTERNAL_W, CAMERA_Y), 3
            )
            return
    if chapter_num == 0:
        if BG_PRATICA is None: 
            BG_PRATICA = load_bg_image('bg_pratica')
        if BG_PRATICA is not None:
            surface.blit(BG_PRATICA, (0, 0))
            draw_grid_overlay(surface)
            ground_pal = {'L': MARIO_GROUND_LIGHT, 'D': MARIO_GROUND_MAIN}
            for x in range(0, INTERNAL_W, 32):
                for y in range(CAMERA_Y, INTERNAL_H, 32):
                    draw_sprite(surface, MARIO_GROUND, x, y, ground_pal, scale=2)
            pygame.draw.line(surface, (0, 0, 0), (0, CAMERA_Y), (INTERNAL_W, CAMERA_Y), 3)
            return

    if chapter_num == 2:
        if BG_MUNDO2 is None: 
            BG_MUNDO2 = load_bg_image('bg_mundo2')
        if BG_MUNDO2 is not None:
            surface.blit(BG_MUNDO2, (0, 0))
            draw_grid_overlay(surface)
            ground_pal = {'L': MARIO_GROUND_LIGHT, 'D': MARIO_GROUND_MAIN}
            for x in range(0, INTERNAL_W, 32):
                for y in range(CAMERA_Y, INTERNAL_H, 32):
                    draw_sprite(surface, MARIO_GROUND, x, y, ground_pal, scale=2)
            pygame.draw.line(surface, (0, 0, 0), (0, CAMERA_Y), (INTERNAL_W, CAMERA_Y), 3)
            return

    surface.fill(MARIO_SKY)
    for cx, cy in [(60, 80), (300, 120), (520, 60)]:
        pygame.draw.rect(surface, (255, 255, 255), (cx, cy, 60, 20))
        pygame.draw.rect(surface, (255, 255, 255), (cx + 10, cy - 10, 40, 20))
        pygame.draw.rect(surface, (255, 255, 255), (cx + 20, cy - 20, 20, 20))
    for bx, by in [(20, CAMERA_Y - 30), (240, CAMERA_Y - 40), (500, CAMERA_Y - 24)]:
        pygame.draw.rect(surface, MARIO_PIPE_GREEN, (bx, by, 80, 40))
        pygame.draw.circle(surface, MARIO_PIPE_GREEN, (bx + 20, by), 20)
        pygame.draw.circle(surface, MARIO_PIPE_GREEN, (bx + 60, by), 20)
        pygame.draw.circle(surface, MARIO_PIPE_GREEN, (bx + 40, by - 20), 30)
    for gx in range(0, 22):
        px, _ = world_to_px(gx, 0)
        pygame.draw.line(surface, (150, 180, 240), (px, 0), (px, CAMERA_Y), 1)
    for gy in range(0, 16):
        _, py = world_to_px(0, gy)
        pygame.draw.line(surface, (150, 180, 240), (CAMERA_X, py), (INTERNAL_W, py), 1)
    _, y0 = world_to_px(0, 0)
    pygame.draw.line(surface, (80, 80, 80), (CAMERA_X, y0), (INTERNAL_W, y0), 3)
    pygame.draw.line(surface, (80, 80, 80), (CAMERA_X, 0), (CAMERA_X, y0), 3)
    ground_pal = {'L': MARIO_GROUND_LIGHT, 'D': MARIO_GROUND_MAIN}
    for x in range(0, INTERNAL_W, 32):
        for y in range(CAMERA_Y, INTERNAL_H, 32):
            draw_sprite(surface, MARIO_GROUND, x, y, ground_pal, scale=2)
    pygame.draw.line(surface, (0, 0, 0), (0, CAMERA_Y), (INTERNAL_W, CAMERA_Y), 3)

def draw_obstacle(surface, obs):
    px, py = world_to_px(obs['x'], obs['y'])
    if obs['type'] == 'pipe':
        pipe_w = int(16 * CAMERA_UNIT / 15)
        pipe_h = int(obs['h'] * CAMERA_UNIT)
        pygame.draw.rect(surface, MARIO_PIPE_GREEN, (px, py - pipe_h, pipe_w, pipe_h))
        pygame.draw.rect(surface, MARIO_PIPE_DARK, (px + pipe_w - 8, py - pipe_h, 8, pipe_h))
        pygame.draw.rect(surface, MARIO_PIPE_GREEN, (px - 4, py - pipe_h - 16, pipe_w + 8, 16))
        pygame.draw.rect(surface, MARIO_PIPE_DARK, (px + pipe_w - 4, py - pipe_h - 16, 8, 16))
        pygame.draw.rect(surface, (0, 0, 0), (px - 4, py - pipe_h - 16, pipe_w + 8, 16), 1)

def draw_arrow(surface, f, x, y):
    fx, fy = world_to_px(x, y)
    ux, uy = 1.0, 0.0
    if f is not None:
        y1, y2 = f(x - 0.05), f(x + 0.05)
        if y1 is not None and y2 is not None:
            dx, dy = 0.1 * CAMERA_UNIT, -(y2 - y1) * CAMERA_UNIT
            n = math.hypot(dx, dy)
            if n > 0.001: ux, uy = dx / n, dy / n
    tail = (fx - ux * 12, fy - uy * 12)
    tip = (fx + ux * 10, fy + uy * 10)
    pygame.draw.line(surface, (80, 60, 40), tail, tip, 3)
    px_, py_ = -uy, ux
    pygame.draw.polygon(surface, (40, 40, 40), [(tip[0] + ux * 6, tip[1] + uy * 6),
                                                (tip[0] + px_ * 4, tip[1] + py_ * 4),
                                                (tip[0] - px_ * 4, tip[1] - py_ * 4)])

def draw_trail(surface, f, x_start, x_end, color):
    if f is None or x_end <= x_start: return
    prev = None
    x = x_start
    while x <= x_end:
        y = f(x)
        if y is not None and -5 < y < 20:
            p = world_to_px(x, y)
            if prev is not None: pygame.draw.line(surface, color, prev, p, 2)
            prev = p
        else: prev = None
        x += TRAIL_STEP

def new_anim():
    return {'phase': 'idle', 'pull': 0, 'start': 0, 'arrow_x': 0, 'arrow_y': 0, 'hit': False, 'impact_start': 0}

_font_cache = {}

def wrap_lines(text, size, max_w):
    if size not in _font_cache: _font_cache[size] = pygame.font.SysFont('Arial', size, bold=True)
    font = _font_cache[size]
    lines, current = [], ""
    for w in text.split(' '):
        if font.size(current + w)[0] < max_w: current += w + " "
        else:
            lines.append(current.strip())
            current = w + " "
    lines.append(current.strip())
    return lines

def draw_cartesian_graph(surface, phase, f, x_end, hit, input_text):
    surface.fill((15, 15, 25))
    gx0, gy0 = 80, 60
    gw, gh = 480, 320

    x_min_val = phase['archer']['x']
    x_max = max(phase['target']['x'] + 2, x_end + 1, x_min_val + 4)
    y_min, y_max = 0, 15
    y_range = y_max - y_min

    def g2p(gx, gy):
        px = gx0 + int((gx / x_max) * gw)
        py = gy0 + gh - int(((gy - y_min) / y_range) * gh)
        return px, py

    for i in range(0, int(x_max) + 1):
        px, _ = g2p(i, y_min)
        pygame.draw.line(surface, (40, 45, 60), (px, gy0), (px, gy0 + gh), 1)
        draw_text(surface, str(i), px, gy0 + gh + 18, 16, (180, 180, 200), center=True)
    for j in range(y_min, y_max + 1):
        _, py = g2p(0, j)
        pygame.draw.line(surface, (40, 45, 60), (gx0, py), (gx0 + gw, py), 1)
        draw_text(surface, str(j), gx0 - 18, py, 16, (180, 180, 200), center=True)

    ox, oy = g2p(0, 0)
    pygame.draw.line(surface, (220, 220, 240), (gx0, oy), (gx0 + gw, oy), 3)
    pygame.draw.line(surface, (220, 220, 240), (ox, gy0), (ox, gy0 + gh), 3)
    pygame.draw.polygon(surface, (220, 220, 240), [(gx0 + gw, oy), (gx0 + gw - 12, oy - 6), (gx0 + gw - 12, oy + 6)])
    pygame.draw.polygon(surface, (220, 220, 240), [(ox, gy0), (ox - 6, gy0 + 12), (ox + 6, gy0 + 12)])
    draw_text(surface, "x", gx0 + gw + 14, oy - 8, 20, (220, 220, 240), center=True)
    draw_text(surface, "y", ox + 10, gy0 - 8, 20, (220, 220, 240), center=True)

    if f is not None:
        prev = None
        x = x_min_val
        while x <= x_end:
            yv = f(x)
            if yv is not None and y_min - 2 <= yv <= y_max + 2:
                p = g2p(x, yv)
                if prev is not None: pygame.draw.line(surface, TRAIL_COLOR_HIT if hit else TRAIL_COLOR_MISS, prev, p, 3)
                prev = p
            else: prev = None
            x += 0.05

    ax, ay = g2p(phase['archer']['x'], phase['archer']['y'])
    pygame.draw.circle(surface, (80, 160, 255), (ax, ay), 8)
    draw_text(surface, "A", ax, ay - 16, 16, (80, 160, 255), center=True)

    tx, ty = g2p(phase['target']['x'], phase['target']['y'])
    r_px = max(6, min(int((phase['target']['r'] / x_max) * gw) if x_max > 0 else 10, 20))
    pygame.draw.circle(surface, (230, 57, 70), (tx, ty), r_px, 3)
    pygame.draw.circle(surface, (230, 57, 70), (tx, ty), 2)

    if f is not None:
        y_end_val = f(x_end)
        if y_end_val is not None:
            fx, fy = g2p(x_end, y_end_val)
            pygame.draw.circle(surface, (255, 255, 255), (fx, fy), 4)

    draw_text(surface, "GRAFICO DO TIRO", gx0 + gw // 2, 22, 32, (255, 220, 100), center=True)
    status = "ACERTOU!" if hit else "ERROU!"
    status_color = (42, 220, 143) if hit else (230, 80, 70)
    draw_text(surface, status, gx0 + gw // 2, gy0 + gh + 60, 36, status_color, center=True)

    draw_text(surface, f"Sua funcao: {input_text}", gx0, gy0 + gh + 100, 20, (220, 220, 240))
    draw_text(surface, f"Tipo: {phase['tipo']}   |   Alvo: ({phase['target']['x']:g}, {phase['target']['y']:g})",
              gx0, gy0 + gh + 130, 20, (220, 220, 240))
    draw_text(surface, "Clique ou ENTER para continuar", gx0 + gw // 2, 460, 22, (200, 200, 200), center=True)

def draw_pause_menu(surface, mouse_pos, scale, is_practice=False):
    overlay = pygame.Surface((INTERNAL_W, INTERNAL_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    
    draw_text(surface, "JOGO PAUSADO", INTERNAL_W // 2, 120, 48, (255, 255, 255), center=True)
    
    mx, my = mouse_pos[0] // scale, mouse_pos[1] // scale
    
    if is_practice:
        btn_continuar = (INTERNAL_W // 2 - 150, 220, 300, 50)
        btn_novo = (INTERNAL_W // 2 - 150, 290, 300, 50)
        btn_sair = (INTERNAL_W // 2 - 150, 360, 300, 50)
        
        hover_cont = btn_continuar[0] <= mx <= btn_continuar[0] + btn_continuar[2] and btn_continuar[1] <= my <= btn_continuar[1] + btn_continuar[3]
        hover_novo = btn_novo[0] <= mx <= btn_novo[0] + btn_novo[2] and btn_novo[1] <= my <= btn_novo[1] + btn_novo[3]
        hover_sair = btn_sair[0] <= mx <= btn_sair[0] + btn_sair[2] and btn_sair[1] <= my <= btn_sair[1] + btn_sair[3]
        
        draw_mc_button(surface, *btn_continuar, "CONTINUAR", (69, 123, 157), hover_cont)
        draw_mc_button(surface, *btn_novo, "NOVO DESAFIO", (200, 120, 40), hover_novo)
        draw_mc_button(surface, *btn_sair, "SAIR PARA O MENU", (200, 50, 50), hover_sair)
        
        if pygame.mouse.get_pressed()[0]:
            if hover_cont: return "continuar"
            if hover_novo: return "novo"
            if hover_sair: return "sair"
    else:
        btn_continuar = (INTERNAL_W // 2 - 150, 220, 300, 50)
        btn_sair = (INTERNAL_W // 2 - 150, 290, 300, 50)
        
        hover_cont = btn_continuar[0] <= mx <= btn_continuar[0] + btn_continuar[2] and btn_continuar[1] <= my <= btn_continuar[1] + btn_continuar[3]
        hover_sair = btn_sair[0] <= mx <= btn_sair[0] + btn_sair[2] and btn_sair[1] <= my <= btn_sair[1] + btn_sair[3]
        
        draw_mc_button(surface, *btn_continuar, "CONTINUAR", (69, 123, 157), hover_cont)
        draw_mc_button(surface, *btn_sair, "SAIR PARA SELECAO", (200, 50, 50), hover_sair)
        
        if pygame.mouse.get_pressed()[0]:
            if hover_cont: return "continuar"
            if hover_sair: return "sair"
            
    return None

def play_practice(window, surface, clock, mode):
    phase = generate_random_phase(mode)
    setup_camera(phase) # <--- Ativa o zoom
    
    input_text = "y="
    show_preview = False
    anim = new_anim()
    result_msg = None
    error_reason = ""
    attempts = MAX_ATTEMPTS
    shot = None
    show_graph = False
    paused = False

    while True:
        clock.tick(60)
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        
        if paused:
            action = draw_pause_menu(surface, mouse_pos, SCALE, is_practice=True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'quit'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = False
            if action == "continuar":
                paused = False
            elif action == "novo":
                phase = generate_random_phase(mode)
                setup_camera(phase) # <--- Ativa o zoom
                input_text = "y="
                attempts, result_msg, show_preview = MAX_ATTEMPTS, None, False
                anim = new_anim()
                shot = None
                show_graph = False
                paused = False
            elif action == "sair":
                return 'menu'
                
            scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
            window.blit(scaled, (0, 0))
            pygame.display.flip()
            continue

        continue_key = False
        click_pos = None
        can_type = anim['phase'] == 'idle' and result_msg is None and not show_graph

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_pos = (event.pos[0] // SCALE, event.pos[1] // SCALE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                if event.key == pygame.K_RETURN:
                    if show_graph: continue_key = True
                    elif result_msg is not None: show_graph = True
                    elif can_type:
                        anim['phase'] = 'pull'
                        anim['start'] = now
                        show_preview = False
                elif event.key == pygame.K_BACKSPACE and can_type:
                    input_text = input_text[:-1] if len(input_text) > 2 else "y="
                elif can_type and event.unicode and len(input_text) < MAX_EXPR_LEN:
                    ch = event.unicode.lower()
                    if ch == ',': ch = '.'
                    if ch in TYPEABLE: input_text += ch

        if show_graph:
            draw_cartesian_graph(surface, phase, shot['f'] if shot else None, anim['arrow_x'], anim['hit'], input_text)
            if click_pos or continue_key:
                if anim['hit']:
                    phase = generate_random_phase(mode)
                    setup_camera(phase) # <--- Ativa o zoom
                    input_text = "y="
                    attempts, result_msg, show_preview = MAX_ATTEMPTS, None, False
                    anim = new_anim()
                    shot = None
                    show_graph = False
                elif attempts <= 0:
                    attempts, result_msg, show_preview = MAX_ATTEMPTS, None, False
                    anim = new_anim()
                    shot = None
                    show_graph = False
                else:
                    result_msg, show_preview, show_graph = None, False, False
                    anim = new_anim()
                    shot = None
            scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
            window.blit(scaled, (0, 0))
            pygame.display.flip()
            continue

        draw_mario_bg(surface, 0)
        for obs in phase['obstacles']: draw_obstacle(surface, obs)

        steve_scale = max(1, int(2 * (CAMERA_UNIT / GAME_UNIT)))
        ax, ay = world_to_px(phase['archer']['x'], phase['archer']['y'])
        draw_sprite(surface, STEVE, ax - 6 * steve_scale, ay - 8 * steve_scale, scale=steve_scale)
        draw_bow(surface, ax, ay, 0, anim['pull'] if anim['phase'] == 'pull' else 0)
        target_scale = max(1, int(2 * (CAMERA_UNIT / GAME_UNIT)))
        tx, ty = world_to_px(phase['target']['x'], phase['target']['y'])
        draw_sprite(surface, TARGET, tx - 8 * target_scale, ty - 8 * target_scale, scale=target_scale)

        if show_preview and anim['phase'] == 'idle' and result_msg is None:
            f_prev, _ = compile_expr(input_text[2:])
            if f_prev:
                x_prev = phase['archer']['x']
                while x_prev <= phase['target']['x'] + 1:
                    y_prev = f_prev(x_prev)
                    if y_prev is not None and -0.5 < y_prev < 20:
                        sx, sy = world_to_px(x_prev, y_prev)
                        pygame.draw.circle(surface, PREVIEW_COLOR, (sx, sy), 2)
                    x_prev += 0.15

        if anim['phase'] == 'pull':
            t = (now - anim['start']) / 300.0
            anim['pull'] = min(1, t)
            if t >= 1.1:
                shot = evaluate_shot(phase, input_text[2:])
                anim['arrow_x'] = phase['archer']['x']
                anim['arrow_y'] = phase['archer']['y']
                anim['phase'] = 'fly'
                anim['start'] = now
        elif anim['phase'] == 'fly':
            t = (now - anim['start']) / 1000.0
            f = shot['f']
            arrow_x = phase['archer']['x'] + t * 12
            finished = f is None or arrow_x >= shot['stop_x']
            if finished: arrow_x = shot['stop_x']
            arrow_y = f(arrow_x) if f else None
            anim['arrow_x'] = arrow_x
            anim['arrow_y'] = arrow_y if arrow_y is not None else anim['arrow_y']
            if finished:
                anim['phase'] = 'impact'
                anim['hit'] = shot['hit']
                anim['impact_start'] = now
        elif anim['phase'] == 'impact' and (now - anim['impact_start']) > 500:
            result_msg = 'hit' if anim['hit'] else 'miss'
            if not anim['hit']:
                attempts -= 1
                error_reason = shot['reason']
            anim['phase'] = 'done'

        if anim['phase'] in ('fly', 'impact', 'done') and shot is not None and shot['f'] is not None:
            trail_color = TRAIL_COLOR_HIT if anim['hit'] else TRAIL_COLOR_MISS
            draw_trail(surface, shot['f'], phase['archer']['x'], anim['arrow_x'], trail_color)

        if anim['phase'] in ('fly', 'impact'):
            draw_arrow(surface, shot['f'] if shot else None, anim['arrow_x'], anim['arrow_y'])

        pygame.draw.rect(surface, (30, 30, 40), (0, 320, INTERNAL_W, 160))
        pygame.draw.line(surface, (100, 100, 110), (0, 320), (INTERNAL_W, 320), 3)
        pygame.draw.rect(surface, (255, 255, 255), (20, 330, 300, 44))
        pygame.draw.rect(surface, (100, 100, 100), (20, 330, 300, 44), 2)
        draw_text(surface, input_text, 30, 344 if len(input_text) <= 14 else 350, 28 if len(input_text) <= 14 else 20, (0, 0, 0))

        mx, my = pygame.mouse.get_pos()
        mx, my = mx // SCALE, my // SCALE
        clicked_key = None
        for r, row in enumerate(KEYS):
            for c, key in enumerate(row):
                kx, ky, kw, kh = 20 + c * 48, 384 + r * 22, 44, 18
                color, text_color = (220, 220, 220), (0, 0, 0)
                if kx <= mx <= kx + kw and ky <= my <= ky + kh: color = (255, 255, 150)
                if click_pos and can_type and kx <= click_pos[0] <= kx + kw and ky <= click_pos[1] <= ky + kh: clicked_key = key
                pygame.draw.rect(surface, color, (kx, ky, kw, kh))
                pygame.draw.rect(surface, (150, 150, 150), (kx, ky, kw, kh), 2)
                draw_text(surface, key, kx + kw // 2, ky + kh // 2, 22 if len(key) == 1 else 16, text_color, center=True)

        btn_prev = (330, 340, 280, 50)
        btn_fire = (330, 410, 280, 50)
        pygame.draw.rect(surface, (69, 123, 157), btn_prev)
        pygame.draw.rect(surface, (100, 160, 200), btn_prev, 3)
        draw_text(surface, "PREVISAO", btn_prev[0] + btn_prev[2] // 2, btn_prev[1] + btn_prev[3] // 2, 26, (255, 255, 255), center=True)
        pygame.draw.rect(surface, (200, 50, 50), btn_fire)
        pygame.draw.rect(surface, (255, 100, 100), btn_fire, 3)
        draw_text(surface, "ATIRAR", btn_fire[0] + btn_fire[2] // 2, btn_fire[1] + btn_fire[3] // 2, 26, (255, 255, 255), center=True)

        def inside(btn): return click_pos and btn[0] <= click_pos[0] <= btn[0] + btn[2] and btn[1] <= click_pos[1] <= btn[1] + btn[3]
        if click_pos and result_msg is None:
            if inside(btn_prev): show_preview = not show_preview
            elif inside(btn_fire):
                if anim['phase'] == 'idle':
                    anim['phase'] = 'pull'
                    anim['start'] = now
                    show_preview = False
            elif clicked_key:
                if clicked_key == 'C': input_text = "y="
                elif clicked_key == '<': input_text = input_text[:-1] if len(input_text) > 2 else "y="
                elif len(input_text) + len(clicked_key) <= MAX_EXPR_LEN: input_text += clicked_key

        pygame.draw.rect(surface, (0, 0, 0), (0, 0, INTERNAL_W, 40))
        draw_text(surface, f"MODO PRATICAR - {phase['tipo'].upper()}", 10, 8, 28, (255, 220, 100))
        
        pygame.draw.rect(surface, (20, 20, 30), (336, 48, 296, 132))
        pygame.draw.rect(surface, (255, 220, 100), (336, 48, 296, 132), 2)
        draw_text(surface, f"Arqueiro: (x={phase['archer']['x']:g}, y={phase['archer']['y']:g})", 344, 54, 18, (255, 255, 255))
        draw_text(surface, f"Alvo:     (x={phase['target']['x']:g}, y={phase['target']['y']:g})", 344, 76, 18, (255, 255, 255))
        for i, line in enumerate(wrap_lines(phase['goal'], 18, 276)[:3]):
            draw_text(surface, line, 344, 102 + i * 20, 18, (255, 220, 100))

        if result_msg and not show_graph:
            overlay = pygame.Surface((INTERNAL_W, INTERNAL_H))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            msg = "ACERTOU!" if result_msg == 'hit' else "ERROU!"
            color = (42, 157, 143) if result_msg == 'hit' else (230, 57, 70)
            draw_text(surface, msg, INTERNAL_W // 2, 140, 60, color, center=True)
            
            if result_msg == 'hit':
                lines = wrap_lines(phase['tip'], 22, 580)[:4]
                for i, line in enumerate(lines):
                    draw_text(surface, line, INTERNAL_W // 2, 210 + i * 30, 22, (255, 255, 255), center=True)
            else:
                reason_lines = wrap_lines(error_reason, 22, 580)[:3]
                hint_lines = wrap_lines(phase['miss_hint'], 20, 580)[:3]
                for i, line in enumerate(reason_lines):
                    draw_text(surface, line, INTERNAL_W // 2, 210 + i * 28, 22, (255, 255, 255), center=True)
                for i, line in enumerate(hint_lines):
                    draw_text(surface, line, INTERNAL_W // 2, 210 + (len(reason_lines) + i) * 28 + 12, 20, (255, 220, 100), center=True)

            draw_text(surface, "Clique ou ENTER para ver o grafico", INTERNAL_W // 2, 410, 24, (200, 200, 200), center=True)
            if click_pos or continue_key: show_graph = True

        scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
        window.blit(scaled, (0, 0))
        pygame.display.flip()


def play(window, surface, clock, chapter_num):
    phases = phases_for(chapter_num)
    if not phases: return 'menu'
    phase_idx = 0
    phase = phases[phase_idx]
    setup_camera(phase) # <--- Ativa o zoom
    
    input_text = "y="
    show_preview = False
    anim = new_anim()
    result_msg = None
    error_reason = ""
    attempts = MAX_ATTEMPTS
    errors = 0
    shot = None
    show_graph = False
    paused = False

    while True:
        clock.tick(60)
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        if paused:
            action = draw_pause_menu(surface, mouse_pos, SCALE, is_practice=False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'quit'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = False
            if action == "continuar":
                paused = False
            elif action == "sair":
                return 'menu'
                
            scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
            window.blit(scaled, (0, 0))
            pygame.display.flip()
            continue

        continue_key = False
        click_pos = None
        can_type = anim['phase'] == 'idle' and result_msg is None and not show_graph

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_pos = (event.pos[0] // SCALE, event.pos[1] // SCALE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                if event.key == pygame.K_RETURN:
                    if show_graph: continue_key = True
                    elif result_msg is not None: show_graph = True
                    elif can_type:
                        anim['phase'] = 'pull'
                        anim['start'] = now
                        show_preview = False
                elif event.key == pygame.K_BACKSPACE and can_type:
                    input_text = input_text[:-1] if len(input_text) > 2 else "y="
                elif can_type and event.unicode and len(input_text) < MAX_EXPR_LEN:
                    ch = event.unicode.lower()
                    if ch == ',': ch = '.'
                    if ch in TYPEABLE: input_text += ch

        if show_graph:
            draw_cartesian_graph(surface, phase, shot['f'] if shot else None, anim['arrow_x'], anim['hit'], input_text)
            if click_pos or continue_key:
                if anim['hit']:
                    if phase_idx + 1 >= len(phases):
                        data = savemod.load()
                        savemod.complete_chapter(data, chapter_num, stars_for(errors))
                        return 'menu'
                    phase_idx += 1
                    phase = phases[phase_idx]
                    setup_camera(phase) # <--- Ativa o zoom
                    input_text = "y="
                    attempts, result_msg, show_preview = MAX_ATTEMPTS, None, False
                    anim = new_anim()
                    shot = None
                    show_graph = False
                elif attempts <= 0: return 'menu'
                else:
                    result_msg, show_preview, show_graph = None, False, False
                    anim = new_anim()
                    shot = None
            scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
            window.blit(scaled, (0, 0))
            pygame.display.flip()
            continue

        
        draw_mario_bg.fase_atual = phase_idx
        draw_mario_bg(surface, chapter_num)
        for obs in phase['obstacles']: draw_obstacle(surface, obs)
        steve_scale = max(1, int(2 * (CAMERA_UNIT / GAME_UNIT)))
        ax, ay = world_to_px(phase['archer']['x'], phase['archer']['y'])
        draw_sprite(surface, STEVE, ax - 6 * steve_scale, ay - 8 * steve_scale, scale=steve_scale)
        draw_bow(surface, ax, ay, 0, anim['pull'] if anim['phase'] == 'pull' else 0)
        target_scale = max(1, int(2 * (CAMERA_UNIT / GAME_UNIT)))
        tx, ty = world_to_px(phase['target']['x'], phase['target']['y'])
        draw_sprite(surface, TARGET, tx - 8 * target_scale, ty - 8 * target_scale, scale=target_scale)

        if show_preview and anim['phase'] == 'idle' and result_msg is None:
            f_prev, _ = compile_expr(input_text[2:])
            if f_prev:
                x_prev = phase['archer']['x']
                while x_prev <= phase['target']['x'] + 1:
                    y_prev = f_prev(x_prev)
                    if y_prev is not None and -0.5 < y_prev < 20:
                        sx, sy = world_to_px(x_prev, y_prev)
                        pygame.draw.circle(surface, PREVIEW_COLOR, (sx, sy), 2)
                    x_prev += 0.15

        if anim['phase'] == 'pull':
            t = (now - anim['start']) / 300.0
            anim['pull'] = min(1, t)
            if t >= 1.1:
                shot = evaluate_shot(phase, input_text[2:])
                anim['arrow_x'] = phase['archer']['x']
                anim['arrow_y'] = phase['archer']['y']
                anim['phase'] = 'fly'
                anim['start'] = now
        elif anim['phase'] == 'fly':
            t = (now - anim['start']) / 1000.0
            f = shot['f']
            arrow_x = phase['archer']['x'] + t * 12
            finished = f is None or arrow_x >= shot['stop_x']
            if finished: arrow_x = shot['stop_x']
            arrow_y = f(arrow_x) if f else None
            anim['arrow_x'] = arrow_x
            anim['arrow_y'] = arrow_y if arrow_y is not None else anim['arrow_y']
            if finished:
                anim['phase'] = 'impact'
                anim['hit'] = shot['hit']
                anim['impact_start'] = now
        elif anim['phase'] == 'impact' and (now - anim['impact_start']) > 500:
            result_msg = 'hit' if anim['hit'] else 'miss'
            if not anim['hit']:
                attempts -= 1
                errors += 1
                error_reason = shot['reason']
            anim['phase'] = 'done'

        if anim['phase'] in ('fly', 'impact', 'done') and shot is not None and shot['f'] is not None:
            trail_color = TRAIL_COLOR_HIT if anim['hit'] else TRAIL_COLOR_MISS
            draw_trail(surface, shot['f'], phase['archer']['x'], anim['arrow_x'], trail_color)
        if anim['phase'] in ('fly', 'impact'):
            draw_arrow(surface, shot['f'] if shot else None, anim['arrow_x'], anim['arrow_y'])

        pygame.draw.rect(surface, (30, 30, 40), (0, 320, INTERNAL_W, 160))
        pygame.draw.line(surface, (100, 100, 110), (0, 320), (INTERNAL_W, 320), 3)
        pygame.draw.rect(surface, (255, 255, 255), (20, 330, 300, 44))
        pygame.draw.rect(surface, (100, 100, 100), (20, 330, 300, 44), 2)
        draw_text(surface, input_text, 30, 344 if len(input_text) <= 14 else 350, 28 if len(input_text) <= 14 else 20, (0, 0, 0))

        mx, my = pygame.mouse.get_pos()
        mx, my = mx // SCALE, my // SCALE
        clicked_key = None
        for r, row in enumerate(KEYS):
            for c, key in enumerate(row):
                kx, ky, kw, kh = 20 + c * 48, 384 + r * 22, 44, 18
                color, text_color = (220, 220, 220), (0, 0, 0)
                if kx <= mx <= kx + kw and ky <= my <= ky + kh: color = (255, 255, 150)
                if click_pos and can_type and kx <= click_pos[0] <= kx + kw and ky <= click_pos[1] <= ky + kh: clicked_key = key
                pygame.draw.rect(surface, color, (kx, ky, kw, kh))
                pygame.draw.rect(surface, (150, 150, 150), (kx, ky, kw, kh), 2)
                draw_text(surface, key, kx + kw // 2, ky + kh // 2, 22 if len(key) == 1 else 16, text_color, center=True)

        btn_prev = (330, 340, 280, 50)
        btn_fire = (330, 410, 280, 50)
        pygame.draw.rect(surface, (69, 123, 157), btn_prev)
        pygame.draw.rect(surface, (100, 160, 200), btn_prev, 3)
        draw_text(surface, "PREVISAO", btn_prev[0] + btn_prev[2] // 2, btn_prev[1] + btn_prev[3] // 2, 26, (255, 255, 255), center=True)
        pygame.draw.rect(surface, (200, 50, 50), btn_fire)
        pygame.draw.rect(surface, (255, 100, 100), btn_fire, 3)
        draw_text(surface, "ATIRAR", btn_fire[0] + btn_fire[2] // 2, btn_fire[1] + btn_fire[3] // 2, 26, (255, 255, 255), center=True)

        def inside(btn): return click_pos and btn[0] <= click_pos[0] <= btn[0] + btn[2] and btn[1] <= click_pos[1] <= btn[1] + btn[3]
        if click_pos and result_msg is None:
            if inside(btn_prev): show_preview = not show_preview
            elif inside(btn_fire):
                if anim['phase'] == 'idle':
                    anim['phase'] = 'pull'
                    anim['start'] = now
                    show_preview = False
            elif clicked_key:
                if clicked_key == 'C': input_text = "y="
                elif clicked_key == '<': input_text = input_text[:-1] if len(input_text) > 2 else "y="
                elif len(input_text) + len(clicked_key) <= MAX_EXPR_LEN: input_text += clicked_key

        pygame.draw.rect(surface, (0, 0, 0), (0, 0, INTERNAL_W, 40))
        draw_text(surface, f"Fase {phase['id']} - {phase['tipo']}", 10, 8, 28, (255, 255, 255))
        draw_text(surface, f"Tentativas: {attempts}/{MAX_ATTEMPTS}", INTERNAL_W - 220, 8, 28, (255, 255, 255))

        pygame.draw.rect(surface, (20, 20, 30), (336, 48, 296, 132))
        pygame.draw.rect(surface, (255, 220, 100), (336, 48, 296, 132), 2)
        draw_text(surface, f"Arqueiro: (x={phase['archer']['x']:g}, y={phase['archer']['y']:g})", 344, 54, 18, (255, 255, 255))
        draw_text(surface, f"Alvo:     (x={phase['target']['x']:g}, y={phase['target']['y']:g})", 344, 76, 18, (255, 255, 255))
        for i, line in enumerate(wrap_lines(phase['goal'], 18, 276)[:3]):
            draw_text(surface, line, 344, 102 + i * 20, 18, (255, 220, 100))

        if result_msg and not show_graph:
            overlay = pygame.Surface((INTERNAL_W, INTERNAL_H))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            msg = "ACERTOU!" if result_msg == 'hit' else "ERROU!"
            color = (42, 157, 143) if result_msg == 'hit' else (230, 57, 70)
            draw_text(surface, msg, INTERNAL_W // 2, 140, 60, color, center=True)

            if result_msg == 'hit':
                lines = wrap_lines(phase['tip'], 22, 580)[:4]
                for i, line in enumerate(lines):
                    draw_text(surface, line, INTERNAL_W // 2, 210 + i * 30, 22, (255, 255, 255), center=True)
            else:
                reason_lines = wrap_lines(error_reason, 22, 580)[:3]
                hint_lines = wrap_lines(phase['miss_hint'], 20, 580)[:3]
                for i, line in enumerate(reason_lines):
                    draw_text(surface, line, INTERNAL_W // 2, 210 + i * 28, 22, (255, 255, 255), center=True)
                for i, line in enumerate(hint_lines):
                    draw_text(surface, line, INTERNAL_W // 2, 210 + (len(reason_lines) + i) * 28 + 12, 20, (255, 220, 100), center=True)

            draw_text(surface, "Clique ou ENTER para ver o grafico", INTERNAL_W // 2, 410, 24, (200, 200, 200), center=True)
            if click_pos or continue_key: show_graph = True

        scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
        window.blit(scaled, (0, 0))
        pygame.display.flip()