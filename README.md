#  Function Archer

**Function Archer** é um jogo educativo 2D desenvolvido em Python com a biblioteca Pygame, criado para tornar o aprendizado de matemática mais visual, interativo e acessível.

A proposta do jogo é transformar conceitos matemáticos em mecânicas de gameplay: o jogador controla a trajetória de uma flecha por meio da escrita de funções matemáticas. Para acertar os alvos e superar os obstáculos, é necessário compreender e aplicar os conceitos estudados.

Além da experiência prática, o projeto conta com um módulo teórico integrado, no qual o jogador pode estudar os fundamentos matemáticos abordados no jogo.

---

##  Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Executar](#-como-executar)
- [Conteúdo Matemático](#-conteúdo-matemático)
- [Documentação de Uso de Inteligência Artificial](#-documentação-de-uso-de-inteligência-artificial)
- [Autores](#-autores)

---

##  Sobre o Projeto

O aprendizado de funções e conceitos do cálculo diferencial e integral pode ser desafiador devido ao seu caráter abstrato. Muitas vezes, o estudante precisa interpretar equações e gráficos sem conseguir visualizar diretamente suas aplicações.

O **Function Archer** busca aproximar a teoria da prática por meio de uma experiência interativa.

A mecânica principal consiste em inserir uma equação matemática para determinar a trajetória de uma flecha. A partir da função digitada, o jogo desenha a curva correspondente e simula o percurso do projétil até o alvo.

O projeto apresenta uma identidade visual inspirada em jogos retrô, utilizando elementos de **pixel art**. O menu principal possui uma estética baseada em jogos de construção por blocos, enquanto o primeiro mundo apresenta uma ambientação de plataforma 2D.

O objetivo é proporcionar uma experiência de aprendizagem na qual o jogador possa experimentar, observar resultados, identificar erros e compreender melhor o comportamento das funções matemáticas.

##  Funcionalidades

### Menu e navegação
- **Menu principal interativo:** acesso às opções de jogar e aprender.
- **Seleção de mundos:** mapa de progressão das fases com estética de blocos tridimensionais.
- **Sistema de progresso:** salvamento das informações do jogador em arquivo JSON.

### Módulo Aprender
- Conteúdo teórico integrado à experiência do jogo.
- Explicações sobre funções, limites, derivadas e integrais.
- Organização dos conteúdos conforme os assuntos trabalhados na disciplina de Cálculo Diferencial e Integral.

### Mecânicas de gameplay
- **Trajetória baseada em funções:** o jogador insere equações matemáticas para determinar o caminho da flecha.
- **Previsão de trajetória:** visualização da curva matemática antes de realizar o disparo.
- **Teclado virtual:** botões integrados à interface para facilitar a inserção de operadores e caracteres matemáticos, como o expoente `^`.
- **Obstáculos e alvos:** desafios que exigem a construção de funções adequadas para alcançar os objetivos.
- **Feedback inteligente:** ao errar o disparo, o jogo analisa a trajetória e informa se a flecha passou acima ou abaixo do alvo, auxiliando o jogador a corrigir a equação.

### Exemplos de equações

O sistema permite trabalhar com diferentes expressões matemáticas, como:

| Tipo de função | Exemplo |
|---|---|
| Constante | `y = 3` |
| Afim (1º grau) | `y = 2*x + 1` |
| Quadrática (2º grau) | `y = 2*x^2 + 3*x + 1` |

A trajetória gerada depende da expressão inserida pelo jogador.

##  Tecnologias Utilizadas

| Tecnologia | Aplicação |
|---|---|
| **Python 3.10+** | Linguagem principal do projeto. |
| **Pygame 2.6+** | Desenvolvimento da interface gráfica, renderização, eventos e mecânicas do jogo. |
| **JSON** | Armazenamento do progresso do jogador. |
| **Markdown** | Documentação do projeto. |

O projeto também utiliza um mecanismo de avaliação de expressões matemáticas para interpretar as equações inseridas pelo jogador. A avaliação deve ser restrita às operações e expressões matemáticas permitidas pelo jogo.

##  Estrutura do Projeto

A organização dos arquivos busca separar as responsabilidades de interface, lógica de gameplay, configurações e recursos visuais.

```text
jogo-funcao/
│
├── src/
│   ├── main.py          # Ponto de entrada e gerenciamento dos estados do jogo
│   ├── config.py        # Configurações gerais e dimensões da tela
│   ├── palette.py       # Paleta de cores e estilos visuais
│   ├── sprites.py       # Matrizes de desenho dos personagens e cenários
│   ├── renderer.py      # Funções auxiliares de renderização
│   ├── save.py          # Sistema de salvamento de progresso em JSON
│   ├── menu.py          # Menus principal e de seleção de mundos
│   ├── learn.py         # Interface e conteúdo do módulo teórico
│   └── game.py          # Gameplay, física e avaliação das funções
│
├── .gitignore           # Arquivos e diretórios ignorados pelo Git
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação principal
```

##  Como Executar

Siga as etapas abaixo para executar o Function Archer em sua máquina.

### 1. Pré-requisitos

Antes de começar, certifique-se de possuir:

- Python 3.10 ou superior instalado.
- Git instalado para clonar o repositório.
- Terminal ou editor de código de sua preferência.

### 2. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/jogo-funcao.git
```

Entre no diretório do projeto:

```bash
cd jogo-funcao
```

> Substitua `SEU-USUARIO` pelo nome de usuário ou organização responsável pelo repositório no GitHub.

### 3. Crie um ambiente virtual

O ambiente virtual permite instalar as dependências do projeto sem interferir nas demais instalações do Python em sua máquina.

**Windows:**

```bash
python -m venv .venv
```

Para ativar no PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Para ativar no Prompt de Comando (CMD):

```cmd
.venv\Scripts\activate.bat
```

**Linux ou macOS:**

```bash
python3 -m venv .venv
```

Ative o ambiente:

```bash
source .venv/bin/activate
```

### 4. Instale as dependências

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

### 5. Execute o jogo

Para iniciar o Function Archer, utilize:

```bash
python src/main.py
```

No Linux ou macOS, caso necessário, utilize:

```bash
python3 src/main.py
```

---

##  Conteúdo Matemático

O Function Archer foi desenvolvido para trabalhar quatro conteúdos fundamentais da disciplina de Cálculo Diferencial e Integral (CDI).

Os assuntos são apresentados de maneira integrada, combinando explicações teóricas e aplicações interativas.

### 1. Funções

**Aula 1 — Funções e suas aplicações**

É o principal conteúdo aplicado na mecânica de gameplay.

O jogador utiliza expressões matemáticas para determinar a trajetória da flecha, trabalhando especialmente com:

- Funções constantes;
- Funções afins (1º grau);
- Funções quadráticas (2º grau);
- Coeficientes e comportamento dos gráficos.

A proposta é demonstrar visualmente como a alteração de uma expressão modifica o gráfico e, consequentemente, a trajetória do projétil.

### 2. Limites

**Aula 2 — Conceito de limite**

O módulo teórico apresenta o conceito de limites, abordando a ideia de aproximação e tendência de uma função quando a variável se aproxima de determinado valor.

O conteúdo também serve como base para futuras mecânicas e desafios envolvendo alvos móveis e situações de aproximação.

### 3. Derivadas

**Aula 3 — Taxa de variação instantânea**

O conteúdo apresenta a derivada como uma ferramenta matemática utilizada para determinar a taxa de variação instantânea de uma função.

Também são abordados conceitos relacionados à inclinação da reta tangente a uma curva e à interpretação do comportamento de uma função em determinado ponto.

### 4. Integrais

**Aula 4 — Acumulação e área sob a curva**

O módulo apresenta o conceito de integral e sua relação com o cálculo de áreas e o acúmulo de grandezas.

A proposta é utilizar a visualização gráfica para facilitar a compreensão da área sob uma curva e de sua interpretação matemática.

> **Observação:** na versão atual, a mecânica principal de gameplay está concentrada no conteúdo de funções. Limites, derivadas e integrais também são abordados no módulo teórico, servindo de base para possíveis expansões das mecânicas e das fases.

---

##  Documentação de Uso de Inteligência Artificial

Durante o desenvolvimento do Function Archer, foram utilizadas ferramentas de Inteligência Artificial como apoio ao processo de programação, organização e documentação do projeto.

**Ferramenta utilizada:** ChatGPT (OpenAI).

**Finalidades de utilização:**
- Auxílio na estruturação e organização do código-fonte.
- Apoio na implementação de elementos gráficos e recursos visuais em pixel art.
- Investigação e resolução de problemas relacionados à biblioteca Pygame.
- Apoio na construção de lógicas matemáticas e mecânicas de gameplay.
- Auxílio na formatação de textos e implementação de quebra automática de linhas.
- Revisão e aprimoramento da documentação do repositório.

**Validação humana:**

As sugestões fornecidas pela Inteligência Artificial foram utilizadas como suporte ao desenvolvimento, não substituindo a análise e a tomada de decisões dos integrantes da equipe.

Os integrantes ficaram responsáveis por revisar, testar e adaptar as implementações, realizando ajustes na identidade visual, na lógica de colisões, nos cálculos matemáticos e na interface do usuário.

O uso dessas ferramentas teve como objetivo auxiliar o desenvolvimento, mantendo a responsabilidade técnica e a validação das funcionalidades sob responsabilidade da equipe.

---

##  Autores

Projeto desenvolvido por:

- Jefferson Gustavo Fernandes Estevam
- João Edu Araújo Silva
- Pedro Lucas Batista Pereira
- Thiago Lopes Teobaldo

**Disciplina:** Cálculo Diferencial e Integral, Algoritmo.

**Instituição:** UniCatólica.

---

<p align="center">
  <strong>Function Archer — Aprender matemática também pode ser uma aventura.</strong>
</p>
