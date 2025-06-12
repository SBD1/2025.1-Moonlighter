# Moonlight Terminal Game

<div align="center">
  <img src="assets/Moonlighter_Icon.png" alt="Capa Moonlighter" width="50%">
  <p><b>Figura 1:</b> Capa oficial do Jogo Moonlighter</p>
</div>

O **Moonlight Terminal Game** é inspirado no jogo indie de ação e aventura **Moonlighter**, adaptado para ser executado diretamente no terminal. Nosso objetivo é recriar a essência do jogo original, com foco em mecânicas de exploração, gerenciamento e combate, utilizando tecnologias modernas e boas práticas de desenvolvimento.

---

## 🎮 Sobre o Projeto

No **Moonlighter**, você assume o papel de Will, um comerciante que vive uma vida dupla: durante o dia, ele gerencia sua loja, e à noite, explora masmorras em busca de tesouros e recursos raros. Nosso projeto adapta essa experiência para o terminal, com funcionalidades como:

- **Exploração de masmorras**: Navegue pelas masmorras, enfrentando desafios e coletando itens valiosos.
- **Combate contra monstros**: Enfrente uma variedade de inimigos com diferentes habilidades e comportamentos.
- **Sistema de armas e armaduras**: Equipe-se com armas e armaduras que podem ter possuir diferentes efeitos.
- **Efeitos e habilidades especiais**: Utilize habilidades e efeitos únicos para derrotar inimigos e superar obstáculos.
- **Gerenciamento de inventário**: Organize os itens coletados durante as explorações e decida o que vender ou guardar.
- **Gestão de loja**: Venda itens para clientes fictícios, ajuste preços e maximize seus lucros.
- **Progressão do personagem**: Melhore as habilidades de Will e desbloqueie novos equipamentos e funcionalidades.


A aplicação é desenvolvida em **Python**, com a lógica de dados estruturada em **PostgreSQL**, utilizando SQL puro para modelagem, triggers, views e controle de acesso.

---

# 👩‍💻 Contribuidores:

<div style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 20px;
  margin-top: 30px;
">

<a href="https://github.com/arthurevg" style="text-decoration: none; color: inherit; box-shadow: 0 4px 10px 0 rgba(0, 0, 0, 0.2)">
  <div style="text-align: center; background: #f5f5f5; padding: 20px;">
    <img src="https://github.com/arthurevg.png" style="width: 120px; height: 120px; object-fit: cover; border-radius: 50%; border: 3px solid #149d73;">
    <h5 style="margin: 20px 0px 0px 0px; padding: 0px; color: #149d73">231027032</h5>
    <p style="color: black; margin: 0px 0px 20px 0px; padding: 0px">Arthur Evangelista</p>
  </div>
</a>

<a href="https://github.com/DanielRogs" style="text-decoration: none; color: inherit; box-shadow: 0 4px 10px 0 rgba(0, 0, 0, 0.2)">
  <div style="text-align: center; background: #f5f5f5; padding: 20px;">
    <img src="https://github.com/DanielRogs.png" style="width: 120px; height: 120px; object-fit: cover; border-radius: 50%; border: 3px solid #149d73;">
    <h5 style="margin: 20px 0px 0px 0px; padding: 0px; color: #149d73">211061583</h5>
    <p style="color: black; margin: 0px 0px 20px 0px; padding: 0px">Daniel Rodrigues</p>
  </div>
</a>

<a href="https://github.com/IgorJustino" style="text-decoration: none; color: inherit; box-shadow: 0 4px 10px 0 rgba(0, 0, 0, 0.2)">
  <div style="text-align: center; background: #f5f5f5; padding: 20px;">
    <img src="https://github.com/IgorJustino.png" style="width: 120px; height: 120px; object-fit: cover; border-radius: 50%; border: 3px solid #149d73;">
    <h5 style="margin: 20px 0px 0px 0px; padding: 0px; color: #149d73">211061897</h5>
    <p style="color: black; margin: 0px 0px 20px 0px; padding: 0px">Igor Justino</p>
  </div>
</a>

<a href="https://github.com/jpaulohe4rt" style="text-decoration: none; color: inherit; box-shadow: 0 4px 10px 0 rgba(0, 0, 0, 0.2)">
  <div style="text-align: center; background: #f5f5f5; padding: 20px;">
    <img src="https://github.com/jpaulohe4rt.png" style="width: 120px; height: 120px; object-fit: cover; border-radius: 50%; border: 3px solid #149d73;">
    <h5 style="margin: 20px 0px 0px 0px; padding: 0px; color: #149d73">190030755</h5>
    <p style="color: black; margin: 0px 0px 20px 0px; padding: 0px">João Paulo</p>
  </div>
</a>

<a href="https://github.com/Yanmatheus0812" style="text-decoration: none; color: inherit; box-shadow: 0 4px 10px 0 rgba(0, 0, 0, 0.2)">
  <div style="text-align: center; background: #f5f5f5; padding: 20px;">
    <img src="https://github.com/Yanmatheus0812.png" style="width: 120px; height: 120px; object-fit: cover; border-radius: 50%; border: 3px solid #149d73;">
    <h5 style="margin: 20px 0px 0px 0px; padding: 0px; color: #149d73">231038303</h5>
    <p style="color: black; margin: 0px 0px 20px 0px; padding: 0px">Yan Matheus</p>
  </div>
</a>
</div>


## 🗃️ Estrutura do Projeto

O projeto está organizado em três ambientes principais:

- **`apps/cli`**: Código da interface em terminal (Python), responsável pela interação do usuário com o sistema.
- **`apps/sql`**: Lógica do banco de dados (PostgreSQL), incluindo tabelas, seeds, views, triggers e controles de acesso.
- **`apps/docs`**: Documentação do projeto, criada com MkDocs, explicando o funcionamento, decisões de arquitetura, DER/MER e instruções de uso.

Essa estrutura modular facilita o desenvolvimento e a manutenção do projeto.

---

## 🚀 Como Executar

O projeto ainda está em fase inicial e o código não foi implementado nesta primeira entrega. Assim que o desenvolvimento começar, as instruções para execução serão adicionadas aqui.

Fique atento às próximas atualizações!



## Histórico de Versão

| Versão | Data          | Descrição                          | Autor(es)     | 
| ------ | ------------- | ---------------------------------- | ------------- |
| `1.0`  |  30/04/2025 |  Criação da página 'Home', contendo informações sobre o projeto | [Arthur](https://github.com/arthurevg)  |

