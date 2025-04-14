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

## 🗃️ Estrutura do Projeto:

O projeto Moonlighter é dividido em três ambientes principais, organizados dentro da pasta `/apps`. Cada um deles cumpre um papel específico na arquitetura do sistema, mantendo o projeto modular e fácil de navegar:

- `apps/cli`: Contém o código da interface em terminal desenvolvida em Python, responsável pela interação do usuário com o sistema. Aqui é onde o jogo acontece — você executa comandos, visualiza ações e interage com o banco por meio de menus e prompts.
- `apps/sql`: Abriga toda a lógica relacionada ao banco de dados PostgreSQL, utilizando apenas SQL puro. Inclui a criação de tabelas, inserção de dados (seeds), views, triggers e controles de acesso. Esta pasta é o "coração lógico" do sistema.
- `apps/docs`: Ambiente de documentação criado com MkDocs, voltado para explicar o funcionamento do projeto, decisões de arquitetura, DER/MER, comandos SQL utilizados, e instruções de uso. É também o que será publicado no GitHub Pages para facilitar o acesso à documentação do time ou de avaliadores.

Essa organização facilita a separação entre lógica do jogo, estrutura de dados e documentação, permitindo que cada parte evolua de forma independente, mas integrada.

## 🚀 Executando o Projeto:

## 📝 Acesse a Documentação do Projeto!


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