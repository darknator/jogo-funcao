Function Archer

O Function Archer é um jogo educativo 2D desenvolvido em Python com a biblioteca Pygame. O objetivo do projeto é ensinar matemática de forma lúdica e interativa, permitindo que o jogador controle a trajetória de uma flecha através da escrita de funções matemáticas.

O jogador deve digitar a equação correta para que a flecha atinja o alvo, desviando de obstáculos. O jogo conta com um sistema de feedback inteligente que explica o motivo do erro, além de um módulo teórico integrado para o estudo dos conceitos.
Sumário

    Sobre o Projeto

    Funcionalidades

    Tecnologias Utilizadas

    Estrutura do Projeto

    Como Executar

    Conteúdo Matemático

    Documentação de Uso de IA

    Autores

Sobre o Projeto

O aprendizado de funções e cálculos matemáticos costuma ser abstrato para muitos estudantes. O Function Archer propõe a visualização imediata desses conceitos. Ao inserir uma equação no jogo, o jogador vê instantaneamente a curva sendo traçada e a flecha seguindo exatamente aquele caminho.

O projeto foi construído visando a interface e a experiência do usuário, utilizando uma estética pixel art. O menu principal é inspirado em jogos de blocos (estilo Minecraft) e o primeiro mundo possui temática retrô de plataforma 2D.
Funcionalidades

    Menu Interativo: Tela inicial com opções de Jogar e Aprender.

    Módulo Aprender: Área de leitura com explicações detalhadas sobre Funções, Limites, Derivadas e Integrais.

    Seleção de Mundos: Mapa de fases progressivo no estilo blocos 3D.

    Gameplay Baseado em Funções: O jogador digita a equação (ex: y=2x+1 ou y=3) e o jogo calcula o voo da flecha.

    Teclado Virtual Integrado: Interface com botões na tela para inserção de caracteres especiais, como o expoente (^).

    Previsão de Trajetória: Ferramenta para desenhar a curva da função antes de atirar.

    Feedback Inteligente: Se o jogador errar, o sistema calcula onde a flecha passou no eixo X e informa se ela passou por cima ou por baixo do alvo, auxiliando no ajuste da equação.

Tecnologias Utilizadas

    Python 3.10+: Linguagem base do projeto.

    Pygame 2.6+: Biblioteca para renderização gráfica, controle de framerate e captura de eventos.

    Eval (Seguro): Uso restrito para processar expressões matemáticas digitadas pelo jogador.

    Markdown: Para a documentação do repositório.

Estrutura do Projeto
jogo-funcao/
├── src/
│   ├── main.py          # Ponto de entrada, gerencia os estados do jogo
│   ├── config.py        # Constantes de tela, dimensões e configurações
│   ├── palette.py       # Paleta de cores e estilos visuais
│   ├── sprites.py       # Matrizes de desenho dos personagens e cenário
│   ├── renderer.py      # Funções auxiliares de desenho (textos, sprites)
│   ├── save.py          # Sistema de salvamento de progresso (JSON)
│   ├── menu.py          # Interface dos menus principal e de seleção
│   ├── learn.py         # Interface do módulo teórico
│   └── game.py          # Lógica de gameplay, física e avaliação de funções
├── .gitignore           # Arquivos ignorados pelo Git
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação

Como Executar
Pré-requisitos

É necessário ter o Python instalado em sua máquina.
Passo a Passo

1. Clone o repositório:
bash

git clone https://github.com/seu-usuario/jogo-funcao.git
cd jogo-funcao

2. Crie e ative um ambiente virtual (venv):

No Windows:
bash

python -m venv .venv
.venv\Scripts\activate

No Linux ou Mac:
bash

python3 -m venv .venv
source .venv/bin/activate

3. Instale as dependências:
bash

pip install -r requirements.txt

4. Execute o jogo:
bash

python src/main.py

Conteúdo Matemático

O projeto aborda os quatro eixos exigidos na disciplina, integrando teoria e prática:

    Funções (Aula 1): O jogo trabalha diretamente com funções constantes, afins (primeiro grau) e quadráticas. A mecânica principal consiste em aplicar os coeficientes (a, b, c) no cálculo da trajetória (eixo y) em relação ao deslocamento (eixo x).

    Limites (Aula 2): Conceito explorado no módulo "Aprender" e planejado para futuras fases onde alvos móveis exigirão a compreensão de aproximação e tendência de valores.

    Derivadas (Aula 3): Apresentado no módulo teórico como a taxa de variação instantânea, correlacionando com a inclinação da reta tangente à trajetória da flecha no ar.

    Integrais (Aula 4): Apresentado no módulo teórico como o cálculo de área sob a curva, com foco no acúmulo de grandezas (ex: área percorrida abaixo da trajetória da flecha).

Documentação de Uso de IA

Em conformidade com as diretrizes de avaliação, documentamos o uso de ferramentas de Inteligência Artificial durante o desenvolvimento.

    Ferramenta Utilizada: [Coloque aqui o nome da IA, ex: ChatGPT, Claude]

    Objetivo: Auxílio na estruturação inicial do código, lógica de renderização de pixel art, resolução de bugs relacionados ao Pygame e formatação de texto com quebra de linha automática.

    Validação Humana: Todos os trechos de código sugeridos pela IA passaram por revisão humana. Foram feitas adaptações na paleta de cores, ajustes na lógica de colisão (matemática vetorial) e adequações na interface de usuário para garantir que o jogo funcionasse corretamente e estivesse alinhado ao escopo pedagógico da disciplina.

Autores
