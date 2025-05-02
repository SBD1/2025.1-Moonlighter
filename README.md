# 2025.1-Moonlighter

![Capa Moonlighter](./assets/Moonlighter_Capa.webp)

<div align="center">

![GitHub repo size](https://img.shields.io/github/repo-size/SBD1/2025.1-Moonlighter?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/SBD1/2025.1-Moonlighter?style=for-the-badge)
![GitHub views](https://komarev.com/ghpvc/?username=SBD1&repo=2025.1-Moonlighter&color=blueviolet&style=for-the-badge&label=Views)

</div>

## 🎮 Sobre o Moonlighter:

Moonlighter é um jogo indie de ação e aventura com elementos de gerenciamento, desenvolvido pela Digital Sun e lançado em 2018. Nele, você controla Will, um comerciante que vive na pacata vila de Rynoka. Durante o dia, Will cuida da sua loja, vendendo itens, ajustando preços e interagindo com os clientes. Mas à noite, ele se aventura em masmorras misteriosas em busca de tesouros, enfrentando monstros e coletando recursos raros.

O jogo chama atenção pela sua mecânica de vida dupla — equilibrando combate em tempo real com um sistema econômico de venda e precificação de itens — além de seus visuais em pixel art e trilha sonora envolvente.

### 🧪 Nosso Projeto: Moonlighter no Terminal

O projeto se baseia em uma versão adaptada e simplificada do Moonlighter, executada diretamente no terminal. A ideia é recriar a essência da rotina de Will com foco em:

- Exploração de masmorras (via menus e opções textuais)
- Coleta de itens
- Controle de inventário
- Gestão de uma loja com clientes fictícios
- Simulação de vendas e lucro

A aplicação será construída em Python (interface em terminal), com toda a lógica de dados estruturada em PostgreSQL, utilizando SQL puro para modelagem, triggers, views e controle de acesso.

##  📝 Acesse a Documentação!

O conteúdo da documentação do projeto Moonlighter aborda os assuntos e atividades cobradas durante a disciplina de Sistema de Bancos de Dados 1 da Universidade de Brasília do Campus Faculdade de Ciências e Tecnologias em Engenharia - FCTE.

Para acessar a documentação do projeto, [Clique aqui!](sbd1.github.io/2025.1-Moonlighter/)

## 🗃️ Estrutura do Projeto:

O projeto Moonlighter é dividido em três ambientes principais, organizados dentro da pasta `/apps`. Cada um deles cumpre um papel específico na arquitetura do sistema, mantendo o projeto modular e fácil de navegar:

- `apps/cli`: Contém o código da interface em terminal desenvolvida em Python, responsável pela interação do usuário com o sistema. Aqui é onde o jogo acontece — você executa comandos, visualiza ações e interage com o banco por meio de menus e prompts.
- `apps/sql`: Abriga toda a lógica relacionada ao banco de dados PostgreSQL, utilizando apenas SQL puro. Inclui a criação de tabelas, inserção de dados (seeds), views, triggers e controles de acesso. Esta pasta é o "coração lógico" do sistema.
- `apps/docs`: Ambiente de documentação criado com MkDocs, voltado para explicar o funcionamento do projeto, decisões de arquitetura, DER/MER, comandos SQL utilizados, e instruções de uso. É também o que será publicado no GitHub Pages para facilitar o acesso à documentação do time ou de avaliadores.

Essa organização facilita a separação entre lógica do jogo, estrutura de dados e documentação, permitindo que cada parte evolua de forma independente, mas integrada.

## 🚀 Executando o Projeto:

O projeto utiliza de pacotes JavaScript para auxiliar na execução e padronização de qualidade para o time de desenvolvimento, se restringindo apenas para este uso. Portanto, é necessário que o usuário possua Node.Js na versão 22+.

O arquivo `package.json` dispõe de comandos que auxiliam a subir os diferentes ambientes de execução separadamente:

### Rodando a Documentação 📝

Para rodar a documentação em ambiente de desenvolvimento, é necessário:

- Python3 | Versão 3.12+
- PIP | Versão 24+ (Geralmente instalado junto com o Python)

Em versões de **Windows 10+ ou Ubuntu 22.04** execute o comando:

#### 1. Instale o mkdocs:
```shell
pip install mkdocs
```
#### 2. Instale o Tema _Meterial_ do mkdocs:
```shell
pip install mkdocs-material
```
#### 3. Inicialize a documentação localmente:
```shell
npm run devDoc
```

Para usuários com o **Ubuntu na versão 24.04** ou sistemas onde o Python está configurado para **impedir a instalação de pacotes globalmente com pip**, como uma medida de segurança (PEP 668) por conta do gerenciado de pacotes padrão: `apt`, utilize os passos abaixo:

#### 1. Inicialize um Ambiente Virtual:
```shell
python3 -m venv .venv
```

#### 2. Ative o Ambiente Virtual:
```shell
source .venv/bin/activate
```
#### 3. Instale o mkdocs:
```shell
pip install mkdocs
```

#### 4. Instale o Tema _Meterial_ do mkdocs:
```shell
pip install mkdocs-material
```
#### 5. Inicialize a documentação localmente:
```shell
npm run devDoc
```

### Rodando o Jogo 🎮

_EM CONTRUÇÃO..._

## 📝 Contribua com o projeto!

Para acessar a documentação do projeto Moonlighter, [Clique Aqui](https://sbd1.github.io/2025.1-Moonlighter/) ou clique no link disponível na descrição do repositório.

O projeto utiliza o protocolo **_Coventional Commits_** nas mensagens de commit, e portanto, deve seguir o seguinte padrão:

`tipo(escopo opcional): descrição breve`

Para controle de qualidade, o projeto utiliza a biblioteca **Husky** para executar comandos verificadores em diferentes fases de interação com o Git, como o pré-commit.

Para contribuir no projeto. Realize os seguintes passos:

#### 1. Certifique de instalar as tecnologias utilizadas no projeto:

- Node.Js | Versão 22+;
- PIP | Versão 24+;
- Python3 | Versão 3+;

#### 2. Clone o Repositório:

Selecione uma pasta de sua preferência e execute o seguinte comando para clonagem do repositório:

```shell
git clone https://github.com/SBD1/2025.1-Moonlighter.git
```

#### 3. Baixe as dependências do projeto:

Para contribuir no projeto com os commits, baixe as dependências do Husky para que as verificações possam acontecer:

```shell
npm install
```

#### 4. Suba o serviço de sua escolha

Acesse o tópico **"Executando o projeto"** para obter detalhes de como acessar os ambientes do projeto.


---
# 👩‍💻 Contribuidores:

<!-- Foto dos participantes do grupo -->
<div align="center">
  <table>
    <tr>
      <td align="center"><a href="https://github.com/arthurevg"><img style="border-radius: 50%;" src="https://github.com/arthurevg.png" width="100px;" alt=""/><br /><sub><b>Arthur Evangelista</b></sub></a><br /><a href="https://github.com/arthurevg" title="Rocketseat">231027032</a></td>
      <td align="center"><a href="https://github.com/DanielRogs"><img style="border-radius: 50%;" src="https://github.com/DanielRogs.png" width="100px;" alt=""/><br /><sub><b>Daniel Rodrigues</b></sub></a><br /><a href="https://github.com/DanielRogs" title="Rocketseat">211061583</a></td>
      <td align="center"><a href="https://github.com/IgorJustino"><img style="border-radius: 50%;" src="https://github.com/IgorJustino.png" width="100px;" alt=""/><br /><sub><b>Igor Justino</b></sub></a><br /><a href="https://github.com/arthur-suares" title="Rocketseat">211061897</a></td>
      </tr>
      <tr>
      <td align="center"><a href="https://github.com/jpaulohe4rt"><img style="border-radius: 50%;" src="https://github.com/jpaulohe4rt.png" width="100px;" alt=""/><br /><sub><b>João Paulo</b></sub></a><br /><a href="https://github.com/jpaulohe4rt" title="Rocketseat">190030755</a></td>
      <td align="center"><a href="https://github.com/Yanmatheus0812"><img style="border-radius: 50%;" src="https://github.com/Yanmatheus0812.png" width="100px;" alt=""/><br /><sub><b>Yan Matheus</b></sub></a><br /><a href="https://github.com/Yanmatheus0812" title="Rocketseat">231038303</a></td>
  </table>
</div>