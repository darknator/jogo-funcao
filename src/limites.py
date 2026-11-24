
# MUNDO 3 - LIMITES
# Fases independentes dos mundos anteriores

PHASES_LIMITES = [
    {
        'id': '3-1',
        'chapter': 3,
        'tipo': 'Introducao aos limites',

        'archer': {'x': 0, 'y': 1},
        'target': {'x': 2, 'y': 3, 'r': 0.6},
        'obstacles': [],


        'goal': (
            'Limite de f(x) = x + 1 '
            'quando x tende a 2. '
            'Qual funcao leva a flecha ao alvo?'
),

        'dominio': 'R',
        'imagem': 'R',
        'solution': 'y=x+1',

        'tip': (
            'Em uma funcao continua, o limite pode ser '
            'calculado por substituicao direta. '
            'Quando x se aproxima de 2, x+1 se aproxima de 3.'
        ),

        'miss_hint': (
            'Substitua x por 2 na expressao x+1. '
            'O limite e 3. Para disparar, digite y=x+1.'
        )
    },

    {
        'id': '3-2',
        'chapter': 3,
        'tipo': 'Substituicao direta',

        'archer': {'x': 0, 'y': 1},
        'target': {'x': 3, 'y': 7, 'r': 0.8},
        'obstacles': [],

        'goal': (
            'Calcule o limite de f(x) = 2x + 1 '
            'quando x tende a 3. '
            'Digite a funcao para acertar o alvo.'
        ),

        'dominio': 'R',
        'imagem': 'R',
        'solution': 'y=2*x+1',

        'tip': (
            'Substitua x por 3 na funcao. '
            'Assim, 2 vezes 3 mais 1 resulta em 7.'
        ),

        'miss_hint': (
            'O limite e 7. A funcao 2x+1 '
            'parte de y=1 e passa pelo alvo (3,7). '
            'Digite y=2*x+1.'
        )
    },  
    {
        'id': '3-3',
        'chapter': 3,
        'tipo': 'Indeterminacao 0/0',

        'archer': {'x': 0, 'y': 2},
        'target': {'x': 2, 'y': 4, 'r': 0.8},
        'obstacles': [],

        'goal': (
            'Calcule o limite de '
            '(x^2-4)/(x-2) quando x tende a 2. '
            'Simplifique e dispare!'
        ),

        'dominio': 'R, exceto x=2',
        'imagem': 'R',
        'solution': 'y=x+2',

        'tip': (
            'A substituicao direta resulta em 0/0. '
            'Fatore x^2-4 como (x-2)(x+2). '
            'Simplifique para x+2, com x diferente de 2. '
            'O limite e 4.'
        ),

        'miss_hint': (
            'A expressao original nao esta definida '
            'em x=2. Simplifique a fracao primeiro. '
            'Digite y=x+2 para chegar ao alvo (2,4).'
        )
    },

    {
        'id': '3-4',
        'chapter': 3,
        'tipo': 'Limites laterais',

        'archer': {'x': 0, 'y': 2},
        'target': {'x': 2, 'y': 0, 'r': 0.8},
        'obstacles': [],

        'goal': (
            'Considere f(x) = abs(x-2). '
            'Calcule os limites laterais em x=2. '
            'Eles sao iguais? Dispare!'
        ),

        'dominio': 'R',
        'imagem': 'R',
        'solution': 'y=abs(x-2)',

        'tip': (
            'Quando x se aproxima de 2 pela esquerda '
            'ou pela direita, abs(x-2) se aproxima de 0. '
            'Portanto, o limite existe e vale 0.'
        ),

        'miss_hint': (
            'Os limites laterais sao iguais a 0. '
            'A funcao abs(x-2) passa pelo alvo (2,0). '
            'Digite y=abs(x-2).'
        )
    },

    {
        'id': '3-5',
        'chapter': 3,
        'tipo': 'Desafio final de limites',

        'archer': {'x': 0, 'y': 3},
        'target': {'x': 3, 'y': 6, 'r': 0.8},
        'obstacles': [],

        'goal': (
            'Desafio final! Calcule o limite de '
            '(x^2-9)/(x-3) quando x tende a 3. '
            'Simplifique e acerte o alvo!'
        ),

        'dominio': 'R, exceto x=3',
        'imagem': 'R',
        'solution': 'y=x+3',

        'tip': (
            'A substituicao direta gera 0/0. '
            'Fatore x^2-9 como (x-3)(x+3). '
            'Simplifique para x+3, com x diferente de 3. '
            'O limite e 6.'
        ),

        'miss_hint': (
            'Fatore o numerador e simplifique a fracao. '
            'O limite e 6. Digite y=x+3 '
            'para atingir o alvo (3,6).'
        )
    }

]
