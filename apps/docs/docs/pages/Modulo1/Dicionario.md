<span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.1</span>

# Dicionário de Dados

## O que é um Dicionário de Dados?

Um Dicionário de Dados é um documento ou repositório central que descreve detalhadamente os elementos de dados utilizados em um sistema ou banco de dados. Ele contém informações sobre cada campo, como nome, tipo de dado, tamanho, formato, restrições, padrão de preenchimento e significado. O objetivo principal do dicionário é padronizar e organizar os dados para que todos os envolvidos no projeto — analistas, desenvolvedores, testadores e usuários — tenham uma compreensão clara e consistente sobre o que cada dado representa e como deve ser tratado.

Além de auxiliar no desenvolvimento e manutenção de sistemas, o dicionário de dados também facilita a comunicação entre as equipes e a documentação do projeto, servindo como uma fonte de referência durante todas as fases do ciclo de vida do software. Ele pode abranger tanto dados estruturados (como tabelas de banco de dados relacionais) quanto dados utilizados em interfaces, relatórios e integrações com outros sistemas.

## Dicionário de Dados do Projeto Moonlighter

 **Nome da Tabela:** Masmorra <br/>
 **Descrição**: Armazena as informações das masmorras <br/>

 | Atributo          | Descrição                                | Tipo       | Limite | Restrições   |
 | ----------------- | ---------------------------------------- | ---------- | ------ | ------------ |
 | `NomeMasmorra`    | Nome da masmorra                         | Varchar    | 30     | PK           |
 | `Descricao`       | Descrição da masmorra                    | Varchar    | 60     |              |
 | `Nivel`           | Nível de dificuldade da masmorra         | Integer    |        |              |
 | `QtdAndar`        | Quantidade de andares da masmorra        | Integer    |        |              |
---

**Nome da Tabela:** Inst_Masmorra <br/>
**Descrição**: Armazena as informações das instâncias de masmorras <br/>
    
| Atributo            | Descrição                                   | Tipo     | Limite | Restrições |
| ------------------- | ------------------------------------------- | -------- | ------ | ---------- |
| `NomeMasmorra`      | Nome da masmorra                            | Varchar  | 30     | PK, FK     |
| `SeedMasmorra`      | Semente de geração da masmorra              | Integer  |        |            |
| `PosiçãoX_Jogador`  | Posição do jogador na coordenada X          | Integer  |        |            |
| `PosiçãoY_Jogador`  | Posição do jogador na coordenada Y          | Integer  |        |            |
---

 **Nome da Tabela:** Sala <br/>
 **Descrição**: Armazena as informações das salas das masmorras <br/>

 | Atributo          | Descrição                                | Tipo       | Limite | Restrições   |
 | ----------------- | ---------------------------------------- | ---------- | ------ | ------------ |
 | `SeedSala`        | Semente de geração da sala               | Integer    |        | PK           |
 | `PosicaoX`        | Posição da sala na coordenada X          | Integer    |        |              |
 | `PosicaoY`        | Posição da sala na coordenada Y          | Integer    |        |              |
 | `Categoria`       | Categoria da sala                        | Varchar    | 60     |              |
 | `Explorada`       | A sala já foi explorada?                 | Boolean    |        |              |
 | `NomeMasmorra`    | Nome da masmorra que se encontra a sala  | Varchar    | 30     | FK           |
---

**Nome da Tabela:** Sala_Inst_Masmorra <br/>
**Descrição**: Armazena as informações das salas que pertencem a uma instância de masmorra <br/>
| Atributo        | Descrição                       | Tipo     | Limite | Restrições |
| --------------- | ------------------------------- | -------- | ------ | ---------- |
| `SeedSala`      | Semente de geração da sala      | Integer  |        | PK         |
| `NomeMasmorra`  | Nome da masmorra                | Varchar  | 30     | FK         |
---

**Nome da Tabela:** Mapa <br/>
**Descrição**: Armazena as informações do mapa do jogo <br/>
| Atributo   | Descrição                           | Tipo     | Limite | Restrições |
| ---------- | ----------------------------------- | -------- | ------ | ---------- |
| `IdMapa`   | Número identificador do mapa        | Integer  |        | PK         |
| `Período`  | Período do dia do mapa              | Varchar  | 30     |            |
| `Dia`      | Data do dia que está o mapa         | Integer  |        |            |
---

**Nome da Tabela:** Masmorra_Mapa <br/>
**Descrição**: Armazena as informações das masmorras no mapa do jogo <br/>
| Atributo        | Descrição                                | Tipo     | Limite | Restrições |
| --------------- | ---------------------------------------- | -------- | ------ | ---------- |
| `NomeMasmorra`  | Nome da masmorra                         | Varchar  | 30     | FK         |
| `IdMapa`        | Número identificador do mapa             | Integer  |        | FK         |
| `Desbloqueado`  | A masmorra foi desbloqueada?             | Boolean  |        |            |
---

**Nome da Tabela:** Monstro <br/>
**Descrição**: Armazena as informações dos monstros  <br/>
| Atributo              | Descrição                                                 | Tipo     | Limite | Restrições |
| --------------------- | --------------------------------------------------------- | -------- | ------ | ---------- |
| `IdMonstro`           | Número identificador do monstro                           | Integer  |        | PK         |
| `Nome`                | Nome do monstro                                           | Varchar  | 30     |            |
| `Descrição`           | Descrição do monstro                                      | Varchar  | 60     |            |
| `Nível`               | Nível do monstro                                          | Integer  |        |            |
| `VidaMáxima`          | Vida máxima do monstro                                    | Integer  |        |            |
| `OuroDropado`         | Quantidade de ouro que o monstro deixa ao cair            | Float    |        |            |
| `DadoAtaque`          | Número do dado de ataque do monstro                       | Integer  |        |            |
| `ChanceCrítico`       | Chance de ataque crítico do monstro                       | Integer  |        |            |
| `Multiplicador`       | Multiplicador de ataque do monstro                        | Integer  |        |            |
| `MultiplicadorCrítico`| Multiplicador do ataque crítico do monstro                | Integer  |        |            |
| `Chefe`               | O monstro é um chefe?                                     | Boolean  |        |            |
| `NomeMasmorra`        | Nome da masmorra que o monstro está                       | Varchar  | 60     | FK         |
| `IdEfeito`            | Número identificador do efeito que o monstro está         | Integer  |        | FK         |
---

**Nome da Tabela:** Inst_Monstro <br/>
**Descrição**: Armazena as informações das instâncias dos monstros <br/>
| Atributo      | Descrição                                            | Tipo     | Limite | Restrições |
| ------------- | ---------------------------------------------------- | -------- | ------ | ---------- |
| `IdMonstro`   | Número identificador do monstro                      | Integer  |        | PK, FK     |
| `VidaAtual`   | Vida atual do monstro                                | Integer  |        |            |
| `Status`      | O monstro está vivo?                                 | Boolean  |        |            |
| `SeedSala`    | Semente de geração da sala em que o monstro está     | Integer  |        | FK         |
---

**Nome da Tabela:** Item <br/>
**Descrição**: Armazena as informações dos itens <br/>
| Atributo        | Descrição                                                  | Tipo     | Limite | Restrições |
| --------------- | ---------------------------------------------------------- | -------- | ------ | ---------- |
| `IdItem`        | Número de identificação do item                            | Integer  |        | PK         |
| `Nome`          | Nome do item                                               | Varchar  | 30     |            |
| `Descrição`     | Descrição do item                                          | Varchar  | 60     |            |
| `Tipo`          | Tipo do item                                               | Varchar  | 15     |            |
| `PreçoBase`     | Preço base que o item vale em sua venda                    | Integer  |        |            |
| `Raridade`      | Número de raridade do item                                 | Integer  |        |            |
| `StackMáximo`   | Quantidade máxima que o item pode ser empilhado            | Integer  |        |            |
| `IdEfeito`      | Número de identificador do efeito que o item pode dar      | Integer  |        | FK         |
---

**Nome da Tabela:** Arma <br/>
**Descrição**: Armazena as informações dos itens tipo arma <br/>
| Atributo              | Descrição                                    | Tipo     | Limite | Restrições |
| --------------------- | -------------------------------------------- | -------- | ------ | ---------- |
| `IdItem`              | Número de identificação do item              | Integer  |        | FK         |
| `DadoAtaque`          | Número do dado de ataque                     | Integer  |        |            |
| `ChanceCrítico`       | Número da chance de dano crítico             | Integer  |        |            |
| `Multiplicador`       | Número do multiplicador de dano              | Integer  |        |            |
| `MultiplicadorCrítico`| Número do multiplicador de dano crítico      | Integer  |        |            |
| `Alcance`             | Alcance da arma                              | Integer  |        |            |
| `TipoArma`            | Tipo de arma                                 | Varchar  | 15     |            |
---

**Nome da Tabela:** Armadura <br/>
**Descrição**: Armazena as informações dos itens tipo armadura <br/>
| Atributo           | Descrição                                                      | Tipo     | Limite | Restrições |
| ------------------ | -------------------------------------------------------------- | -------- | ------ | ---------- |
| `IdItem`           | Número de identificação do item                                | Integer  |        | FK         |
| `DadoDefesa`       | Número do dado de defesa                                       | Integer  |        |            |
| `DefesaPassiva`    | Número de defesa passiva da armadura                           | Integer  |        |            |
| `CríticoDefensivo` | Valor mínimo no dado para ganhar um bônus de defesa            | Integer  |        |            |
| `BonusDefesa`      | Valor atribuído à defesa passiva, aumentando a defesa total    | Integer  |        |            |
| `TipoArmadura`     | Tipo de armadura                                               | Varchar  | 15     |            |
---

**Nome da Tabela:** Poção <br/>
**Descrição**: Armazena as informações dos itens tipo poção <br/>
| Atributo         | Descrição                                      | Tipo     | Limite | Restrições |
| ---------------- | ---------------------------------------------- | -------- | ------ | ---------- |
| `IdItem`         | Número identificador do item usado             | Integer  |        | FK         |
| `DuraçãoTurnos`  | Duração de turnos de efeito da poção           | Integer  |        |            |
---

**Nome da Tabela:** Inst_Item <br/>
**Descrição**: Armazena as informações das instâncias dos itens <br/>
| Atributo       | Descrição                                                    | Tipo     | Limite | Restrições |
| -------------- | ------------------------------------------------------------ | -------- | ------ | ---------- |
| `IdItem`       | Número de identificação do item                              | Integer  |        | PK, FK     |
| `Quantidade`   | Quantidade da instância do item                              | Integer  |        |            |
| `IdMonstro`    | Número de identificação do monstro que está com o item       | Integer  |        | FK         |
| `IdInventário` | Número de identificação do inventário em que está o item     | Integer  |        | FK         |
| `IdLojaNPC`    | Número de identificação da loja do NPC em que está o item    | Integer  |        | FK         |
| `SeedSala`     | Semente de geração da sala que contém o item                 | Integer  |        | FK         |
| `NickName`     | Nome do jogador que contém o item                            | Integer  |        | FK         |
---

**Nome da Tabela:** Monstro_Item <br/>
**Descrição**: Armazena as informações dos itens dos monstros <br/>
| Atributo     | Descrição                                               | Tipo     | Limite | Restrições |
| ------------ | ------------------------------------------------------- | -------- | ------ | ---------- |
| `IdMonstro`  | Número identificador do monstro                         | Integer  |        | FK         |
| `IdItem`     | Número identificador do item                            | Integer  |        | FK         |
| `ChanceDrop` | Número da chance do monstro deixar cair um item         | Integer  |        |            |
| `QtdMinima`  | Quantidade mínima de itens que o monstro deixa cair     | Integer  |        |            |
| `QtdMaxima`  | Quantidade máxima de itens que o monstro deixa cair     | Integer  |        |            |
---

**Nome da Tabela:** Efeito <br/>
**Descrição**: Armazena as informações dos efeitos dos itens <br/>
| Atributo         | Descrição                                            | Tipo     | Limite | Restrições |
| ---------------- | ---------------------------------------------------- | -------- | ------ | ---------- |
| `IdEfeito`       | Número de identificação do efeito                    | Integer  |        | PK         |
| `Nome`           | Nome do efeito                                       | Varchar  | 30     |            |
| `Descrição`      | Descrição do efeito                                  | Varchar  | 60     |            |
| `Tipo`           | Tipo do efeito                                       | Varchar  | 15     |            |
| `Valor`          | Quantificação de impacto do efeito                   | Integer  |        |            |
| `DuraçãoTurnos`  | Duração de turnos do efeito                          | Integer  |        |            |
---

**Nome da Tabela:** Receita <br/>
**Descrição**: Armazena as informações das receitas para se fabricar um item <br/>
| Atributo    | Descrição                                                      | Tipo     | Limite | Restrições |
| ----------- | -------------------------------------------------------------- | -------- | ------ | ---------- |
| `IdItem`    | Número identificador do item usado                             | Integer  |        | FK         |
| `IdItem`    | Número identificador do item gerado                            | Integer  |        | FK         |
| `Quantidade`| Quantidade de itens usados necessários para fabricar           | Integer  |        |            |
---

**Nome da Tabela:** Jogador <br/>
**Descrição**: Armazena as informações do jogador <br/>
| Atributo   | Descrição                                             | Tipo     | Limite | Restrições |
| ---------- | ----------------------------------------------------- | -------- | ------ | ---------- |
| `Nickname` | Nome único do jogador                                 | Varchar  | 60     | PK         |
| `MaxHP`    | Número máximo de vida do jogador                      | Integer  |        |            |
| `AtualHP`  | Vida atual do jogador                                 | Integer  |        |            |
| `Ouro`     | Ouro do jogador                                       | Float    |        |            |
| `IdEfeito` | Número de identificação do efeito aplicado no jogador | Integer  |        | FK         |
---

**Nome da Tabela:** LojaJogador <br/>
**Descrição**: Armazena as informações da loja do jogador <br/>
| Atributo           | Descrição                                                         | Tipo     | Limite | Restrições |
| ------------------ | ----------------------------------------------------------------- | -------- | ------ | ---------- |
| `NickName`         | Nome único do jogador                                             | Varchar  | 60     | PK, FK     |
| `Nível`            | Nível da loja do jogador                                          | Integer  |        |            |
| `ExposiçãoMáxima`  | Número máximo de itens que podem ser expostos na loja do jogador  | Integer  |        |            |
| `ExposiçãoUsada`   | Número de itens atualmente expostos na loja do jogador            | Integer  |        |            |
| `IdMapa`           | Número de identificação do mapa do mundo                          | Integer  |        | FK         |
---

**Nome da Tabela:** Inventário <br/>
**Descrição**: Armazena as informações dos inventários <br/>
| Atributo       | Descrição                                             | Tipo     | Limite | Restrições |
| -------------- | ----------------------------------------------------- | -------- | ------ | ---------- |
| `IdInventário` | Número de identificação do inventário                 | Integer  |        | PK         |
| `Nome`         | Nome do inventário                                    | Varchar  | 30     |            |
| `SlotMáximo`   | Quantidade máxima de armazenamento de itens           | Integer  |        |            |
---

**Nome da Tabela:** Inst_Inventario <br/>
**Descrição**: Armazena as informações das instâncias de inventário <br/>
| Atributo       | Descrição                                             | Tipo     | Limite | Restrições |
| -------------- | ----------------------------------------------------- | -------- | ------ | ---------- |
| `IdInventário` | Número de identificação do inventário                 | Integer  |        | PK, FK     |
| `SlotOcupado`  | Quantidade de lugares do inventário ocupados          | Integer  |        |            |
| `Nickname`     | Nome do jogador                                       | Varchar  | 60     | FK         |
---

**Nome da Tabela:** NPC <br/>
**Descrição**: Armazena as informações dos NPCs  <br/>
| Atributo    | Descrição                                         | Tipo     | Limite | Restrições |
| ----------- | ------------------------------------------------- | -------- | ------ | ---------- |
| `IdNPC`     | Número de identificação do NPC                    | Integer  |        | PK         |
| `Nome`      | Nome do NPC                                       | Varchar  | 30     |            |
| `TipoNPC`   | Tipo de NPC                                       | Varchar  | 30     |            |
| `Descrição` | Descrição do NPC                                  | Varchar  | 60     |            |
| `Ativo`     | O NPC está interagindo com o jogador?             | Boolean  |        |            |
---

**Nome da Tabela:** LojaNPC <br/>
**Descrição**: Armazena as informações da loja do NPC <br/>
| Atributo     | Descrição                                           | Tipo     | Limite | Restrições |
| ------------ | --------------------------------------------------- | -------- | ------ | ---------- |
| `IdLojaNPC`  | Número de identificação da loja do NPC              | Integer  |        | PK         |
| `Nome`       | Nome da loja do NPC                                 | Varchar  | 30     |            |
| `TipoLoja`   | Tipo da loja do NPC                                 | Varchar  | 30     |            |
| `Descrição`  | Descrição da loja do NPC                            | Varchar  | 120    |            |
| `Status`     | Status da loja do NPC                               | Varchar  | 30     |            |
| `IdNPC`      | Número de identificação do NPC da loja              | Integer  |        | FK         |
| `IdMapa`     | Número de identificação do mapa do mundo            | Integer  |        | FK         |
---

**Nome da Tabela:** Forjaria <br/>
**Descrição**: Armazena as informações da loja do NPC tipo forjaria <br/>
| Atributo     | Descrição                                  | Tipo     | Limite | Restrições |
| ------------ | ------------------------------------------ | -------- | ------ | ---------- |
| `IdLojaNPC`  | Número de identificação da loja do NPC     | Integer  |        | FK         |
---

**Nome da Tabela:** Varejo <br/>
**Descrição**: Armazena as informações da loja do NPC tipo varejo <br/>
| Atributo      | Descrição                                         | Tipo     | Limite | Restrições |
| ------------- | ------------------------------------------------- | -------- | ------ | ---------- |
| `IdLojaNPC`   | Número de identificação da loja do NPC            | Integer  |        | FK         |
| `MargemLucro` | Margem de lucro dos itens do NPC                  | Float    |        |            |
---

**Nome da Tabela:** Banco <br/>
**Descrição**: Armazena as informações da loja do NPC tipo banco <br/>
| Atributo        | Descrição                                               | Tipo     | Limite | Restrições |
| --------------- | ------------------------------------------------------- | -------- | ------ | ---------- |
| `IdLojaNPC`     | Número de identificação da loja do NPC                  | Integer  |        | FK         |
| `ValorEntrada`  | Valor do ouro de entrada depositado pelo jogador        | Float    |        |            |
| `ValorAtual`    | Valor atual do ouro com rendimento do jogador           | Float    |        |            |
---

**Nome da Tabela:** Diálogo <br/>
**Descrição**: Armazena as informações dos diálogos <br/>
| Atributo      | Descrição                                      | Tipo     | Limite | Restrições |
| ------------- | ---------------------------------------------- | -------- | ------ | ---------- |
| `IdDiálogo`   | Número de identificação do diálogo             | Integer  |        | PK         |
| `Conteúdo`    | Conteúdo do diálogo                            | Varchar  | 300    |            |
| `Ordem`       | Ordem do diálogo                               | Integer  |        |            |
| `Tipo`        | Tipo de diálogo                                | Varchar  | 60     |            |
| `IdDialogo`   | Número de identificação do diálogo             | Integer  |        | FK         |
---

**Nome da Tabela:** Diálogo_NPC <br/>
**Descrição**: Armazena as informações dos diálogos com NPCs <br/>
| Atributo     | Descrição                                | Tipo     | Limite | Restrições |
| ------------ | ---------------------------------------- | -------- | ------ | ---------- |
| `IdDiálogo`  | Número de identificação do diálogo       | Integer  |        | FK         |
| `IdNPC`      | Número de identificação do NPC           | Integer  |        | FK         |
---
--

# Bibliografia

> <p><small>CONTENT STUDIO. O que é um dicionário de dados? Disponível em: <a href="https://www.purestorage.com/br/knowledge/what-is-a-data-dictionary.html">https://www.purestorage.com/br/knowledge/what-is-a-data-dictionary.html</a>. Acesso em: 30 abr. 2025.</small></p>

‌

# Versão:

| Data       | Versão | Autor(es)        | Mudanças                                           |
| ---------- | ------ | ---------------- | -------------------------------------------------- |
| 30/04/2024 | `1.0`  | Daniel Rodrigues | Adição do Tópico "O que é um dicionário de dados?" |
| 01/05/2024 | `1.1`  | Yan Matheus      | Adição das tabelas do dicionário de dados          |
