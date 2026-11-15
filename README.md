# Function Archer

O Function Archer e um jogo educativo 2D desenvolvido em Python com a biblioteca Pygame. O objetivo do projeto e ensinar matematica de forma ludica e interativa, permitindo que o jogador controle a trajetoria de uma flecha atraves da escrita de funcoes matematicas.

O jogador deve digitar a equacao correta para que a flecha atinja o alvo, desviando de obstaculos. O jogo conta com um sistema de feedback inteligente que explica o motivo do erro, alem de um modulo teorico integrado para o estudo dos conceitos.

## Sumario

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Funcionalidades](#funcionalidades)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Como Executar](#como-executar)
6. [Conteudo Matematico](#conteudo-matematico)
7. [Documentacao de Uso de IA](#documentacao-de-uso-de-ia)
8. [Autores](#autores)

---

## Sobre o Projeto

O aprendizado de funcoes e calculos matematicos costuma ser abstrato para muitos estudantes. O Function Archer propoe a visualizacao imediata desses conceitos. Ao inserir uma equacao no jogo, o jogador ve instantaneamente a curva sendo tracada e a flecha seguindo exatamente aquele caminho.

O projeto foi construido visando a interface e a experiencia do usuario, utilizando uma estetica pixel art. O menu principal e inspirado em jogos de blocos (estilo Minecraft) e o primeiro mundo possui tematica retro de plataforma 2D.

## Funcionalidades

- **Menu Interativo:** Tela inicial com opcoes de Jogar e Aprender.
- **Modulo Aprender:** Area de leitura com explicacoes detalhadas sobre Funcoes, Limites, Derivadas e Integrais.
- **Selecao de Mundos:** Mapa de fases progressivo no estilo blocos 3D.
- **Gameplay Baseado em Funcoes:** O jogador digita a equacao (ex: `y=2x+1` ou `y=3`) e o jogo calcula o voo da flecha.
- **Teclado Virtual Integrado:** Interface com botoes na tela para insercao de caracteres especiais, como o expoente (`^`).
- **Previsao de Trajetoria:** Ferramenta para desenhar a curva da funcao antes de atirar.
- **Feedback Inteligente:** Se o jogador errar, o sistema calcula onde a flecha passou no eixo X e informa se ela passou por cima ou por baixo do alvo, auxiliando no ajuste da equacao.

## Tecnologias Utilizadas

- **Python 3.10+:** Linguagem base do projeto.
- **Pygame 2.6+:** Biblioteca para renderizacao grafica, controle de framerate e captura de eventos.
- **Eval (Seguro):** Uso restrito para processar expressoes matematicas digitadas pelo jogador.
- **Markdown:** Para a documentacao do repositorio.

## Estrutura do Projeto

```text
jogo-funcao/
├── src/
│   ├── main.py          # Ponto de entrada, gerencia os estados do jogo
│   ├── config.py        # Constantes de tela, dimensoes e configuracoes
│   ├── palette.py       # Paleta de cores e estilos visuais
│   ├── sprites.py       # Matrizes de desenho dos personagens e cenario
│   ├── renderer.py      # Funcoes auxiliares de desenho (textos, sprites)
│   ├── save.py          # Sistema de salvamento de progresso (JSON)
│   ├── menu.py          # Interface dos menus principal e de selecao
│   ├── learn.py         # Interface do modulo teorico
│   └── game.py          # Logica de gameplay, fisica e avaliacao de funcoes
├── .gitignore           # Arquivos ignorados pelo Git
├── requirements.txt     # Dependencias do projeto
└── README.md            # Documentacao

Como Executar
Pre-requisitos

E necessario ter o Python instalado em sua maquina e o ambiente virtual configurado.
Passo a Passo

    Clone o repositorio:

bash

git clone https://github.com/seu-usuario/jogo-funcao.git
cd jogo-funcao

    Crie e ative um ambiente virtual (venv):

bash

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

    Instale as dependencias:

bash

pip install -r requirements.txt

    Execute o jogo:

bash

python src/main.py

Conteudo Matematico

O projeto aborda os quatro eixos exigidos, integrando teoria e pratica:

    Funcoes (Aula 1): O jogo trabalha diretamente com funcoes constantes, afins (primeiro grau) e quadraticas. A mecanica principal consiste em aplicar os coeficientes (a, b, c) no calculo da trajetoria (eixo y) em relacao ao deslocamento (eixo x).

    Limites (Aula 2): Conceito explorado no modulo "Aprender" e planejado para futuras fases onde alvos moveis exigirao a compreensao de aproximacao e tendencia de valores.

    Derivadas (Aula 3): Apresentado no modulo teorico como a taxa de variacao instantanea, correlacionando com a inclinacao da reta tangente a trajetoria da flecha no ar.

    Integrais (Aula 4): Apresentado no modulo teorico como o calculo de area sob a curva, com foco no acumulo de grandezas (ex: area percorrida abaixo da trajetoria da flecha).

Documentacao de Uso de IA

Em conformidade com as diretrizes de avaliacao, documentamos o uso de ferramentas de Inteligencia Artificial durante o desenvolvimento.

    Ferramenta Utilizada: [Nome da Ferramenta - Ex: ChatGPT, Claude]

    Objetivo: Auxilio na estruturacao inicial do codigo, logica de renderizacao de pixel art, resolucao de bugs relacionados ao Pygame e formatacao de texto com quebra de linha automatica.

    Validacao Humana: Todos os trechos de codigo sugeridos pela IA passaram por revisao humana. Foram feitas adaptacoes na paleta de cores, ajustes na logica de colisao (matematica vetorial) e adequacoes na interface de usuario para garantir que o jogo funcionasse corretamente e estivesse alinhado ao escopo pedagogico.

Projeto desenvolvido para a disciplina de Calculo Diferencial e Integral (CDI).
