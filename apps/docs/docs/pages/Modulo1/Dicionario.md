<span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 2.1</span>

# Dicionário de Dados

## O que é um Dicionário de Dados?

Um Dicionário de Dados é um documento ou repositório central que descreve detalhadamente os elementos de dados utilizados em um sistema ou banco de dados. Ele contém informações sobre cada campo, como nome, tipo de dado, tamanho, formato, restrições, padrão de preenchimento e significado. O objetivo principal do dicionário é padronizar e organizar os dados para que todos os envolvidos no projeto — analistas, desenvolvedores, testadores e usuários — tenham uma compreensão clara e consistente sobre o que cada dado representa e como deve ser tratado.

Além de auxiliar no desenvolvimento e manutenção de sistemas, o dicionário de dados também facilita a comunicação entre as equipes e a documentação do projeto, servindo como uma fonte de referência durante todas as fases do ciclo de vida do software. Ele pode abranger tanto dados estruturados (como tabelas de banco de dados relacionais) quanto dados utilizados em interfaces, relatórios e integrações com outros sistemas.

## Dicionário de Dados do Projeto Moonlighter

!!! Warning "Atenção!"
    O conteúdo deste tópico **poderá sofrer alterações** ao longo da Disciplina de Sistema de Banco de Dados 1. Portanto, as tabelas serão organizadas iniciando pela versão mais recente e finalizando com a versão mais antiga.

O dicionário de dados do Projeto Moonlighter apresenta a descrição detalhada dos atributos utilizados nas tabelas do Modelo Relacional. Ele serve como um guia técnico que traduz, de forma objetiva e organizada, as informações presentes na modelagem conceitual e lógica do banco de dados, facilitando o entendimento e a padronização dos dados por parte da equipe de desenvolvimento, análise e demais envolvidos no projeto.

Cada tabela está documentada com seus respectivos campos, tipos de dados, restrições e limites, garantindo transparência na estruturação das informações e contribuindo para a manutenção da integridade e consistência do sistema.

<center>
  <span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Dicionário de Dados | Versão 2.1</span>
</center>

??? info "Tabela LOCAL | 2.1v"
    **Nome da Tabela:** Local <br/>
    **Descrição**: Armazena todos os locais disponíveis para locomoção do jogador  <br/>

    | Atributo    | Descrição                            | Tipo     | Limite | Restrições       |
    | ----------- | ------------------------------------ | -------- | ------ | ---------------- |
    | `nomeLocal` | Nome do Local disponível para acesso | Varchar  | 60     | `PK`             |
    | `descricao` | Descrição Narrada de como é o local  | Varchar  | 200    | `NOT NULL`       |
    | `tipoLocal` | Tipo de Local para indentificação às tabelas especializadas `Masmorra` ou `Estabelecimento` ou Nenhum | Varchar  | 20     | `NOT NULL`       |
    | `acesso`    | Referência à tabela `Local` para indicar se o local atual está dentro de outro local  | Varchar  | 60     | `FK`             |

??? info "Tabela MASMORRA | 2.1v"
    **Nome da Tabela:** Masmorra <br/>
    **Descrição**: Armazena configurações de Locais classificadas como Masmorras <br/>

    | Atributo           | Descrição                            | Tipo     | Limite | Restrições       |
    | ------------------ | ------------------------------------ | -------- | ------ | ---------------- |
    | `nomeLocal`        | Referência à tabela `Local`, para indicar qual local é classificado como masmorra | Varchar  | 60     | `PK`, `FK`         |
    | `nivelDesbloqueio` | Indica o nível necessário de Mundo para desbloqueiar a masmorra                     | SmallInt  |        | `NOT NULL`       |
    | `dificuldade`      | Indica a dificuldade da masmorra          | Varchar   | 7      | `NOT NULL`       |

??? info "Tabela ESTABELECIMENTO | 2.1v"
    **Nome da Tabela:** Estabelecimento <br/>
    **Descrição**: Armazena Locais que são classificados como Estabelecimento <br/>

    | Atributo    | Descrição                            | Tipo     | Limite | Restrições       |
    | ----------- | ------------------------------------ | -------- | ------ | ---------------- |
    | `nomeLocal` | Referência à tabela `Local`, para indicar qual local é classificado como estabelecimento       | Varchar  | 60     | `PK`, `PK`         |

??? info "Tabela EFEITO | 2.1v"
    **Nome da Tabela:** Efeito <br/>
    **Descrição**: Armazena as informações dos efeitos dos itens ou jogador <br/>

    | Atributo         | Descrição                                            | Tipo     | Limite | Restrições      |
    | ---------------- | ---------------------------------------------------- | -------- | ------ | --------------- |
    | `idEfeito`       | Número de identificação do efeito                    | Integer  |        | `PK`, `IDENTITY`|
    | `nome`           | Nome do efeito                                       | Varchar  | 30     | `NOT NULL`      |
    | `descrição`      | Descrição do efeito                                  | Varchar  | 100    | `NOT NULL`      |
    | `tipo`           | Tipo do efeito                                       | Varchar  | 15     | `NOT NULL`      |
    | `valor`          | Quantificação de impacto do efeito                   | SmallInt |        | `NOT NULL`      |
    | `duraçãoTurnos`  | Duração de turnos do efeito                          | SmallInt |        |       |

??? info "Tabela JOGADOR | 2.1v"
    **Nome da Tabela:** Jogador <br/>
    **Descrição**: Armazena as informações do jogador <br/>

    | Atributo   | Descrição                                                | Tipo     | Limite | Restrições |
    | ---------- | -------------------------------------------------------- | -------- | ------ | ---------- |
    | `nickname`         | Indica o nome do jogador                                                          | Varchar  | 60     | `PK`       |
    | `maxHP`            | Indica o número máximo de vida disponível do jogador                              | SmallInt |        | `NOT NULL` |
    | `atualHP`          | Indica a vida atual do jogador                                                    | SmallInt |        | `NOT NULL` |
    | `ouro`             | Indica a quantidade de Ouro que o jogador possui                                  | Integere |        | `NOT NULL` |
    | `posicaoX_Jogador` | Indica a posição de linha de uma matriz quando estiver dentro da masmorra         | SmallInt |        | `NOT NULL` |
    | `posicaoY_Jogador` | Indica a posição de coluna de uma matriz quando estiver dentro da masmorra        | SmallInt |        | `NOT NULL` |
    | `nomeLocal`        | Referência à Tabela `Local` para indicar onde o jogador está
    | `idEfeito` | Referência à Tabela `Efeito`, identificando se o jogador está sob algum efeito | Integer  |        | `FK`       |

??? info "Tabela MUNDO | 2.1v"
    **Nome da Tabela:** Mundo <br/>
    **Descrição**: Armazena os dados do Mundo em que o jogador está <br/>

    | Atributo         | Descrição                                             | Tipo     | Limite | Restrições     |
    | ---------------- | ----------------------------------------------------- | -------- | ------ | -------------- |
    | `seedMundo`      | Registra a semente de geração do mundo                | Varchar  | 30     | `PK`           |
    | `nickname`       | Referência à tabela `Jogador` para indicar à qual jogador o mundo pertence                | Varchar  | 60      | `FK`, `NOT NULL`      |
    | `periodo`        | Indica o período que o mundo se encontra: Manhã, Tarde, Noite                             | Varchar  | 8       | `NOT NULL`            |
    | `dia`            | Indica a quantidade de dias passados                  | SmallInt |        | `NOT NULL`           |
    | `nivelMundo`     | Indica o nível do mundo para desbloqueio das masmorras| SmallInt |        | `NOT NULL`           |

??? info "Tabela INST_MASMORRA | 2.1v"
    **Nome da Tabela:** Inst_masmorra <br/>
    **Descrição**: Guarda as instâncias de masmorras geradas proceduralmente, após o jogador entrar em uma masmorra <br/>

    | Atributo         | Descrição                                              | Tipo     | Limite | Restrições     |
    | ---------------- | ------------------------------------------------------ | -------- | ------ | -------------- |
    | `seedMundo`      | Referência à tabela `Mundo` para indicar à qual mundo essa instância pertence               | Varchar  | 30     | `PK`, `FK`          |
    | `seedMasmorra`   | Registra a semente de geração da instância de masmorra | Varchar  | 30     | `PK`           |
    | `nomeLocal`      | Referência à tabela `Masmorra` para indicar à qual tipo de masmorra a instância pertence    | Varchar  | 60     | `FK`, `NOT NULL`    |
    | `ativo`          | Indica se a masmorra está sendo explorada pelo jogador ou não                               | Boolean  |        | `NOT NULL`          |

??? info "Tabela SALA | 2.1v"
    **Nome da Tabela:** Sala <br/>
    **Descrição**: Armazena os dados de uma sala, disponível para acesso ao jogador através das instâncias de masmorras <br/>
    
    | Atributo         | Descrição                                             | Tipo     | Limite | Restrições         |
    | ---------------- | ----------------------------------------------------- | -------- | ------ | ------------------ |
    | `seedSala`       | Registra a semente de geração da Sala                 | Varchar  | 30     | `PK`               |
    | `posicaoX`       | Indica em qual posição de linha em uma matriz, a sala está na instância de masmorra            | SmallInt  |        | `NOT NULL`          |
    | `posicaoY`       | Indica em qual posição de coluna em uma matriz, a sala está na instância de masmorra           | SmallInt  |        | `NOT NULL`          |
    | `categoria`      | Indica se a sala é de combate, loot ou do chefe       | Varchar  | 60     | `NOT NULL`          |
    | `seedMundo`      | Referência à Tabela `Inst_Masmorra` para indicar à qual instância de masmorra a sala pertence  | Varchar   | 30     | `FK`, `NOT NULL`    |
    | `seedMasmorra`   | Referência à Tabela `Inst_Masmorra` para indicar à qual instância de masmorra a sala pertence  | Varchar   | 30     | `FK`, `NOT NULL`    |

??? info "Tabela MONSTRO | 2.1v"
    **Nome da Tabela:** Monstro <br/>
    **Descrição**: Lista o _Bestiário_ (Lista de Monstros) disponível no jogo  <br/>

    | Atributo              | Descrição                                                                               | Tipo     | Limite | Restrições       |
    | --------------------- | --------------------------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `idMonstro`           | Número identificador do monstro                                                         | Integer  |        | `PK`, `IDENTITY` |
    | `nome`                | Indica o nome do monstro                                                                | Varchar  | 30     | `NOT NULL`       |
    | `descrição`           | Descreve o monstro                                                                      | Varchar  | 100    | `NOT NULL`       |
    | `nível`               | Indica o nível do monstro                                                               | SmallInt |        | `NOT NULL`       |
    | `vidaMáxima`          | Indica a vida máxima do monstro                                                         | SmallInt |        | `NOT NULL`       |
    | `ouroDropado`         | Indica a quantidade de ouro que o monstro deixa ao cair                                 | SmallInt |        | `NOT NULL`       |
    | `dadoAtaque`          | Indica o número do dado de ataque do monstro                                            | Varchar  | 4      | `NOT NULL`       |
    | `chanceCrítico`       | Indica a chance de ataque crítico do monstro                                            | Real     |        | `NOT NULL`       |
    | `multiplicador`       | Indica o multiplicador de ataque do monstro                                             | SmallInt |        | `NOT NULL`       |
    | `multiplicadorCrítico`| Indica o multiplicador do ataque crítico do monstro                                     | SmallInt |        | `NOT NULL`       |
    | `chefe`               | O monstro é um chefe?                                                                   | Boolean  |        | `NOT NULL`       |
    | `nomeLocal`           | Referência à tabela `Masmorra` para indicar à qual tipo de masmorra o monstro pertence  | Varchar  | 60     | `FK`, `NOT NULL` |
    | `idEfeito`            | Referência à Tabela `Efeito` para indicar se o monstro possui algum efeito              | Integer  |        | `FK`             |

??? info "Tabela INST_MONSTRO | 2.1v"
    **Nome da Tabela:** Inst_Monstro <br/>
    **Descrição**: Armazena as informações das instâncias dos monstros <br/>

    | Atributo      | Descrição                                            | Tipo     | Limite | Restrições       |
    | ------------- | ---------------------------------------------------- | -------- | ------ | ---------------- |
    | `seedMundo`   | Referência à Tabela `Mundo` para indicar à qual mundo a instância de monstro pertence       | Varchar  | 30     | `PK`, `FK`         |
    | `idMonstro`   | Referência à Tabela `Monstro` para indicar qual é o monstro da instância                    | Integer  |        | `PK`, `FK`         |
    | `vidaAtual`   | Indica a vida atual do monstro                       | SmallInt |        | `NOT NULL`       |
    | `status`      | O monstro está vivo?                                 | Boolean  |        | `NOT NULL`       |
    | `seedSala`    | Referência à Tabela `Sala` para indicar onde a instância de monstro está localizado         | Varchar  | 30     | `FK`, `NOT NULL`   |

??? info "Tabela ITEM | 2.1v"
    **Nome da Tabela:** Item <br/>
    **Descrição**: Lista todos os itens disponíveis no jogo <br/>

    | Atributo        | Descrição                                                               | Tipo     | Limite | Restrições       |
    | --------------- | ----------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `idItem`        | Número de identificação do item                                         | Integer  |        | `PK`, `IDENTITY` |
    | `nome`          | Indica o nome do item                                                   | Varchar  | 80     | `NOT NULL`       |
    | `descrição`     | Descreve o item                                                         | Varchar  | 500    | `NOT NULL`       |
    | `tipo`          | Tipo do item para indentificação às tabelas especializadas `Arma`, `Armadura`, `Pocao` ou Nenhum               | Varchar  | 15     | `NOT NULL`       |
    | `preçoBase`     | Indica o preço base que o item vale em sua venda                        | Interger |        | `NOT NULL`       |
    | `cultura`       | Indica à qual cultura de masmorra o item pertence                       | Varchar  | 10     | `NOT NULL`       |
    | `stackMaximo`   | Indica quantos itens do mesmo tipo eu posso empilhar no mesmo slot      | SmallInt |        | `NOT NULL`       |
    | `idEfeito`      | Referência à Tabela `Efeito` para indicar que efeito o item pode aplicar| Integer  |        | `FK`             |

??? info "Tabela ARMA | 2.1v"
    **Nome da Tabela:** Arma <br/>
    **Descrição**: Armazena as informações dos itens classificadas como arma <br/>

    | Atributo              | Descrição                                    | Tipo     | Limite | Restrições       |
    | --------------------- | -------------------------------------------- | -------- | ------ | ---------------- |
    | `idItem`              | Referência à Tabela `Item` para indicar qual item é classificado como Arma          | Integer  |        | `PK`, `FK`       |
    | `dadoAtaque`          | Número do dado de ataque                     | Varchar  | 4      | `NOT NULL`       |
    | `chanceCrítico`       | Número da chance de dano crítico             | Real     |        | `NOT NULL`       | 
    | `multiplicador`       | Número do multiplicador de dano              | SmallInt |        | `NOT NULL`       |
    | `multiplicadorCrítico`| Número do multiplicador de dano crítico      | SmallInt |        | `NOT NULL`       |
    | `tipoArma`            | Tipo de arma                                 | Varchar  | 15     | `NOT NULL`       |

??? info "Tabela ARMADURA | 2.1v"
    **Nome da Tabela:** Armadura <br/>
    **Descrição**: Armazena as informações dos itens classificadas como armadura <br/>

    | Atributo           | Descrição                                                      | Tipo     | Limite | Restrições       |
    | ------------------ | -------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `idItem`           | Referência à Tabela `Item` para indicar qual item é classificado como Armadura                        | Integer  |        | `PK`, `FK`       |
    | `dadoDefesa`       | Número do dado de defesa                                       | Varchar  | 3      | `NOT NULL`       |
    | `defesaPassiva`    | Número de defesa passiva da armadura                           | SmallInt |        | `NOT NULL`       |
    | `críticoDefensivo` | Valor mínimo no dado para ganhar um bônus de defesa            | SmallInt |        | `NOT NULL`       |
    | `bonusDefesa`      | Valor atribuído à defesa passiva, aumentando a defesa total    | SmallInt |        | `NOT NULL`       |
    | `tipoArmadura`     | Tipo de armadura                                               | Varchar  | 15     | `NOT NULL`       |

??? info "Tabela POCAO | 2.1v"
    **Nome da Tabela:** Pocao <br/>
    **Descrição**: Armazena as informações dos itens classificadas como poção <br/>

    | Atributo         | Descrição                                      | Tipo     | Limite | Restrições       |
    | ---------------- | ---------------------------------------------- | -------- | ------ | ---------------- |
    | `idItem`         | Referência à Tabela `Item` para indicar qual item é classificado como Pocao           | Integer  |        | `PK`, `FK`       |
    | `duraçãoTurnos`  | Duração de turnos de efeito da poção           | SmallInt |        | `NOT NULL`       |

??? info "Tabela MONSTRO_ITEM | 2.1v"
    **Nome da Tabela:** Monstro_Item <br/>
    **Descrição**: Armazena as informações de Itens que Monstros podem deixar cair <br/>

    | Atributo     | Descrição                                                                                  | Tipo     | Limite | Restrições       |
    | ------------ | ------------------------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `idMonstro`  | Referência à Tabela `Monstro` para indicar qual é o monstro que irá deixar o item cair     | Integer  |        | `FK`, `NOT NULL` |
    | `idItem`     | Referência à Tabela `Item` para indicar qual o item o monstro irá deixar cair              | Integer  |        | `FK`, `NOT NULL` |
    | `chanceDrop` | Indica a chance do monstro em deixar cair o item                                           | Real     |        | `NOT NULL`       |
    | `qtdMinima`  | Quantidade mínima em _stack_ do "IdItem" que o monstro "IdMonstro" precisa deixar cair     | SmallInt |        | `NOT NULL`       |
    | `qtdMaxima`  | Quantidade máxima em _stack_ do "IdItem" que o monstro "IdMonstro" pode deixar cair        | SmallInt |        | `NOT NULL`       |

??? info "Tabela RECEITA | 2.1v"
    **Nome da Tabela:** Receita <br/>
    **Descrição**: Armazena as informações das receitas para se fabricar um item <br/>

    | Atributo            | Descrição                                                               | Tipo     | Limite | Restrições       |
    | ------------------- | ----------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `idItemFabricado`   | Referência à Tabela `Item` para identificar o item Fabricado            | Integer  |        | `FK`, `NOT NULL` |
    | `idItemFabricador`  | Referência à Tabela `Item` para identificar o item Fabricador           | Integer  |        | `FK`, `NOT NULL` |
    | `quantidade`        | Quantidade de itens em _stack_ necessários para fabricar o item         | SmallInt |        | `NOT NULL`       |

??? info "Tabela LOJA_JOGADOR | 2.1v"
    **Nome da Tabela:** Loja_Jogador <br/>
    **Descrição**: Armazena as informações das lojas de cada jogador <br/>

    | Atributo          | Descrição                                                       | Tipo     | Limite | Restrições       |
    | ----------------- | --------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `seedMundo`       | Referência à Tabela `Mundo` para indicar o mundo à qual a loja do jogador pertence  | Integer  |        | `PK`, `FK` |
    | `nomeLocal`       | Referência à Tabela `Estabelecimento` para indicar à qual tipo de estabelecimento, a loja do jogador pertence | Integer  |        | `FK`, `NOT NULL` |
    | `nivel`           | Indica o nível da loja do jogador                               | SmallInt |        | `NOT NULL`       |
    | `exposicaoMaxima` | Indica o máximo de itens que o jogador pode expor para venda em sua loja   | SmallInt |        | `NOT NULL`       |
    | `exposicaoUsada`  | Indica o espaço usado de exposição de itens para venda na loja do jogador  | SmallInt |        | `NOT NULL`       |

??? info "Tabela INVENTARIO | 2.1v"
    **Nome da Tabela:** Inventário <br/>
    **Descrição**: Armazena as informações de tipos de inventários existentes no jogo <br/>

    | Atributo       | Descrição                                             | Tipo     | Limite | Restrições       |
    | -------------- | ----------------------------------------------------- | -------- | ------ | ---------------- |
    | `idInventário` | Número de identificação do inventário                 | Integer  |        | `PK`, `IDENTITY` |
    | `nome`         | Indica o nome do inventário                           | Varchar  | 30     | `NOT NULL`       |
    | `slotMáximo`   | Indica a quantidade máxima de armazenamento de itens  | SmallInt |        | `NOT NULL`       |

??? info "Tabela INST_INVENTARIO | 2.1v"
    **Nome da Tabela:** Inst_Inventario <br/>
    **Descrição**: Armazena as informações das instâncias de inventário dos jogadores <br/>

    | Atributo       | Descrição                                                                            | Tipo     | Limite | Restrições       |
    | -------------- | ------------------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `idInventário` | Referência à Tabela `Inventário` para indicar qual o tipo de inventário              | Integer  |        | `PK`, `FK`       |
    | `nickname`     | Referência à Tabela `Jogador` para indicar à qual jogador esta instância pertence    | Varchar  | 60     | `PK`, `FK`       |
    | `slotOcupado`  | Indica a quantidade de espaço do inventário ocupado                                  | Integer  |        | `NOT NULL`       |

??? info "Tabela NPC | 2.1v"
    **Nome da Tabela:** Npc <br/>
    **Descrição**: Armazena as informações dos NPCs  <br/>

    | Atributo    | Descrição                                         | Tipo     | Limite | Restrições       |
    | ----------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `idNPC`     | Número de identificação do NPC                    | Integer  |        | `PK`, `IDENTITY` |
    | `nome`      | Nome do NPC                                       | Varchar  | 60     | `NOT NULL`       |
    | `tipoNPC`   | Indica se o NPC é do mundo, comercialização ou interação     | Varchar  | 30     | `NOT NULL`       |
    | `descrição` | Descrive como é o NPC de forma narrada            | Varchar  | 100    | `NOT NULL`       |
    | `ativo`     | O NPC está interagindo com o jogador?             | Boolean  |        | `NOT NULL`       |

??? info "Tabela INST_FORJA | 2.1v"
    **Nome da Tabela:** Inst_Forja <br/>
    **Descrição**: Armazena os dados de cada forja existentes em cada Mundo  <br/>

    | Atributo    | Descrição                                         | Tipo     | Limite | Restrições       |
    | ----------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `seedMundo` | Referência à Tabela `Mundo` para indicar à qual mundo a instância de forja pertence      | Varchar  | 30     | `PK`, `FK`       |
    | `nomeLocal` | Referência à Tabela `Estabelecimento` para indicar à qual tipo de estabelecimento a forja pertence | Varchar  | 60     | `FK`, `NOT NULL` |
    | `idNPC`     | Referência à Tabela `Npc` para indicar qual NPC adminstra a instância de forja           | Interger |        | `FK`, `NOT NULL` |

??? info "Tabela INST_FORJA_ITEM | 2.1v"
    **Nome da Tabela:** Inst_Forja_Item <br/>
    **Descrição**: Armazena os itens que podem ser forjados nas instâncias de forjarias  <br/>

    | Atributo    | Descrição                                         | Tipo     | Limite | Restrições         |
    | ----------- | ------------------------------------------------- | -------- | ------ | ------------------ |
    | `idItem`    | Referência à Tabela `Item` para indicar o item disponível para ser forjado                 | Integer  |        | `FK`    |
    | `idMundo`   | Referência à Tabela `Inst_Forja` para indicar qual a instância de forja pode forjar o item | Varchar  | 30     | `FK`    |

??? info "Tabela INST_VAREJO | 2.1v"
    **Nome da Tabela:** Inst_Varejo <br/>
    **Descrição**: Armazena os dados de cada Varejo existentes em cada Mundo  <br/>

    | Atributo      | Descrição                                         | Tipo     | Limite | Restrições       |
    | ------------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `seedMundo`   | Referência à Tabela `Mundo` para indicar à qual mundo a Instância de Varejo pertence     | Varchar  | 30     | `PK`, `FK`       |
    | `nomeLocal`   | Referência à Tabela `Estabelecimento` para indicar qual o tipo de estabelecimento        | Varchar  | 60     | `FK`, `NOT NULL` |
    | `idNPC`       | Referência à Tabela `Npc` para indicar qual NPC adminstra a instância de Verejo          | Integer  |        | `FK`, `NOT NULL` |
    | `margemLucro` | Indica a magem de lucro aplicado sobre o preço base de todos os itens                    | SmallInt |        | `NOT NULL`       |

??? info "Tabela INST_BANCO | 2.1v"
    **Nome da Tabela:** Inst_Banco <br/>
    **Descrição**: Armazena os dados de cada Banco existentes em cada Mundo  <br/>

    | Atributo      | Descrição                                         | Tipo     | Limite | Restrições       |
    | ------------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `seedMundo`   | Referência à Tabela `Mundo` para indicar à qual mundo a Instância de Varejo pertence     | Varchar  | 30     | `PK`, `FK`       |
    | `nomeLocal`   | Referência à Tabela `Estabelecimento` para indicar qual o tipo de estabelecimento        | Varchar  | 60     | `FK`, `NOT NULL` |
    | `idNPC`       | Referência à Tabela `Npc` para indicar qual NPC adminstra a instância de Verejo          | Integer  |        | `FK`, `NOT NULL` |
    | `valorEntrada`| Indica a quantidade de ouros recebido no banco pelo jogador                              | SmallInt |        | `NOT NULL` |
    | `valorAtual`  | Indica a quantidade de ouros atual                                                       | SmallInt |        | `NOT NULL` |

??? info "Tabela INST_ITEM | 2.1v"
    **Nome da Tabela:** Inst_Item <br/>
    **Descrição**: Armazena os dados de Itens Instânciados por  jogador  <br/>

    | Atributo                | Descrição                                         | Tipo     | Limite | Restrições       |
    | ----------------------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `idItem`                | Referência à Tabela `Item` para indicar qual é o item instânciado     | Varchar   | 30   | `PK`, `FK`       |
    | `quantidade`            | Indica a quantidade em _Slot_ do item instânciado                     | SmallItem |      | `NOT NULL`       |
    | `idMonstro`             | Referência à Tabela `Inst_Monstro` para indicar se a instância do item está com alguma instância de monstro | Interger |        | `FK`       |
    | `seedMundoInstMonstro`  | Referência à Tabela `Inst_Monstro` para indicar se a instância do item está com alguma instância de monstro | Varchar  | 30     | `FK`       |
    | `nickname`              | Referência à Tabela `Inst_Inventario` para indicar se a instância do item está no inventário de algum jogador | Varchar  | 60     | `FK`       |
    | `idInventario`          | Referência à Tabela `Inst_Inventario` para indicar se a instância do item está no inventário de algum jogador | Interger |        | `FK`       |
    | `seedMundoInstVarejo`   | Referência à Tabela `Inst_Varejo` para indicar se a instância do item está sendo vendido em um varejo         | Varchar  | 30     | `FK`       |
    | `seedSala`              | Referência à Tabela `Sala` para indicar se a instância do item está em alguma sala                            | Varchar  | 30     | `FK`       |
    | `seedMundoLojaJogador`  | Referência à Tabela `Loja_Jogador` para indicar se a instância do item está exposto em alguma loja do jogador | Varchar  | 30     | `FK`       |

??? info "Tabela DIÁLOGO | 2.1v"
    **Nome da Tabela:** Diálogo <br/>
    **Descrição**: Armazena as informações de cada diálogo possível <br/>

    | Atributo      | Descrição                                                                             | Tipo     | Limite | Restrições       |
    | ------------- | ------------------------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `idDiálogo`   | Número de identificação do diálogo                                                    | Integer  |        | `PK`, `IDENTITY` |
    | `conteúdo`    | Decreve a frase do diálogo                                                            | Varchar  | 300    | `NOT NULL`       |
    | `ordem`       | Indica a ordem do diálogo                                                             | SmallInt |        | `NOT NULL`       |
    | `tipo`        | Indica o tipo de diálogo                                                              | Varchar  | 60     | `NOT NULL`       |
    | `idDialogoPai`| Referência à Tabela `Diálogo` para indicar se este diálogo procede após um diálogo anterior | Integer  |        | `FK`             |

??? info "Tabela DIÁLOGO_NPC | 2.1v"
    **Nome da Tabela:** Diálogo_NPC <br/>
    **Descrição**: Armazena o conjunto de Diálogos que NPC's podem possuir <br/>

    | Atributo     | Descrição                                | Tipo     | Limite | Restrições       |
    | ------------ | ---------------------------------------- | -------- | ------ | ---------------- |
    | `IdDiálogo`  | Referência à Tabela `Diálogo` para indicar qual é o diálogo que o npc possui    | Integer  |        | `FK`, `NOT NULL` |
    | `IdNPC`      | Referência à Tabela `Npc` para indicar qual é o NPC que possui a o diálogo      | Integer  |        | `FK`, `NOT NULL` |

---
As versões abaixo registram Dicionários que foram depreciadas após análises resultantes da evolução e produção do jogo _Moonlighter_:
<br/>
<br/>

<center>
  <span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Dicionário de Dados | Versão 2.0</span>
</center>

??? info "Tabela LOCAL | 2.0v"
    **Nome da Tabela:** Local <br/>
    **Descrição**: Armazena todos os locais disponíveis para locomoção do jogador  <br/>

    | Atributo    | Descrição                            | Tipo     | Limite | Restrições       |
    | ----------- | ------------------------------------ | -------- | ------ | ---------------- |
    | `nomeLocal` | Nome do Local disponível para acesso | Varchar  | 60     | `PK`             |
    | `descricao` | Descrição Narrada de como é o local  | Varchar  | 200    | `NOT NULL`       |
    | `tipoLocal` | Tipo de Local para indentificação às tabelas especializadas `Masmorra` ou `Estabelecimento` ou Nenhum | Varchar  | 20     | `NOT NULL`       |
    | `acesso`    | Referência à tabela `Local` para indicar se o local atual está dentro de outro local  | Varchar  | 60     | `FK`             |

??? info "Tabela MASMORRA | 2.0v"
    **Nome da Tabela:** Masmorra <br/>
    **Descrição**: Armazena configurações de Locais classificadas como Masmorras <br/>

    | Atributo           | Descrição                            | Tipo     | Limite | Restrições       |
    | ------------------ | ------------------------------------ | -------- | ------ | ---------------- |
    | `nomeLocal`        | Referência à tabela `Local`, para indicar qual local é classificado como masmorra | Varchar  | 60     | `PK`, `FK`         |
    | `nivelDesbloqueio` | Indica o nível necessário de Mundo para desbloqueiar a masmorra                     | SmallInt  |        | `NOT NULL`       |
    | `qntAndar`         | Indica quantos andares a masmorra possui  | SmallInt  |        | `NOT NULL`       |

??? info "Tabela ESTABELECIMENTO | 2.0v"
    **Nome da Tabela:** Estabelecimento <br/>
    **Descrição**: Armazena Locais que são classificados como Estabelecimento <br/>

    | Atributo    | Descrição                            | Tipo     | Limite | Restrições       |
    | ----------- | ------------------------------------ | -------- | ------ | ---------------- |
    | `nomeLocal` | Referência à tabela `Local`, para indicar qual local é classificado como estabelecimento       | Varchar  | 60     | `PK`, `PK`         |

??? info "Tabela EFEITO | 2.0v"
    **Nome da Tabela:** Efeito <br/>
    **Descrição**: Armazena as informações dos efeitos dos itens ou jogador <br/>

    | Atributo         | Descrição                                            | Tipo     | Limite | Restrições      |
    | ---------------- | ---------------------------------------------------- | -------- | ------ | --------------- |
    | `idEfeito`       | Número de identificação do efeito                    | Integer  |        | `PK`, `IDENTITY`|
    | `nome`           | Nome do efeito                                       | Varchar  | 30     | `NOT NULL`      |
    | `descrição`      | Descrição do efeito                                  | Varchar  | 100    | `NOT NULL`      |
    | `tipo`           | Tipo do efeito                                       | Varchar  | 15     | `NOT NULL`      |
    | `valor`          | Quantificação de impacto do efeito                   | SmallInt |        | `NOT NULL`      |
    | `duraçãoTurnos`  | Duração de turnos do efeito                          | SmallInt |        |       |

??? info "Tabela JOGADOR | 2.0v"
    **Nome da Tabela:** Jogador <br/>
    **Descrição**: Armazena as informações do jogador <br/>

    | Atributo   | Descrição                                                | Tipo     | Limite | Restrições |
    | ---------- | -------------------------------------------------------- | -------- | ------ | ---------- |
    | `nickname`         | Indica o nome do jogador                                                          | Varchar  | 60     | `PK`       |
    | `maxHP`            | Indica o número máximo de vida disponível do jogador                              | SmallInt |        | `NOT NULL` |
    | `atualHP`          | Indica a vida atual do jogador                                                    | SmallInt |        | `NOT NULL` |
    | `ouro`             | Indica a quantidade de Ouro que o jogador possui                                  | SmallInt |        | `NOT NULL` |
    | `posicaoX_Jogador` | Indica a posição de linha de uma matriz quando estiver dentro da masmorra         | SmallInt |        | `NOT NULL` |
    | `posicaoY_Jogador` | Indica a posição de coluna de uma matriz quando estiver dentro da masmorra        | SmallInt |        | `NOT NULL` |
    | `nomeLocal`        | Referência à Tabela `Local` para indicar onde o jogador está
    | `idEfeito` | Referência à Tabela `Efeito`, identificando se o jogador está sob algum efeito | Integer  |        | `FK`       |

??? info "Tabela MUNDO | 2.0v"
    **Nome da Tabela:** Mundo <br/>
    **Descrição**: Armazena os dados do Mundo em que o jogador está <br/>

    | Atributo         | Descrição                                             | Tipo     | Limite | Restrições     |
    | ---------------- | ----------------------------------------------------- | -------- | ------ | -------------- |
    | `seedMundo`      | Registra a semente de geração do mundo                | Varchar  | 30     | `PK`           |
    | `nickname`       | Referência à tabela `Jogador` para indicar à qual jogador o mundo pertence                | Varchar  | 60      | `FK`, `NOT NULL`      |
    | `periodo`        | Indica o período que o mundo se encontra: Manhã, Tarde, Noite                             | Varchar  | 8       | `NOT NULL`            |
    | `dia`            | Indica a quantidade de dias passados                  | SmallInt |        | `NOT NULL`           |
    | `nivelMundo`     | Indica o nível do mundo para desbloqueio das masmorras| SmallInt |        | `NOT NULL`           |

??? info "Tabela INST_MASMORRA | 2.0v"
    **Nome da Tabela:** Inst_masmorra <br/>
    **Descrição**: Guarda as instâncias de masmorras geradas proceduralmente, após o jogador entrar em uma masmorra <br/>

    | Atributo         | Descrição                                              | Tipo     | Limite | Restrições     |
    | ---------------- | ------------------------------------------------------ | -------- | ------ | -------------- |
    | `seedMundo`      | Referência à tabela `Mundo` para indicar à qual mundo essa instância pertence               | Varchar  | 30     | `PK`, `FK`          |
    | `seedMasmorra`   | Registra a semente de geração da instância de masmorra | Varchar  | 30     | `PK`           |
    | `nomeLocal`      | Referência à tabela `Masmorra` para indicar à qual tipo de masmorra a instância pertence    | Varchar  | 60     | `FK`, `NOT NULL`    |
    | `ativo`          | Indica se a masmorra está sendo explorada pelo jogador ou não                               | Boolean  |        | `NOT NULL`          |

??? info "Tabela SALA | 2.0v"
    **Nome da Tabela:** Sala <br/>
    **Descrição**: Armazena os dados de uma sala, disponível para acesso ao jogador através das instâncias de masmorras <br/>
    
    | Atributo         | Descrição                                             | Tipo     | Limite | Restrições         |
    | ---------------- | ----------------------------------------------------- | -------- | ------ | ------------------ |
    | `seedSala`       | Registra a semente de geração da Sala                 | Varchar  | 30     | `PK`               |
    | `posicaoX`       | Indica em qual posição de linha em uma matriz, a sala está na instância de masmorra            | SmallInt  |        | `NOT NULL`          |
    | `posicaoY`       | Indica em qual posição de coluna em uma matriz, a sala está na instância de masmorra           | SmallInt  |        | `NOT NULL`          |
    | `categoria`      | Indica se a sala é de combate, loot ou do chefe       | Varchar  | 60     | `NOT NULL`          |
    | `seedMundo`      | Referência à Tabela `Inst_Masmorra` para indicar à qual instância de masmorra a sala pertence  | Varchar   | 30     | `FK`, `NOT NULL`    |
    | `seedMasmorra`   | Referência à Tabela `Inst_Masmorra` para indicar à qual instância de masmorra a sala pertence  | Varchar   | 30     | `FK`, `NOT NULL`    |
    | `nomeLocal`      | Referência à Tabela `Masmorra` para indicar à qual tipo de masmorra a sala pertence            | Varchar   | 60     | `FK`, `NOT NULL`    |

??? info "Tabela MONSTRO | 2.0v"
    **Nome da Tabela:** Monstro <br/>
    **Descrição**: Lista o _Bestiário_ (Lista de Monstros) disponível no jogo  <br/>

    | Atributo              | Descrição                                                                               | Tipo     | Limite | Restrições       |
    | --------------------- | --------------------------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `idMonstro`           | Número identificador do monstro                                                         | Integer  |        | `PK`, `IDENTITY` |
    | `nome`                | Indica o nome do monstro                                                                | Varchar  | 30     | `NOT NULL`       |
    | `descrição`           | Descreve o monstro                                                                      | Varchar  | 100    | `NOT NULL`       |
    | `nível`               | Indica o nível do monstro                                                               | SmallInt |        | `NOT NULL`       |
    | `vidaMáxima`          | Indica a vida máxima do monstro                                                         | SmallInt |        | `NOT NULL`       |
    | `ouroDropado`         | Indica a quantidade de ouro que o monstro deixa ao cair                                 | SmallInt |        | `NOT NULL`       |
    | `dadoAtaque`          | Indica o número do dado de ataque do monstro                                            | Varchar  | 4      | `NOT NULL`       |
    | `chanceCrítico`       | Indica a chance de ataque crítico do monstro                                            | Real     |        | `NOT NULL`       |
    | `multiplicador`       | Indica o multiplicador de ataque do monstro                                             | SmallInt |        | `NOT NULL`       |
    | `multiplicadorCrítico`| Indica o multiplicador do ataque crítico do monstro                                     | SmallInt |        | `NOT NULL`       |
    | `chefe`               | O monstro é um chefe?                                                                   | Boolean  |        | `NOT NULL`       |
    | `nomeLocal`           | Referência à tabela `Masmorra` para indicar à qual tipo de masmorra o monstro pertence  | Varchar  | 60     | `FK`, `NOT NULL` |
    | `idEfeito`            | Referência à Tabela `Efeito` para indicar se o monstro possui algum efeito              | Integer  |        | `FK`             |

??? info "Tabela INST_MONSTRO | 2.0v"
    **Nome da Tabela:** Inst_Monstro <br/>
    **Descrição**: Armazena as informações das instâncias dos monstros <br/>

    | Atributo      | Descrição                                            | Tipo     | Limite | Restrições       |
    | ------------- | ---------------------------------------------------- | -------- | ------ | ---------------- |
    | `seedMundo`   | Referência à Tabela `Mundo` para indicar à qual mundo a instância de monstro pertence       | Varchar  | 30     | `PK`, `FK`         |
    | `idMonstro`   | Referência à Tabela `Monstro` para indicar qual é o monstro da instância                    | Integer  |        | `PK`, `FK`         |
    | `vidaAtual`   | Indica a vida atual do monstro                       | SmallInt |        | `NOT NULL`       |
    | `status`      | O monstro está vivo?                                 | Boolean  |        | `NOT NULL`       |
    | `seedSala`    | Referência à Tabela `Sala` para indicar onde a instância de monstro está localizado         | Varchar  | 30     | `FK`, `NOT NULL`   |

??? info "Tabela ITEM | 2.0v"
    **Nome da Tabela:** Item <br/>
    **Descrição**: Lista todos os itens disponíveis no jogo <br/>

    | Atributo        | Descrição                                                               | Tipo     | Limite | Restrições       |
    | --------------- | ----------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `idItem`        | Número de identificação do item                                         | Integer  |        | `PK`, `IDENTITY` |
    | `nome`          | Indica o nome do item                                                   | Varchar  | 80     | `NOT NULL`       |
    | `descrição`     | Descreve o item                                                         | Varchar  | 500    | `NOT NULL`       |
    | `tipo`          | Tipo do item para indentificação às tabelas especializadas `Arma`, `Armadura`, `Pocao` ou Nenhum               | Varchar  | 15     | `NOT NULL`       |
    | `preçoBase`     | Indica o preço base que o item vale em sua venda                        | Interger |        | `NOT NULL`       |
    | `cultura`       | Indica à qual cultura de masmorra o item pertence                       | Varchar  | 10     | `NOT NULL`       |
    | `stackMaximo`   | Indica quantos itens do mesmo tipo eu posso empilhar no mesmo slot      | SmallInt |        | `NOT NULL`       |
    | `idEfeito`      | Referência à Tabela `Efeito` para indicar que efeito o item pode aplicar| Integer  |        | `FK`             |

??? info "Tabela ARMA | 2.0v"
    **Nome da Tabela:** Arma <br/>
    **Descrição**: Armazena as informações dos itens classificadas como arma <br/>

    | Atributo              | Descrição                                    | Tipo     | Limite | Restrições       |
    | --------------------- | -------------------------------------------- | -------- | ------ | ---------------- |
    | `idItem`              | Referência à Tabela `Item` para indicar qual item é classificado como Arma          | Integer  |        | `PK`, `FK`       |
    | `dadoAtaque`          | Número do dado de ataque                     | Varchar  | 4      | `NOT NULL`       |
    | `chanceCrítico`       | Número da chance de dano crítico             | Real     |        | `NOT NULL`       | 
    | `multiplicador`       | Número do multiplicador de dano              | SmallInt |        | `NOT NULL`       |
    | `multiplicadorCrítico`| Número do multiplicador de dano crítico      | SmallInt |        | `NOT NULL`       |
    | `tipoArma`            | Tipo de arma                                 | Varchar  | 15     | `NOT NULL`       |

??? info "Tabela ARMADURA | 2.0v"
    **Nome da Tabela:** Armadura <br/>
    **Descrição**: Armazena as informações dos itens classificadas como armadura <br/>

    | Atributo           | Descrição                                                      | Tipo     | Limite | Restrições       |
    | ------------------ | -------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `idItem`           | Referência à Tabela `Item` para indicar qual item é classificado como Armadura                        | Integer  |        | `PK`, `FK`       |
    | `dadoDefesa`       | Número do dado de defesa                                       | Varchar  | 3      | `NOT NULL`       |
    | `defesaPassiva`    | Número de defesa passiva da armadura                           | SmallInt |        | `NOT NULL`       |
    | `críticoDefensivo` | Valor mínimo no dado para ganhar um bônus de defesa            | SmallInt |        | `NOT NULL`       |
    | `bonusDefesa`      | Valor atribuído à defesa passiva, aumentando a defesa total    | SmallInt |        | `NOT NULL`       |
    | `tipoArmadura`     | Tipo de armadura                                               | Varchar  | 15     | `NOT NULL`       |

??? info "Tabela POCAO | 2.0v"
    **Nome da Tabela:** Pocao <br/>
    **Descrição**: Armazena as informações dos itens classificadas como poção <br/>

    | Atributo         | Descrição                                      | Tipo     | Limite | Restrições       |
    | ---------------- | ---------------------------------------------- | -------- | ------ | ---------------- |
    | `idItem`         | Referência à Tabela `Item` para indicar qual item é classificado como Pocao           | Integer  |        | `PK`, `FK`       |
    | `duraçãoTurnos`  | Duração de turnos de efeito da poção           | SmallInt |        | `NOT NULL`       |

??? info "Tabela MONSTRO_ITEM | 2.0v"
    **Nome da Tabela:** Monstro_Item <br/>
    **Descrição**: Armazena as informações de Itens que Monstros podem deixar cair <br/>

    | Atributo     | Descrição                                                                                  | Tipo     | Limite | Restrições       |
    | ------------ | ------------------------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `idMonstro`  | Referência à Tabela `Monstro` para indicar qual é o monstro que irá deixar o item cair     | Integer  |        | `FK`, `NOT NULL` |
    | `idItem`     | Referência à Tabela `Item` para indicar qual o item o monstro irá deixar cair              | Integer  |        | `FK`, `NOT NULL` |
    | `chanceDrop` | Indica a chance do monstro em deixar cair o item                                           | Real     |        | `NOT NULL`       |
    | `qtdMinima`  | Quantidade mínima em _stack_ do "IdItem" que o monstro "IdMonstro" precisa deixar cair     | SmallInt |        | `NOT NULL`       |
    | `qtdMaxima`  | Quantidade máxima em _stack_ do "IdItem" que o monstro "IdMonstro" pode deixar cair        | SmallInt |        | `NOT NULL`       |

??? info "Tabela RECEITA | 2.0v"
    **Nome da Tabela:** Receita <br/>
    **Descrição**: Armazena as informações das receitas para se fabricar um item <br/>

    | Atributo            | Descrição                                                               | Tipo     | Limite | Restrições       |
    | ------------------- | ----------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `idItemFabricado`   | Referência à Tabela `Item` para identificar o item Fabricado            | Integer  |        | `FK`, `NOT NULL` |
    | `idItemFabricador`  | Referência à Tabela `Item` para identificar o item Fabricador           | Integer  |        | `FK`, `NOT NULL` |
    | `quantidade`        | Quantidade de itens em _stack_ necessários para fabricar o item         | SmallInt |        | `NOT NULL`       |

??? info "Tabela LOJA_JOGADOR | 2.0v"
    **Nome da Tabela:** Loja_Jogador <br/>
    **Descrição**: Armazena as informações das lojas de cada jogador <br/>

    | Atributo          | Descrição                                                       | Tipo     | Limite | Restrições       |
    | ----------------- | --------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `seedMundo`       | Referência à Tabela `Mundo` para indicar o mundo à qual a loja do jogador pertence  | Integer  |        | `PK`, `FK` |
    | `nomeLocal`       | Referência à Tabela `Estabelecimento` para indicar à qual tipo de estabelecimento, a loja do jogador pertence | Integer  |        | `FK`, `NOT NULL` |
    | `nivel`           | Indica o nível da loja do jogador                               | SmallInt |        | `NOT NULL`       |
    | `exposicaoMaxima` | Indica o máximo de itens que o jogador pode expor para venda em sua loja   | SmallInt |        | `NOT NULL`       |
    | `exposicaoUsada`  | Indica o espaço usado de exposição de itens para venda na loja do jogador  | SmallInt |        | `NOT NULL`       |

??? info "Tabela INVENTARIO | 2.0v"
    **Nome da Tabela:** Inventário <br/>
    **Descrição**: Armazena as informações de tipos de inventários existentes no jogo <br/>

    | Atributo       | Descrição                                             | Tipo     | Limite | Restrições       |
    | -------------- | ----------------------------------------------------- | -------- | ------ | ---------------- |
    | `idInventário` | Número de identificação do inventário                 | Integer  |        | `PK`, `IDENTITY` |
    | `nome`         | Indica o nome do inventário                           | Varchar  | 30     | `NOT NULL`       |
    | `slotMáximo`   | Indica a quantidade máxima de armazenamento de itens  | SmallInt |        | `NOT NULL`       |

??? info "Tabela INST_INVENTARIO | 2.0v"
    **Nome da Tabela:** Inst_Inventario <br/>
    **Descrição**: Armazena as informações das instâncias de inventário dos jogadores <br/>

    | Atributo       | Descrição                                                                            | Tipo     | Limite | Restrições       |
    | -------------- | ------------------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `idInventário` | Referência à Tabela `Inventário` para indicar qual o tipo de inventário              | Integer  |        | `PK`, `FK`       |
    | `nickname`     | Referência à Tabela `Jogador` para indicar à qual jogador esta instância pertence    | Varchar  | 60     | `PK`, `FK`       |
    | `slotOcupado`  | Indica a quantidade de espaço do inventário ocupado                                  | Integer  |        | `NOT NULL`       |

??? info "Tabela NPC | 2.0v"
    **Nome da Tabela:** Npc <br/>
    **Descrição**: Armazena as informações dos NPCs  <br/>

    | Atributo    | Descrição                                         | Tipo     | Limite | Restrições       |
    | ----------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `idNPC`     | Número de identificação do NPC                    | Integer  |        | `PK`, `IDENTITY` |
    | `nome`      | Nome do NPC                                       | Varchar  | 60     | `NOT NULL`       |
    | `tipoNPC`   | Indica se o NPC é do mundo, comercialização ou interação     | Varchar  | 30     | `NOT NULL`       |
    | `descrição` | Descrive como é o NPC de forma narrada            | Varchar  | 100    | `NOT NULL`       |
    | `ativo`     | O NPC está interagindo com o jogador?             | Boolean  |        | `NOT NULL`       |

??? info "Tabela INST_FORJA | 2.0v"
    **Nome da Tabela:** Inst_Forja <br/>
    **Descrição**: Armazena os dados de cada forja existentes em cada Mundo  <br/>

    | Atributo    | Descrição                                         | Tipo     | Limite | Restrições       |
    | ----------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `seedMundo` | Referência à Tabela `Mundo` para indicar à qual mundo a instância de forja pertence      | Varchar  | 30     | `PK`, `FK`       |
    | `nomeLocal` | Referência à Tabela `Estabelecimento` para indicar à qual tipo de estabelecimento a forja pertence | Varchar  | 60     | `FK`, `NOT NULL` |
    | `idNPC`     | Referência à Tabela `Npc` para indicar qual NPC adminstra a instância de forja           | Interger |        | `FK`, `NOT NULL` |

??? info "Tabela INST_FORJA_ITEM | 2.0v"
    **Nome da Tabela:** Inst_Forja_Item <br/>
    **Descrição**: Armazena os itens que podem ser forjados nas instâncias de forjarias  <br/>

    | Atributo    | Descrição                                         | Tipo     | Limite | Restrições         |
    | ----------- | ------------------------------------------------- | -------- | ------ | ------------------ |
    | `idItem`    | Referência à Tabela `Item` para indicar o item disponível para ser forjado                 | Integer  |        | `FK`    |
    | `idMundo`   | Referência à Tabela `Inst_Forja` para indicar qual a instância de forja pode forjar o item | Varchar  | 30     | `FK`    |

??? info "Tabela INST_VAREJO | 2.0v"
    **Nome da Tabela:** Inst_Varejo <br/>
    **Descrição**: Armazena os dados de cada Varejo existentes em cada Mundo  <br/>

    | Atributo      | Descrição                                         | Tipo     | Limite | Restrições       |
    | ------------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `seedMundo`   | Referência à Tabela `Mundo` para indicar à qual mundo a Instância de Varejo pertence     | Varchar  | 30     | `PK`, `FK`       |
    | `nomeLocal`   | Referência à Tabela `Estabelecimento` para indicar qual o tipo de estabelecimento        | Varchar  | 60     | `FK`, `NOT NULL` |
    | `idNPC`       | Referência à Tabela `Npc` para indicar qual NPC adminstra a instância de Verejo          | Integer  |        | `FK`, `NOT NULL` |
    | `margemLucro` | Indica a magem de lucro aplicado sobre o preço base de todos os itens                    | SmallInt |        | `NOT NULL`       |

??? info "Tabela INST_BANCO | 2.0v"
    **Nome da Tabela:** Inst_Banco <br/>
    **Descrição**: Armazena os dados de cada Banco existentes em cada Mundo  <br/>

    | Atributo      | Descrição                                         | Tipo     | Limite | Restrições       |
    | ------------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `seedMundo`   | Referência à Tabela `Mundo` para indicar à qual mundo a Instância de Varejo pertence     | Varchar  | 30     | `PK`, `FK`       |
    | `nomeLocal`   | Referência à Tabela `Estabelecimento` para indicar qual o tipo de estabelecimento        | Varchar  | 60     | `FK`, `NOT NULL` |
    | `idNPC`       | Referência à Tabela `Npc` para indicar qual NPC adminstra a instância de Verejo          | Integer  |        | `FK`, `NOT NULL` |
    | `valorEntrada`| Indica a quantidade de ouros recebido no banco pelo jogador                              | SmallInt |        | `NOT NULL` |
    | `valorAtual`  | Indica a quantidade de ouros atual                                                       | SmallInt |        | `NOT NULL` |

??? info "Tabela INST_ITEM | 2.0v"
    **Nome da Tabela:** Inst_Item <br/>
    **Descrição**: Armazena os dados de Itens Instânciados por  jogador  <br/>

    | Atributo                | Descrição                                         | Tipo     | Limite | Restrições       |
    | ----------------------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `idItem`                | Referência à Tabela `Item` para indicar qual é o item instânciado     | Varchar   | 30   | `PK`, `FK`       |
    | `quantidade`            | Indica a quantidade em _Slot_ do item instânciado                     | SmallItem |      | `NOT NULL`       |
    | `idMonstro`             | Referência à Tabela `Inst_Monstro` para indicar se a instância do item está com alguma instância de monstro | Interger |        | `FK`       |
    | `seedMundoInstMonstro`  | Referência à Tabela `Inst_Monstro` para indicar se a instância do item está com alguma instância de monstro | Varchar  | 30     | `FK`       |
    | `nickname`              | Referência à Tabela `Inst_Inventario` para indicar se a instância do item está no inventário de algum jogador | Varchar  | 60     | `FK`       |
    | `idInventario`          | Referência à Tabela `Inst_Inventario` para indicar se a instância do item está no inventário de algum jogador | Interger |        | `FK`       |
    | `seedMundoInstVarejo`   | Referência à Tabela `Inst_Varejo` para indicar se a instância do item está sendo vendido em um varejo         | Varchar  | 30     | `FK`       |
    | `seedSala`              | Referência à Tabela `Sala` para indicar se a instância do item está em alguma sala                            | Varchar  | 30     | `FK`       |
    | `seedMundoLojaJogador`  | Referência à Tabela `Loja_Jogador` para indicar se a instância do item está exposto em alguma loja do jogador | Varchar  | 30     | `FK`       |

??? info "Tabela DIÁLOGO | 2.0v"
    **Nome da Tabela:** Diálogo <br/>
    **Descrição**: Armazena as informações de cada diálogo possível <br/>

    | Atributo      | Descrição                                                                             | Tipo     | Limite | Restrições       |
    | ------------- | ------------------------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `idDiálogo`   | Número de identificação do diálogo                                                    | Integer  |        | `PK`, `IDENTITY` |
    | `conteúdo`    | Decreve a frase do diálogo                                                            | Varchar  | 300    | `NOT NULL`       |
    | `ordem`       | Indica a ordem do diálogo                                                             | SmallInt |        | `NOT NULL`       |
    | `tipo`        | Indica o tipo de diálogo                                                              | Varchar  | 60     | `NOT NULL`       |
    | `idDialogoPai`| Referência à Tabela `Diálogo` para indicar se este diálogo procede após um diálogo anterior | Integer  |        | `FK`             |

??? info "Tabela DIÁLOGO_NPC | 2.0v"
    **Nome da Tabela:** Diálogo_NPC <br/>
    **Descrição**: Armazena o conjunto de Diálogos que NPC's podem possuir <br/>

    | Atributo     | Descrição                                | Tipo     | Limite | Restrições       |
    | ------------ | ---------------------------------------- | -------- | ------ | ---------------- |
    | `IdDiálogo`  | Referência à Tabela `Diálogo` para indicar qual é o diálogo que o npc possui    | Integer  |        | `FK`, `NOT NULL` |
    | `IdNPC`      | Referência à Tabela `Npc` para indicar qual é o NPC que possui a o diálogo      | Integer  |        | `FK`, `NOT NULL` |

---

<center>
  <span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Dicionário de Dados | Versão 1.1</span>
</center>

??? info "Tabela MASMORRA | 1.1v"
    **Nome da Tabela:** Masmorra <br/>
    **Descrição**: Armazena os tipos de masmorras para ser explorada <br/>

    | Atributo          | Descrição                                | Tipo       | Limite | Restrições     |
    | ----------------- | ---------------------------------------- | ---------- | ------ | -------------- |
    | `NomeMasmorra`    | Nome da masmorra                         | Varchar    | 30     | `PK`           |
    | `Descricao`       | Descrição da masmorra                    | Varchar    | 100    | `NOT NULL`     |
    | `Nivel`           | Nível de dificuldade da masmorra         | SmallInt   |        | `NOT NULL`     |
    | `QtdAndar`        | Quantidade de andares da masmorra        | SmallInt   |        | `NOT NULL`     |

??? info "Tabela INST_MASMORRA | 1.1v"
    **Nome da Tabela:** Inst_Masmorra <br/>
    **Descrição**: Armazena as informações das instâncias de masmorras criadas de forma procedural <br/>
        
    | Atributo            | Descrição                                   | Tipo     | Limite | Restrições            |
    | ------------------- | ------------------------------------------- | -------- | ------ | --------------------- |
    | `NomeMasmorra`      | Nome da masmorra                            | Varchar  | 30     | `PK`, `FK`            |
    | `SeedMasmorra`      | Semente de geração da masmorra              | Varchar  | 10     | `PK`                  |
    | `PosiçãoX_Jogador`  | Posição do jogador na coordenada X          | Integer  |        | `NOT NULL`            |
    | `PosiçãoY_Jogador`  | Posição do jogador na coordenada Y          | Integer  |        | `NOT NULL`            |

??? info "Tabela SALA | 1.1v"
    **Nome da Tabela:** Sala <br/>
    **Descrição**: Armazena as informações de salas para as inst_masmorras, criadas de forma procedural <br/>

    | Atributo          | Descrição                                           | Tipo       | Limite | Restrições       |
    | ----------------- | --------------------------------------------------- | ---------- | ------ | ---------------- |
    | `SeedSala`        | Semente de geração da sala                          | Varchar    | 10     | `PK`             |
    | `PosicaoX`        | Posição da sala na coordenada X                     | Integer    |        | `NOT NULL`       |
    | `PosicaoY`        | Posição da sala na coordenada Y                     | Integer    |        | `NOT NULL`       |
    | `Categoria`       | Categoria da sala                                   | Varchar    | 60     | `NOT NULL`       |
    | `NomeMasmorra`    | Refernência à Inst_Masmorra que se encontra a sala  | Varchar    | 30     | `FK`, `NOT NULL` |

??? info "Tabela SALA_INST_MASMORRA | 1.1v"
    **Nome da Tabela:** Sala_Inst_Masmorra <br/>
    **Descrição**: Armazena o conjunto de salas que pertencem à uma instância de masmorra <br/>

    | Atributo        | Descrição                                                                                   | Tipo     | Limite | Restrições         |
    | --------------- | ------------------------------------------------------------------------------------------- | -------- | ------ | ------------------ |
    | `SeedSala`      | Referência à Tabela "Sala", indicando qual a sala                                           | Varchar  | 10     | `FK`, `NOT NULL`   |
    | `SeedMasmorra`  | Referência à Tabela "Inst_Masmorra", indicando qual instância de masmorra a sala pertence   | Varchar  | 30     | `FK`, `NOT NULL`   |
    | `Explorada`     | A sala já foi explorada?                                                                    | Boolean  |        | `NOT NULL`         |


??? info "Tabela MAPA | 1.1v"
    **Nome da Tabela:** Mapa <br/>
    **Descrição**: Armazena as informações do mapa do jogo <br/>

    | Atributo   | Descrição                           | Tipo     | Limite | Restrições       |
    | ---------- | ----------------------------------- | -------- | ------ | ---------------- |
    | `IdMapa`   | Número identificador do mapa        | Integer  |        | `PK`, `IDENTITY` |
    | `Período`  | Período do dia do mapa              | Varchar  | 8      | `NOT NULL`       |
    | `Dia`      | Dias passados no jogo               | Integer  |        | `NOT NULL`       |

??? info "Tabela MASMORRA_MAPA | 1.1v"
    **Nome da Tabela:** Masmorra_Mapa <br/>
    **Descrição**: Armazena as informações das masmorras existentes em cada mapa do jogo <br/>

    | Atributo        | Descrição                                | Tipo     | Limite | Restrições        |
    | --------------- | ---------------------------------------- | -------- | ------ | ----------------- |
    | `NomeMasmorra`  | Referência à Tabela "Masmorra"           | Varchar  | 30     | `FK`, `NOT NULL`  |
    | `IdMapa`        | Referência à Tabela "Mapa"               | Integer  |        | `FK`, `NOT NULL`  |
    | `Desbloqueado`  | A masmorra foi desbloqueada?             | Boolean  |        | `NOT NULL`        |

??? info "Tabela EFEITO | 1.1v"
    **Nome da Tabela:** Efeito <br/>
    **Descrição**: Armazena as informações dos efeitos dos itens ou jogador <br/>

    | Atributo         | Descrição                                            | Tipo     | Limite | Restrições      |
    | ---------------- | ---------------------------------------------------- | -------- | ------ | --------------- |
    | `IdEfeito`       | Número de identificação do efeito                    | Integer  |        | `PK`, `IDENTITY`|
    | `Nome`           | Nome do efeito                                       | Varchar  | 30     | `NOT NULL`      |
    | `Descrição`      | Descrição do efeito                                  | Varchar  | 100    | `NOT NULL`      |
    | `Tipo`           | Tipo do efeito                                       | Varchar  | 15     | `NOT NULL`      |
    | `Valor`          | Quantificação de impacto do efeito                   | SmallInt |        | `NOT NULL`      |
    | `DuraçãoTurnos`  | Duração de turnos do efeito                          | SmallInt |        |       |

??? info "Tabela MONSTRO | 1.1v"
    **Nome da Tabela:** Monstro <br/>
    **Descrição**: Armazena as informações de monstros  <br/>

    | Atributo              | Descrição                                                                      | Tipo     | Limite | Restrições       |
    | --------------------- | ------------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `IdMonstro`           | Número identificador do monstro                                                | Integer  |        | `PK`, `IDENTITY` |
    | `Nome`                | Nome do monstro                                                                | Varchar  | 30     | `NOT NULL`       |
    | `Descrição`           | Descrição do monstro                                                           | Varchar  | 100    | `NOT NULL`       |
    | `Nível`               | Nível do monstro                                                               | SmallInt |        | `NOT NULL`       |
    | `VidaMáxima`          | Vida máxima do monstro                                                         | SmallInt |        | `NOT NULL`       |
    | `OuroDropado`         | Quantidade de ouro que o monstro deixa ao cair                                 | SmallInt |        | `NOT NULL`       |
    | `DadoAtaque`          | Número do dado de ataque do monstro                                            | Varchar  | 3      | `NOT NULL`       |
    | `ChanceCrítico`       | Chance de ataque crítico do monstro                                            | Real     |        | `NOT NULL`       |
    | `Multiplicador`       | Multiplicador de ataque do monstro                                             | SmallInt |        | `NOT NULL`       |
    | `MultiplicadorCrítico`| Multiplicador do ataque crítico do monstro                                     | SmallInt |        | `NOT NULL`       |
    | `Chefe`               | O monstro é um chefe?                                                          | Boolean  |        | `NOT NULL`       |
    | `NomeMasmorra`        | Referência à tabela "Masmorra", indicando de qual tipo de masmorra o monstro é | Varchar  | 60     | `FK`, `NOT NULL` |
    | `IdEfeito`            | Referência à Tabela "Efeito", indicando se o monstro possui algum efeito       | Integer  |        | `FK`             |

??? info "Tabela INST_MONSTRO | 1.1v"
    **Nome da Tabela:** Inst_Monstro <br/>
    **Descrição**: Armazena as informações das instâncias dos monstros <br/>

    | Atributo      | Descrição                                            | Tipo     | Limite | Restrições       |
    | ------------- | ---------------------------------------------------- | -------- | ------ | ---------------- |
    | `SeedMonstro` | Semente de geração do monstro                        | Integer  |        | `PK`             |
    | `IdMonstro`   | Número identificador do monstro                      | Integer  |        | `PK`, `FK`       |
    | `VidaAtual`   | Vida atual do monstro                                | SmallInt |        | `NOT NULL`       |
    | `Status`      | O monstro está vivo?                                 | Boolean  |        | `NOT NULL`       |
    | `SeedSala`    | Semente de geração da sala em que o monstro está     | Varchar  | 10     | `FK`, `NOT NULL` |

??? info "Tabela ITEM | 1.1v"
    **Nome da Tabela:** Item <br/>
    **Descrição**: Armazena as informações de itens <br/>

    | Atributo        | Descrição                                                               | Tipo     | Limite | Restrições       |
    | --------------- | ----------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdItem`        | Número de identificação do item                                         | Integer  |        | `PK`, `IDENTITY` |
    | `Nome`          | Nome do item                                                            | Varchar  | 80     | `NOT NULL`       |
    | `Descrição`     | Descrição do item                                                       | Varchar  | 500    | `NOT NULL`       |
    | `Tipo`          | Tipo do item                                                            | Varchar  | 15     |                  |
    | `PreçoBase`     | Preço base que o item vale em sua venda                                 | Interger |        | `NOT NULL`       |
    | `Cultura`       | À qual cultura de masmorra o item pertence                              | Varchar  | 10     | `NOT NULL`       |
    | `StackMaximo`   | Quantos itens do mesmo tipo eu posso empilhar no mesmo slot             | SmallInt |        | `NOT NULL`       |
    | `IdEfeito`      | Referência à Tabela "Efeito", indicando que efeito o item pode aplicar  | Integer  |        | `FK`             |

??? info "Tabela ARMA | 1.1v"
    **Nome da Tabela:** Arma <br/>
    **Descrição**: Armazena as informações dos itens tipo arma <br/>

    | Atributo              | Descrição                                    | Tipo     | Limite | Restrições       |
    | --------------------- | -------------------------------------------- | -------- | ------ | ---------------- |
    | `IdItem`              | Referência à Tabela "Item"                   | Integer  |        | `PK`, `FK`       |
    | `DadoAtaque`          | Número do dado de ataque                     | Varchar  | 3      | `NOT NULL`       |
    | `ChanceCrítico`       | Número da chance de dano crítico             | Real     |        | `NOT NULL`       | 
    | `Multiplicador`       | Número do multiplicador de dano              | SmallInt |        | `NOT NULL`       |
    | `MultiplicadorCrítico`| Número do multiplicador de dano crítico      | SmallInt |        | `NOT NULL`       |
    | `TipoArma`            | Tipo de arma                                 | Varchar  | 15     | `NOT NULL`       |

??? info "Tabela ARMADURA | 1.1v"
    **Nome da Tabela:** Armadura <br/>
    **Descrição**: Armazena as informações dos itens tipo armadura <br/>

    | Atributo           | Descrição                                                      | Tipo     | Limite | Restrições       |
    | ------------------ | -------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdItem`           | Referência à Tabela "Item"                                     | Integer  |        | `PK`, `FK`       |
    | `DadoDefesa`       | Número do dado de defesa                                       | Varchar  | 3      | `NOT NULL`       |
    | `DefesaPassiva`    | Número de defesa passiva da armadura                           | Integer  |        | `NOT NULL`       |
    | `CríticoDefensivo` | Valor mínimo no dado para ganhar um bônus de defesa            | Integer  |        | `NOT NULL`       |
    | `BonusDefesa`      | Valor atribuído à defesa passiva, aumentando a defesa total    | Integer  |        | `NOT NULL`       |
    | `TipoArmadura`     | Tipo de armadura                                               | Varchar  | 15     | `NOT NULL`       |

??? info "Tabela POÇÃO | 1.1v"
    **Nome da Tabela:** Poção <br/>
    **Descrição**: Armazena as informações dos itens tipo poção <br/>

    | Atributo         | Descrição                                      | Tipo     | Limite | Restrições       |
    | ---------------- | ---------------------------------------------- | -------- | ------ | ---------------- |
    | `IdItem`         | Referência à Tabela "Item"                     | Integer  |        | `PK`, `FK`       |
    | `DuraçãoTurnos`  | Duração de turnos de efeito da poção           | SmallInt |        | `NOT NULL`       |

??? info "Tabela MONSTRO_ITEM | 1.1v"
    **Nome da Tabela:** Monstro_Item <br/>
    **Descrição**: Armazena as informações de Itens que Monstros podem deixar cair <br/>

    | Atributo     | Descrição                                                                                  | Tipo     | Limite | Restrições       |
    | ------------ | ------------------------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `IdMonstro`  | Referência à Tabela "Monstro"                                                              | Integer  |        | `FK`, `NOT NULL` |
    | `IdItem`     | Referência à Tabela "Item"                                                                 | Integer  |        | `FK`, `NOT NULL` |
    | `ChanceDrop` | Número da chance do monstro deixar cair um item                                            | Real     |        | `NOT NULL`       |
    | `QtdMinima`  | Quantidade mínima em _stack_ do "IdItem" que o monstro "IdMonstro" precisa deixar cair     | SmallInt |        | `NOT NULL`       |
    | `QtdMaxima`  | Quantidade máxima em _stack_ do "IdItem" que o monstro "IdMonstro" pode deixar cair        | SmallInt |        | `NOT NULL`       |

??? info "Tabela RECEITA | 1.1v"
    **Nome da Tabela:** Receita <br/>
    **Descrição**: Armazena as informações das receitas para se fabricar um item <br/>

    | Atributo    | Descrição                                                       | Tipo     | Limite | Restrições       |
    | ----------- | --------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdItemR`   | Referência à Tabela "Item", identificando o item Fabricado      | Integer  |        | `FK`, `NOT NULL` |
    | `IdItem`    | Referência à Tabela "Item", identificando o item Fabricador     | Integer  |        | `FK`, `NOT NULL` |
    | `Quantidade`| Quantidade de itens em _stack_ necessários para fabricar o item | SmallInt |        | `NOT NULL`       |

??? info "Tabela JOGADOR | 1.1v"
    **Nome da Tabela:** Jogador <br/>
    **Descrição**: Armazena as informações do jogador <br/>

    | Atributo   | Descrição                                                                      | Tipo     | Limite | Restrições |
    | ---------- | ------------------------------------------------------------------------------ | -------- | ------ | ---------- |
    | `Nickname` | Nome único do jogador                                                          | Varchar  | 60     | `PK`       |
    | `MaxHP`    | Número máximo de vida do jogador                                               | SmallInt |        | `NOT NULL` |
    | `AtualHP`  | Vida atual do jogador                                                          | SmallInt |        | `NOT NULL` |
    | `Ouro`     | Quantidade de Ouro do jogador                                                  | SmallInt |        | `NOT NULL` |
    | `IdEfeito` | Referência à Tabela "Efeito", identificando se o jogador está sob algum efeito | Integer  |        | `FK`       |

??? info "Tabela LOJA_JOGADOR | 1.1v"
    **Nome da Tabela:** LojaJogador <br/>
    **Descrição**: Armazena as informações da loja do jogador <br/>

    | Atributo           | Descrição                                                                    | Tipo     | Limite | Restrições       |
    | ------------------ | ---------------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `NickName`         | Referência à Tabela "Jogador", identificando a qual jogador a loja pertence  | Varchar  | 60     | `PK`, `FK`       |
    | `Nível`            | Nível da loja do jogador                                                     | SmallInt |        | `NOT NULL`       |
    | `ExposiçãoMáxima`  | Número máximo de itens que podem ser expostos na loja do jogador             | SmallInt |        | `NOT NULL`       |
    | `ExposiçãoUsada`   | Número de itens atualmente expostos na loja do jogador                       | SmallInt |        | `NOT NULL`       |
    | `IdMapa`           | Número de identificação do mapa do mundo                                     | Integer  |        | `FK`, `NOT NULL` |

??? info "Tabela INVENTARIO | 1.1v"
    **Nome da Tabela:** Inventário <br/>
    **Descrição**: Armazena as informações de tipos de inventários existentes no jogo <br/>

    | Atributo       | Descrição                                             | Tipo     | Limite | Restrições       |
    | -------------- | ----------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdInventário` | Número de identificação do inventário                 | Integer  |        | `PK`, `IDENTITY` |
    | `Nome`         | Nome do inventário                                    | Varchar  | 30     | `NOT NULL`       |
    | `SlotMáximo`   | Quantidade máxima de armazenamento de itens           | SmallInt |        | `NOT NULL`       |

??? info "Tabela INST_INVENTARIO | 1.1v"
    **Nome da Tabela:** Inst_Inventario <br/>
    **Descrição**: Armazena as informações das instâncias de inventário dos jogadores <br/>

    | Atributo       | Descrição                                                                            | Tipo     | Limite | Restrições       |
    | -------------- | ------------------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `IdInventário` | Referência à Tabela "Inventário", indicando qual o tipo de inventário                | Integer  |        | `PK`, `FK`       |
    | `SlotOcupado`  | Quantidade de lugares do inventário ocupados                                         | Integer  |        | `NOT NULL`       |
    | `Nickname`     | Referência à Tabela "Jogador", indicando à qual jogador esta instância pertence      | Varchar  | 60     | `FK`, `NOT NULL` |

??? info "Tabela NPC | 1.2v"
    **Nome da Tabela:** NPC <br/>
    **Descrição**: Armazena as informações dos NPCs  <br/>

    | Atributo    | Descrição                                         | Tipo     | Limite | Restrições       |
    | ----------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdNPC`     | Número de identificação do NPC                    | Integer  |        | `PK`, `IDENTITY` |
    | `Nome`      | Nome do NPC                                       | Varchar  | 60     | `NOT NULL`       |
    | `TipoNPC`   | Tipo de NPC                                       | Varchar  | 30     | `NOT NULL`       |
    | `Descrição` | Descrição do NPC                                  | Varchar  | 100    | `NOT NULL`       |
    | `Ativo`     | O NPC está interagindo com o jogador?             | Boolean  |        | `NOT NULL`       |


??? info "Tabela LOJANPC | 1.1v"
    **Nome da Tabela:** LojaNPC <br/>
    **Descrição**: Armazena as informações da loja do NPC <br/>

    | Atributo     | Descrição                                                                | Tipo     | Limite | Restrições       |
    | ------------ | ------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `IdLojaNPC`  | Número de identificação da loja do NPC                                   | Integer  |        | `PK`, `IDENTITY` |
    | `Nome`       | Nome da loja do NPC                                                      | Varchar  | 30     | `NOT NULL`       |
    | `TipoLoja`   | Tipo da loja do NPC                                                      | Varchar  | 30     | `NOT NULL`       |
    | `Descrição`  | Descrição da loja do NPC                                                 | Varchar  | 120    | `NOT NULL`       |
    | `Status`     | A loja está em uso pelo jogador?                                         | Boolean  |        | `NOT NULL`       |
    | `IdNPC`      | Referência à Tabela "NPC", indicando qual NPC cuida da loja              | Integer  |        | `FK`, `NOT NULL` |
    | `IdMapa`     | Referência à Tabela "Mapa", indicando a qual mapa a loja pertence        | Integer  |        | `FK`, `NOT NULL` |

??? info "Tabela FORJARIA | 1.1v"
    **Nome da Tabela:** Forjaria <br/>
    **Descrição**: Armazena as informações da loja do NPC tipo forjaria <br/>

    | Atributo     | Descrição                                  | Tipo     | Limite | Restrições       |
    | ------------ | ------------------------------------------ | -------- | ------ | ---------------- |
    | `IdLojaNPC`  | Referência à Tabela "LojaNPC"              | Integer  |        | `PK`, `FK`       |


??? info "Tabela VAREJO | 1.1v"
    **Nome da Tabela:** Varejo <br/>
    **Descrição**: Armazena as informações da loja do NPC tipo varejo <br/>

    | Atributo      | Descrição                                         | Tipo     | Limite | Restrições       |
    | ------------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdLojaNPC`   | Referência à Tabela "LojaNPC"                     | Integer  |        | `PK`, `FK`       |
    | `MargemLucro` | Margem de lucro dos itens do NPC                  | SmallInt |        | `NOT NULL`       |

??? info "Tabela BANCO | 1.1v"
    **Nome da Tabela:** Banco <br/>
    **Descrição**: Armazena as informações da loja do NPC tipo banco <br/>

    | Atributo        | Descrição                                               | Tipo     | Limite | Restrições       |
    | --------------- | ------------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdLojaNPC`     | Referência à Tabela "LojaNPC"                           | Integer  |        | `PK`, `FK`       |
    | `ValorEntrada`  | Valor do ouro de entrada depositado pelo jogador        | SmallInt |        |                  |
    | `ValorAtual`    | Valor atual do ouro com rendimento do jogador           | SmallInt |        | `NOT NULL`       |

??? info "Tabela INST_ITEM | 1.1v"
    **Nome da Tabela:** Inst_Item <br/>
    **Descrição**: Armazena as informações das instâncias dos itens <br/>

    | Atributo       | Descrição                                                    | Tipo     | Limite | Restrições   |
    | -------------- | ------------------------------------------------------------ | -------- | ------ | ------------ |
    | `IdItem`       | Referência à Tabela "Item"                                   | Integer  |        | `PK`, `FK`   |
    | `Quantidade`   | Quantidade em _stack_ do item                                | SmallInt |        | `NOT NULL`   |
    | `SeedMonstro`  | Referência à Tabela "Inst_Monstro" que está com o item       | Integer  |        | `FK`         |
    | `IdInventário` | Referência à Tabela "Inst_Inventário" em que está o item     | Integer  |        | `FK`         |
    | `IdLojaNPC`    | Referência à Tabela "LojaNPC" em que está o item             | Integer  |        | `FK`         |
    | `SeedSala`     | Referência à Tabela "Sala" que contém o item                 | Varchar  | 10     | `FK`         |
    | `NickName`     | Referência à Tabela "Loja_Jogador" que contém o item         | Varchar  | 60     | `FK`         |

??? info "Tabela DIÁLOGO | 1.1v"
    **Nome da Tabela:** Diálogo <br/>
    **Descrição**: Armazena as informações de cada diálogo possível <br/>

    | Atributo      | Descrição                                                                             | Tipo     | Limite | Restrições       |
    | ------------- | ------------------------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdDiálogo`   | Número de identificação do diálogo                                                    | Integer  |        | `PK`, `IDENTITY` |
    | `Conteúdo`    | Conteúdo do diálogo                                                                   | Varchar  | 300    | `NOT NULL`       |
    | `Ordem`       | Ordem do diálogo                                                                      | SmallInt |        | `NOT NULL`       |
    | `Tipo`        | Tipo de diálogo                                                                       | Varchar  | 60     | `NOT NULL`       |
    | `IdDialogoPai`| Referência à Tabela "Diálogo", indicando se este diálogo procede após um diálogo pai  | Integer  |        | `FK`             |

??? info "Tabela DIÁLOGO_NPC | 1.1v"
    **Nome da Tabela:** Diálogo_NPC <br/>
    **Descrição**: Armazena o conjunto de Diálogos que NPC's podem possuir <br/>

    | Atributo     | Descrição                                | Tipo     | Limite | Restrições       |
    | ------------ | ---------------------------------------- | -------- | ------ | ---------------- |
    | `IdDiálogo`  | Referência à Tabela "Diálogo"            | Integer  |        | `FK`, `NOT NULL` |
    | `IdNPC`      | Referência à Tabela "NPC"                | Integer  |        | `FK`, `NOT NULL` |

---

<center>
  <span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Dicionário de Dados | Versão 1.0</span>
</center>

??? info "Tabela MASMORRA | 1.0v"
    **Nome da Tabela:** Masmorra <br/>
    **Descrição**: Armazena os tipos de masmorras para ser explorada <br/>

    | Atributo          | Descrição                                | Tipo       | Limite | Restrições     |
    | ----------------- | ---------------------------------------- | ---------- | ------ | -------------- |
    | `NomeMasmorra`    | Nome da masmorra                         | Varchar    | 30     | `PK`           |
    | `Descricao`       | Descrição da masmorra                    | Varchar    | 100    | `NOT NULL`     |
    | `Nivel`           | Nível de dificuldade da masmorra         | Integer    |        | `NOT NULL`     |
    | `QtdAndar`        | Quantidade de andares da masmorra        | Integer    |        | `NOT NULL`     |

??? info "Tabela INST_MASMORRA | 1.0v"
    **Nome da Tabela:** Inst_Masmorra <br/>
    **Descrição**: Armazena as informações das instâncias de masmorras criadas de forma procedural <br/>
        
    | Atributo            | Descrição                                   | Tipo     | Limite | Restrições            |
    | ------------------- | ------------------------------------------- | -------- | ------ | --------------------- |
    | `NomeMasmorra`      | Nome da masmorra                            | Varchar  | 30     | `PK`, `FK`            |
    | `SeedMasmorra`      | Semente de geração da masmorra              | Varchar  | 10     | `UNIQUE`, `NOT NULL`  |
    | `PosiçãoX_Jogador`  | Posição do jogador na coordenada X          | Integer  |        | `NOT NULL`            |
    | `PosiçãoY_Jogador`  | Posição do jogador na coordenada Y          | Integer  |        | `NOT NULL`            |

??? info "Tabela SALA | 1.0v"
    **Nome da Tabela:** Sala <br/>
    **Descrição**: Armazena as informações de salas para as inst_masmorras, criadas de forma procedural <br/>

    | Atributo          | Descrição                                           | Tipo       | Limite | Restrições       |
    | ----------------- | --------------------------------------------------- | ---------- | ------ | ---------------- |
    | `SeedSala`        | Semente de geração da sala                          | Varchar    | 10     | `PK`             |
    | `PosicaoX`        | Posição da sala na coordenada X                     | Integer    |        | `NOT NULL`       |
    | `PosicaoY`        | Posição da sala na coordenada Y                     | Integer    |        | `NOT NULL`       |
    | `Categoria`       | Categoria da sala                                   | Varchar    | 60     | `NOT NULL`       |
    | `Explorada`       | A sala já foi explorada?                            | Boolean    |        | `NOT NULL`       |
    | `NomeMasmorra`    | Refernência à Inst_Masmorra que se encontra a sala  | Varchar    | 30     | `FK`, `NOT NULL` |

??? info "Tabela SALA_INST_MASMORRA | 1.0v"
    **Nome da Tabela:** Sala_Inst_Masmorra <br/>
    **Descrição**: Armazena o conjunto de salas que pertencem à uma instância de masmorra <br/>

    | Atributo        | Descrição                                                                                   | Tipo     | Limite | Restrições         |
    | --------------- | ------------------------------------------------------------------------------------------- | -------- | ------ | ------------------ |
    | `SeedSala`      | Referência à Tabela "Sala", indicando qual a sala                                           | Varchar  | 10     | `FK`, `NOT NULL`   |
    | `NomeMasmorra`  | Referência à Tabela "Inst_Masmorra", indicando qual instância de masmorra a sala pertence   | Varchar  | 30     | `FK`, `NOT NULL`   |

??? info "Tabela MAPA | 1.0v"
    **Nome da Tabela:** Mapa <br/>
    **Descrição**: Armazena as informações do mapa do jogo <br/>

    | Atributo   | Descrição                           | Tipo     | Limite | Restrições       |
    | ---------- | ----------------------------------- | -------- | ------ | ---------------- |
    | `IdMapa`   | Número identificador do mapa        | Integer  |        | `PK`, `IDENTITY` |
    | `Período`  | Período do dia do mapa              | Varchar  | 8      | `NOT NULL`       |
    | `Dia`      | Data do dia que está o mapa         | Integer  |        | `NOT NULL`       |

??? info "Tabela MASMORRA_MAPA | 1.0v"
    **Nome da Tabela:** Masmorra_Mapa <br/>
    **Descrição**: Armazena as informações das masmorras existentes em cada mapa do jogo <br/>

    | Atributo        | Descrição                                | Tipo     | Limite | Restrições        |
    | --------------- | ---------------------------------------- | -------- | ------ | ----------------- |
    | `NomeMasmorra`  | Referência à Tabela "Masmorra"           | Varchar  | 30     | `FK`, `NOT NULL`  |
    | `IdMapa`        | Referência à Tabela "Mapa"               | Integer  |        | `FK`, `NOT NULL`  |
    | `Desbloqueado`  | A masmorra foi desbloqueada?             | Boolean  |        | `NOT NULL`        |

??? info "Tabela MONSTRO | 1.0v"
    **Nome da Tabela:** Monstro <br/>
    **Descrição**: Armazena as informações de monstros  <br/>

    | Atributo              | Descrição                                                                      | Tipo     | Limite | Restrições       |
    | --------------------- | ------------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `IdMonstro`           | Número identificador do monstro                                                | Integer  |        | `PK`, `IDENTITY` |
    | `Nome`                | Nome do monstro                                                                | Varchar  | 30     | `NOT NULL`       |
    | `Descrição`           | Descrição do monstro                                                           | Varchar  | 100    | `NOT NULL`       |
    | `Nível`               | Nível do monstro                                                               | Integer  |        | `NOT NULL`       |
    | `VidaMáxima`          | Vida máxima do monstro                                                         | Integer  |        | `NOT NULL`       |
    | `OuroDropado`         | Quantidade de ouro que o monstro deixa ao cair                                 | Integer  |        | `NOT NULL`       |
    | `DadoAtaque`          | Número do dado de ataque do monstro                                            | Varchar  | 3      | `NOT NULL`       |
    | `ChanceCrítico`       | Chance de ataque crítico do monstro                                            | Float    |        | `NOT NULL`       |
    | `Multiplicador`       | Multiplicador de ataque do monstro                                             | Integer  |        | `NOT NULL`       |
    | `MultiplicadorCrítico`| Multiplicador do ataque crítico do monstro                                     | Integer  |        | `NOT NULL`       |
    | `Chefe`               | O monstro é um chefe?                                                          | Boolean  |        | `NOT NULL`       |
    | `NomeMasmorra`        | Referência à tabela "Masmorra", indicando de qual tipo de masmorra o monstro é | Varchar  | 60     | `FK`, `NOT NULL` |
    | `IdEfeito`            | Referência à Tabela "Efeito", indicando se o monstro possui algum efeito       | Integer  |        | `FK`             |

??? info "Tabela INST_MONSTRO | 1.0v"
    **Nome da Tabela:** Inst_Monstro <br/>
    **Descrição**: Armazena as informações das instâncias dos monstros <br/>

    | Atributo      | Descrição                                            | Tipo     | Limite | Restrições       |
    | ------------- | ---------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdMonstro`   | Número identificador do monstro                      | Integer  |        | `PK`, `FK`       |
    | `VidaAtual`   | Vida atual do monstro                                | Integer  |        | `NOT NULL`       |
    | `Status`      | O monstro está vivo?                                 | Boolean  |        | `NOT NULL`       |
    | `SeedSala`    | Semente de geração da sala em que o monstro está     | Varchar  | 10     | `FK`, `NOT NULL` |

??? info "Tabela ITEM | 1.0v"
    **Nome da Tabela:** Item <br/>
    **Descrição**: Armazena as informações de itens <br/>

    | Atributo        | Descrição                                                               | Tipo     | Limite | Restrições       |
    | --------------- | ----------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdItem`        | Número de identificação do item                                         | Integer  |        | `PK`, `IDENTITY` |
    | `Nome`          | Nome do item                                                            | Varchar  | 30     | `NOT NULL`       |
    | `Descrição`     | Descrição do item                                                       | Varchar  | 60     | `NOT NULL`       |
    | `Tipo`          | Tipo do item                                                            | Varchar  | 15     | `NOT NULL`       |
    | `PreçoBase`     | Preço base que o item vale em sua venda                                 | Integer  |        | `NOT NULL`       |
    | `Raridade`      | Número de raridade do item                                              | Integer  |        | `NOT NULL`       |
    | `StackMáximo`   | Quantidade máxima que o item pode ser empilhado                         | Integer  |        | `NOT NULL`       |
    | `IdEfeito`      | Referência à Tabela "Efeito", indicando que efeito o item pode aplicar  | Integer  |        | `FK`             |

??? info "Tabela ARMA | 1.0v"
    **Nome da Tabela:** Arma <br/>
    **Descrição**: Armazena as informações dos itens tipo arma <br/>

    | Atributo              | Descrição                                    | Tipo     | Limite | Restrições       |
    | --------------------- | -------------------------------------------- | -------- | ------ | ---------------- |
    | `IdItem`              | Referência à Tabela "Item"                   | Integer  |        | `FK`, `NOT NULL` |
    | `DadoAtaque`          | Número do dado de ataque                     | Varchar  | 3      | `NOT NULL`       |
    | `ChanceCrítico`       | Número da chance de dano crítico             | Float    |        | `NOT NULL`       | 
    | `Multiplicador`       | Número do multiplicador de dano              | Integer  |        | `NOT NULL`       |
    | `MultiplicadorCrítico`| Número do multiplicador de dano crítico      | Integer  |        | `NOT NULL`       |
    | `Alcance`             | Alcance da arma                              | Integer  |        | `NOT NULL`       |
    | `TipoArma`            | Tipo de arma                                 | Varchar  | 15     | `NOT NULL`       |

??? info "Tabela ARMADURA | 1.0v"
    **Nome da Tabela:** Armadura <br/>
    **Descrição**: Armazena as informações dos itens tipo armadura <br/>

    | Atributo           | Descrição                                                      | Tipo     | Limite | Restrições       |
    | ------------------ | -------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdItem`           | Referência à Tabela "Item"                                     | Integer  |        | `FK`, `NOT NULL` |
    | `DadoDefesa`       | Número do dado de defesa                                       | Varchar  | 3      | `NOT NULL`       |
    | `DefesaPassiva`    | Número de defesa passiva da armadura                           | Integer  |        | `NOT NULL`       |
    | `CríticoDefensivo` | Valor mínimo no dado para ganhar um bônus de defesa            | Integer  |        | `NOT NULL`       |
    | `BonusDefesa`      | Valor atribuído à defesa passiva, aumentando a defesa total    | Integer  |        | `NOT NULL`       |
    | `TipoArmadura`     | Tipo de armadura                                               | Varchar  | 15     | `NOT NULL`       |

??? info "Tabela POÇÃO | 1.0v"
    **Nome da Tabela:** Poção <br/>
    **Descrição**: Armazena as informações dos itens tipo poção <br/>

    | Atributo         | Descrição                                      | Tipo     | Limite | Restrições       |
    | ---------------- | ---------------------------------------------- | -------- | ------ | ---------------- |
    | `IdItem`         | Referência à Tabela "Item"                     | Integer  |        | `FK`, `NOT NULL` |
    | `DuraçãoTurnos`  | Duração de turnos de efeito da poção           | Integer  |        | `NOT NULL`       |

??? info "Tabela INST_ITEM | 1.0v"
    **Nome da Tabela:** Inst_Item <br/>
    **Descrição**: Armazena as informações das instâncias dos itens <br/>

    | Atributo       | Descrição                                                    | Tipo     | Limite | Restrições   |
    | -------------- | ------------------------------------------------------------ | -------- | ------ | ------------ |
    | `IdItem`       | Referência à Tabela "Item"                                   | Integer  |        | `PK`, `FK`   |
    | `Quantidade`   | Quantidade em _stack_ do item                                | Integer  |        | `NOT NULL`   |
    | `IdMonstro`    | Referência à Tabela "Inst_Monstro" que está com o item       | Integer  |        | `FK`         |
    | `IdInventário` | Referência à Tabela "Inst_Inventário" em que está o item     | Integer  |        | `FK`         |
    | `IdLojaNPC`    | Referência à Tabela "LojaNPC" em que está o item             | Integer  |        | `FK`         |
    | `SeedSala`     | Referência à Tabela "Sala" que contém o item                 | Integer  |        | `FK`         |
    | `NickName`     | Referência à Tabela "LojaJogador" que contém o item          | Integer  |        | `FK`         |

??? info "Tabela MONSTRO_ITEM | 1.0v"
    **Nome da Tabela:** Monstro_Item <br/>
    **Descrição**: Armazena as informações de Itens que Monstros podem deixar cair <br/>

    | Atributo     | Descrição                                                                                  | Tipo     | Limite | Restrições       |
    | ------------ | ------------------------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `IdMonstro`  | Referência à Tabela "Monstro"                                                              | Integer  |        | `FK`, `NOT NULL` |
    | `IdItem`     | Referência à Tabela "Item"                                                                 | Integer  |        | `FK`, `NOT NULL` |
    | `ChanceDrop` | Número da chance do monstro deixar cair um item                                            | Float    |        | `NOT NULL`       |
    | `QtdMinima`  | Quantidade mínima em _stack_ do "IdItem" que o monstro "IdMonstro" precisa deixar cair     | Integer  |        | `NOT NULL`       |
    | `QtdMaxima`  | Quantidade máxima em _stack_ do "IdItem" que o monstro "IdMonstro" pode deixar cair        | Integer  |        | `NOT NULL`       |

??? info "Tabela EFEITO | 1.0v"
    **Nome da Tabela:** Efeito <br/>
    **Descrição**: Armazena as informações dos efeitos dos itens ou jogador <br/>

    | Atributo         | Descrição                                            | Tipo     | Limite | Restrições      |
    | ---------------- | ---------------------------------------------------- | -------- | ------ | --------------- |
    | `IdEfeito`       | Número de identificação do efeito                    | Integer  |        | `PK`, `IDENTITY`|
    | `Nome`           | Nome do efeito                                       | Varchar  | 30     | `NOT NULL`      |
    | `Descrição`      | Descrição do efeito                                  | Varchar  | 100    | `NOT NULL`      |
    | `Tipo`           | Tipo do efeito                                       | Varchar  | 15     | `NOT NULL`      |
    | `Valor`          | Quantificação de impacto do efeito                   | Integer  |        | `NOT NULL`      |
    | `DuraçãoTurnos`  | Duração de turnos do efeito                          | Integer  |        | `NOT NULL`      |

??? info "Tabela RECEITA | 1.0v"
    **Nome da Tabela:** Receita <br/>
    **Descrição**: Armazena as informações das receitas para se fabricar um item <br/>

    | Atributo    | Descrição                                                       | Tipo     | Limite | Restrições       |
    | ----------- | --------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdItem`    | Referência à Tabela "Item", identificando o item Fabricado      | Integer  |        | `FK`, `NOT NULL` |
    | `IdItem`    | Referência à Tabela "Item", identificando o item Fabricador     | Integer  |        | `FK`, `NOT NULL` |
    | `Quantidade`| Quantidade de itens em _stack_ necessários para fabricar o item | Integer  |        | `NOT NULL`       |

??? info "Tabela JOGADOR | 1.0v"
    **Nome da Tabela:** Jogador <br/>
    **Descrição**: Armazena as informações do jogador <br/>

    | Atributo   | Descrição                                                                      | Tipo     | Limite | Restrições |
    | ---------- | ------------------------------------------------------------------------------ | -------- | ------ | ---------- |
    | `Nickname` | Nome único do jogador                                                          | Varchar  | 60     | `PK`       |
    | `MaxHP`    | Número máximo de vida do jogador                                               | Integer  |        | `NOT NULL` |
    | `AtualHP`  | Vida atual do jogador                                                          | Integer  |        | `NOT NULL` |
    | `Ouro`     | Quantidade de Ouro do jogador                                                  | Interger |        | `NOT NULL` |
    | `IdEfeito` | Referência à Tabela "Efeito", identificando se o jogador está sob algum efeito | Integer  |        | `FK`       |

??? info "Tabela LOJAJOGADOR | 1.0v"
    **Nome da Tabela:** LojaJogador <br/>
    **Descrição**: Armazena as informações da loja do jogador <br/>

    | Atributo           | Descrição                                                                    | Tipo     | Limite | Restrições       |
    | ------------------ | ---------------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `NickName`         | Referência à Tabela "Jogador", identificando a qual jogador a loja pertence  | Varchar  | 60     | `PK`, `FK`       |
    | `Nível`            | Nível da loja do jogador                                                     | Integer  |        | `NOT NULL`       |
    | `ExposiçãoMáxima`  | Número máximo de itens que podem ser expostos na loja do jogador             | Integer  |        | `NOT NULL`       |
    | `ExposiçãoUsada`   | Número de itens atualmente expostos na loja do jogador                       | Integer  |        | `NOT NULL`       |
    | `IdMapa`           | Número de identificação do mapa do mundo                                     | Integer  |        | `FK`, `NOT NULL` |

??? info "Tabela INST_INVENTARIO | 1.0v"
    **Nome da Tabela:** Inventário <br/>
    **Descrição**: Armazena as informações de tipos de inventários existentes no jogo <br/>

    | Atributo       | Descrição                                             | Tipo     | Limite | Restrições       |
    | -------------- | ----------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdInventário` | Número de identificação do inventário                 | Integer  |        | `PK`, `IDENTITY` |
    | `Nome`         | Nome do inventário                                    | Varchar  | 30     | `NOT NULL`       |
    | `SlotMáximo`   | Quantidade máxima de armazenamento de itens           | Integer  |        | `NOT NULL`       |

??? info "Tabela INST_INVENTARIO | 1.0v"
    **Nome da Tabela:** Inst_Inventario <br/>
    **Descrição**: Armazena as informações das instâncias de inventário dos jogadores <br/>

    | Atributo       | Descrição                                                                            | Tipo     | Limite | Restrições       |
    | -------------- | ------------------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `IdInventário` | Referência à Tabela "Inventário", indicando qual o tipo de inventário                | Integer  |        | `PK`, `FK`       |
    | `SlotOcupado`  | Quantidade de lugares do inventário ocupados                                         | Integer  |        | `NOT NULL`       |
    | `Nickname`     | Referência à Tabela "Jogador", indicando à qual jogador esta instância pertence      | Varchar  | 60     | `FK`, `NOT NULL` |

??? info "Tabela NPC | 1.0v"
    **Nome da Tabela:** NPC <br/>
    **Descrição**: Armazena as informações dos NPCs  <br/>

    | Atributo    | Descrição                                         | Tipo     | Limite | Restrições       |
    | ----------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdNPC`     | Número de identificação do NPC                    | Integer  |        | `PK`, `IDENTITY` |
    | `Nome`      | Nome do NPC                                       | Varchar  | 30     | `NOT NULL`       |
    | `TipoNPC`   | Tipo de NPC                                       | Varchar  | 30     | `NOT NULL`       |
    | `Descrição` | Descrição do NPC                                  | Varchar  | 60     | `NOT NULL`       |
    | `Ativo`     | O NPC está interagindo com o jogador?             | Boolean  |        | `NOT NULL`       |


??? info "Tabela LOJANPC | 1.0v"
    **Nome da Tabela:** LojaNPC <br/>
    **Descrição**: Armazena as informações da loja do NPC <br/>

    | Atributo     | Descrição                                                                | Tipo     | Limite | Restrições       |
    | ------------ | ------------------------------------------------------------------------ | -------- | ------ | ---------------- |
    | `IdLojaNPC`  | Número de identificação da loja do NPC                                   | Integer  |        | `PK`, `IDENTITY` |
    | `Nome`       | Nome da loja do NPC                                                      | Varchar  | 30     | `NOT NULL`       |
    | `TipoLoja`   | Tipo da loja do NPC                                                      | Varchar  | 30     | `NOT NULL`       |
    | `Descrição`  | Descrição da loja do NPC                                                 | Varchar  | 120    | `NOT NULL`       |
    | `Status`     | A loja está em uso pelo jogador?                                         | Boolean  |        | `NOT NULL`       |
    | `IdNPC`      | Referência à Tabela "NPC", indicando qual NPC cuida da loja              | Integer  |        | `FK`, `NOT NULL` |
    | `IdMapa`     | Referência à Tabela "Mapa", indicando a qual mapa a loja pertence        | Integer  |        | `FK`, `NOT NULL` |

??? info "Tabela FORJARIA | 1.0v"
    **Nome da Tabela:** Forjaria <br/>
    **Descrição**: Armazena as informações da loja do NPC tipo forjaria <br/>

    | Atributo     | Descrição                                  | Tipo     | Limite | Restrições       |
    | ------------ | ------------------------------------------ | -------- | ------ | ---------------- |
    | `IdLojaNPC`  | Referência à Tabela "LojaNPC"              | Integer  |        | `FK`, `NOT NULL` |


??? info "Tabela VAREJO | 1.0v"
    **Nome da Tabela:** Varejo <br/>
    **Descrição**: Armazena as informações da loja do NPC tipo varejo <br/>

    | Atributo      | Descrição                                         | Tipo     | Limite | Restrições       |
    | ------------- | ------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdLojaNPC`   | Referência à Tabela "LojaNPC"                     | Integer  |        | `FK`, `NOT NULL` |
    | `MargemLucro` | Margem de lucro dos itens do NPC                  | Interger |        | `NOT NULL`       |

??? info "Tabela BANCO | 1.0v"
    **Nome da Tabela:** Banco <br/>
    **Descrição**: Armazena as informações da loja do NPC tipo banco <br/>

    | Atributo        | Descrição                                               | Tipo     | Limite | Restrições       |
    | --------------- | ------------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdLojaNPC`     | Referência à Tabela "LojaNPC"                           | Integer  |        | `FK`, `NOT NULL` |
    | `ValorEntrada`  | Valor do ouro de entrada depositado pelo jogador        | Integer  |        |                  |
    | `ValorAtual`    | Valor atual do ouro com rendimento do jogador           | Integer  |        | `NOT NULL`       |

??? info "Tabela DIÁLOGO | 1.0v"
    **Nome da Tabela:** Diálogo <br/>
    **Descrição**: Armazena as informações de cada diálogo possível <br/>

    | Atributo      | Descrição                                                                             | Tipo     | Limite | Restrições       |
    | ------------- | ------------------------------------------------------------------------------------- | -------- | ------ | ---------------- |
    | `IdDiálogo`   | Número de identificação do diálogo                                                    | Integer  |        | `PK`, `IDENTITY` |
    | `Conteúdo`    | Conteúdo do diálogo                                                                   | Varchar  | 300    | `NOT NULL`       |
    | `Ordem`       | Ordem do diálogo                                                                      | Integer  |        | `NOT NULL`       |
    | `Tipo`        | Tipo de diálogo                                                                       | Varchar  | 60     | `NOT NULL`       |
    | `IdDialogo`   | Referência à Tabela "Diálogo", indicando se este diálogo procede após um diálogo pai  | Integer  |        | `FK`             |

??? info "Tabela DIÁLOGO_NPC | 1.0v"
    **Nome da Tabela:** Diálogo_NPC <br/>
    **Descrição**: Armazena o conjunto de Diálogos que NPC's podem possuir <br/>

    | Atributo     | Descrição                                | Tipo     | Limite | Restrições       |
    | ------------ | ---------------------------------------- | -------- | ------ | ---------------- |
    | `IdDiálogo`  | Referência à Tabela "Diálogo"            | Integer  |        | `FK`, `NOT NULL` |
    | `IdNPC`      | Referência à Tabela "NPC"                | Integer  |        | `FK`, `NOT NULL` |

---

# Bibliografia

> <p><small>CONTENT STUDIO. O que é um dicionário de dados? Disponível em: <a href="https://www.purestorage.com/br/knowledge/what-is-a-data-dictionary.html">https://www.purestorage.com/br/knowledge/what-is-a-data-dictionary.html</a>. Acesso em: 30 abr. 2025.</small></p>

‌

# Versão:

| Data       | Versão | Autor(es)          | Mudanças                                                              |
| ---------- | ------ | ------------------ | --------------------------------------------------------------------- |
| 30/04/2025 | `1.0`  | Daniel Rodrigues   | Adição do Tópico "O que é um dicionário de dados?"                    |
| 01/05/2025 | `1.1`  | Yan Matheus        | Adição das tabelas do dicionário de dados                             |
| 01/05/2025 | `1.2`  | Daniel Rodrigues   | Reorganização das Tabelas e Adição das Restrições                     |
| 23/05/2025 | `1.3`  | Yan Matheus        | Reorganização das Tabelas e correção das Restrições                   |
| 24/05/2025 | `1.4`  | Daniel Rodrigues   | Separação das diferentes versões do Dicionário e correções Pontuais   |
| 24/05/2025 | `1.5`  | Daniel Rodrigues   | Atualização de atributos                                              |
| 01/06/2025 | `1.6`  | Arthur Evangelista | Atualização do tamanho da descrição na Tabela NPC.                    |
| 11/06/2025 | `2.0`  | Daniel Rodrigues   | Atualização do Novo Dicionário de Dados                               |
| 08/08/2025 | `2.1`  | Yan Matheus        | Atualização do ouro do jogador                                        |
