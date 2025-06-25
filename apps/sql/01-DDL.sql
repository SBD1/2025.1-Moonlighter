-- ---------------------------------------------------------------------------------------------------------------
-- Data de Criação ........: 09/06/2025                                                                         --
-- Autor(es) ..............: Yan Matheus, João Pedro                                                            --
-- Versão .................: 2.0                                                                                --
-- Banco de Dados .........: PostgreSQL                                                                         --
-- Descrição ..............: Criação das tabelas para o jogo Moonlighter                                        --
-- ---------------------------------------------------------------------------------------------------------------

-- CONFIG DO DATABASE
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

-- ZERAR O SCHEMA
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- CRIACAO DE TABELAS
CREATE TABLE "local" (
    "nomeLocal" CHARACTER varying(60) PRIMARY KEY,
    "descricao" CHARACTER varying(200) NOT NULL,
    "tipoLocal" CHARACTER varying(20) NOT NULL,
    "acesso" CHARACTER varying(60),

    CONSTRAINT "fk_local" FOREIGN KEY ("acesso") REFERENCES "local" ("nomeLocal") ON DELETE SET NULL,
    CONSTRAINT "ck_tipo_local" CHECK (
        "tipoLocal" IN ('Local', 'Masmorra', 'Estabelecimento')
    )
);

CREATE TABLE "efeito" (
    "idEfeito" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "descricao" character varying(100) NOT NULL,
    "tipo" character varying(15) NOT NULL,
    "valor" SMALLINT NOT NULL,
    "duracaoTurnos" SMALLINT
);

CREATE TABLE "jogador" (
    "nickname" character varying(60) PRIMARY KEY,
    "maxHP" SMALLINT NOT NULL,
    "atualHP" SMALLINT NOT NULL,
    "ouro" SMALLINT NOT NULL,
    "PosiçãoX_Jogador" SMALLINT NOT NULL,
    "PosiçãoY_Jogador" SMALLINT NOT NULL,
    "nomeLocal" CHARACTER varying(60) NOT NULL,
    "idEfeito" integer,

    CONSTRAINT "fk_efeito" FOREIGN KEY ("idEfeito") REFERENCES "efeito" ("idEfeito") ON DELETE CASCADE,
    CONSTRAINT "fk_local" FOREIGN KEY ("nomeLocal") REFERENCES "local" ("nomeLocal") ON DELETE CASCADE
);

CREATE TABLE "mundo" (
    "seedMundo" character varying(30) PRIMARY KEY,
    "nickname" character varying(60) NOT NULL,
    "periodo" character varying(8) NOT NULL,
    "dia" integer NOT NULL,
    "nivelMundo" SMALLINT NOT NULL,

    CONSTRAINT "fk_jogador" FOREIGN KEY ("nickname") REFERENCES "jogador" ("nickname") ON DELETE CASCADE
);

CREATE TABLE "masmorra" (
    "nomeLocal" character varying(60) PRIMARY KEY,
    "nivelDesbloqueio" SMALLINT NOT NULL,
    "dificuldade" character varying(7) NOT NULL,
    "qtdAndar" SMALLINT NOT NULL,

    CONSTRAINT "fk_local" FOREIGN KEY ("nomeLocal") REFERENCES "local" ("nomeLocal") ON DELETE CASCADE
);

CREATE TABLE "estabelecimento" (
    "nomeLocal" character varying(60) PRIMARY KEY,

    CONSTRAINT "fk_local" FOREIGN KEY ("nomeLocal") REFERENCES "local" ("nomeLocal") ON DELETE CASCADE
);

CREATE TABLE "inst_masmorra" (
    "seedMundo" CHARACTER varying(30) NOT NULL,
    "seedMasmorra" character varying(30) NOT NULL,
    "nomeLocal" character varying(60) NOT NULL,
    "ativo" BOOLEAN NOT NULL,

    CONSTRAINT "fk_masmorra" FOREIGN KEY ("nomeLocal") REFERENCES "masmorra" ("nomeLocal") ON DELETE CASCADE,
    CONSTRAINT "pk_inst_masmorra" PRIMARY KEY ("seedMundo", "seedMasmorra")
);


CREATE TABLE "sala" (
    "seedSala" character varying(30) PRIMARY KEY,
    "posicaoX" integer NOT NULL,
    "posicaoY" integer NOT NULL,
    "categoria" character varying(60) NOT NULL,
    "seedMundo" character varying(30) NOT NULL,
    "seedMasmorra" character varying(30) NOT NULL,
    "nomeLocal" character varying(60) NOT NULL,

    CONSTRAINT "fk_inst_masmorra" FOREIGN KEY ("seedMasmorra", "seedMundo") REFERENCES "inst_masmorra" ("seedMasmorra", "seedMundo") ON DELETE CASCADE,
    CONSTRAINT "fk_masmorra" FOREIGN KEY ("nomeLocal") REFERENCES "masmorra" ("nomeLocal") ON DELETE CASCADE
);

CREATE TABLE "monstro" (
    "idMonstro" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "descricao" character varying(100) NOT NULL,
    "nivel" SMALLINT NOT NULL,
    "vidaMaxima" SMALLINT NOT NULL,
    "ouroDropado" SMALLINT NOT NULL,
    "dadoAtaque" character varying(4) NOT NULL,
    "chanceCritico" REAL NOT NULL,
    "multiplicador" SMALLINT NOT NULL,
    "multiplicadorCritico" SMALLINT NOT NULL,
    "chefe" boolean NOT NULL,
    "nomeLocal" character varying(60) NOT NULL,
    "idEfeito" integer,

    CONSTRAINT "fk_masmorra" FOREIGN KEY ("nomeLocal") REFERENCES "masmorra" ("nomeLocal") ON DELETE CASCADE,
    CONSTRAINT "fk_efeito" FOREIGN KEY ("idEfeito") REFERENCES "efeito" ("idEfeito") ON DELETE CASCADE
);


CREATE TABLE "inst_monstro" (
    "seedMundo" CHARACTER varying(30),
    "idMonstro" integer,
    "vidaAtual" SMALLINT NOT NULL,
    "status" integer NOT NULL,
    "seedSala" character varying(30) NOT NULL,

    CONSTRAINT "pk_inst_monstro" PRIMARY KEY ("seedMundo", "idMonstro"),
    CONSTRAINT "fk_mundo" FOREIGN KEY ("seedMundo") REFERENCES "mundo" ("seedMundo") ON DELETE CASCADE,
    CONSTRAINT "fk_monstro" FOREIGN KEY ("idMonstro") REFERENCES "monstro" ("idMonstro") ON DELETE CASCADE,
    CONSTRAINT "fk_sala" FOREIGN KEY ("seedSala") REFERENCES "sala" ("seedSala") ON DELETE CASCADE
);


CREATE TABLE "item" (
    "idItem" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(80) UNIQUE NOT NULL,
    "descricao" character varying(500) NOT NULL,
    "tipo" character varying(15),
    "precoBase" INTEGER NOT NULL,
    "cultura" CHARACTER varying(10) NOT NULL,
    "stackMaximo" SMALLINT NOT NULL,
    "idEfeito" integer,

    CONSTRAINT "fk_efeito" FOREIGN KEY ("idEfeito") REFERENCES "efeito" ("idEfeito") ON DELETE CASCADE
);


CREATE TABLE "arma" (
    "idItem" integer PRIMARY KEY,
    "dadoAtaque" character varying(3) NOT NULL,
    "chanceCritico" real NOT NULL,
    "multiplicador" SMALLINT NOT NULL,
    "multiplicadorCritico" SMALLINT NOT NULL,
    "tipoArma" character varying(15) NOT NULL,

    CONSTRAINT "fk_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE
);


CREATE TABLE "armadura" (
    "idItem" integer PRIMARY KEY,
    "dadoDefesa" character varying(3) NOT NULL,
    "defesaPassiva" SMALLINT NOT NULL,
    "criticoDefensivo" SMALLINT NOT NULL,
    "bonusDefesa" SMALLINT NOT NULL,
    "tipoArmadura" character varying(15) NOT NULL,

    CONSTRAINT "fk_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE
);


CREATE TABLE "pocao" (
    "idItem" integer PRIMARY KEY,
    "duracaoTurnos" SMALLINT NOT NULL,

    CONSTRAINT "fk_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE
);


CREATE TABLE "monstro_item" (
    "idMonstro" integer NOT NULL,
    "idItem" integer NOT NULL,
    "chanceDrop" real NOT NULL,
    "qtdMinima" SMALLINT NOT NULL,
    "qtdMaxima" SMALLINT NOT NULL,

    CONSTRAINT "fk_monstro" FOREIGN KEY ("idMonstro") REFERENCES "monstro" ("idMonstro") ON DELETE CASCADE,
    CONSTRAINT "fk_monstrp" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE
);


CREATE TABLE "receita" (
    "idItemFabricado" integer NOT NULL,
    "idItemFabricador" integer NOT NULL,
    "quantidade" SMALLINT NOT NULL,

    CONSTRAINT "fk_itemResultado" FOREIGN KEY ("idItemFabricado") REFERENCES "item" ("idItem") ON DELETE CASCADE,
    CONSTRAINT "fk_item" FOREIGN KEY ("idItemFabricador") REFERENCES "item" ("idItem") ON DELETE CASCADE
);


CREATE TABLE "loja_jogador" (
    "seedMundo" CHARACTER varying(30) PRIMARY KEY,
    "nomeLocal" character varying(60),
    "nivel" SMALLINT NOT NULL,
    "exposicaoMaxima" SMALLINT NOT NULL,
    "exposicaoUsada" SMALLINT NOT NULL,
    
    CONSTRAINT "fk_mundo" FOREIGN KEY ("seedMundo") REFERENCES "mundo" ("seedMundo") ON DELETE CASCADE,
    CONSTRAINT "fk_estabelecimento" FOREIGN KEY ("nomeLocal") REFERENCES "estabelecimento" ("nomeLocal") ON DELETE CASCADE
);


CREATE TABLE "inventario" (
    "idInventario" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "slotMaximo" SMALLINT NOT NULL
);

-- REVISAR ESSA TABELA
CREATE TABLE "inst_inventario" (
    "idInventario" integer,
    "nickname" character varying(60) NOT NULL,
    "slotOcupado" integer NOT NULL,

    CONSTRAINT "fk_inventario" FOREIGN KEY ("idInventario") REFERENCES "inventario" ("idInventario") ON DELETE CASCADE,
    CONSTRAINT "fk_jogador" FOREIGN KEY ("nickname") REFERENCES "jogador" ("nickname") ON DELETE CASCADE,
    CONSTRAINT "pk_inst_inventario" PRIMARY KEY ("idInventario", "nickname")
);


CREATE TABLE "npc" (
    "idNPC" integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "nome" character varying(60) NOT NULL,
    "tipoNPC" character varying(30) NOT NULL,
    "descricao" character varying(100) NOT NULL,
    "ativo" boolean NOT NULL
);

CREATE TABLE "inst_forja" (
    "seedMundo" character varying(30) PRIMARY KEY,
    "nomeLocal" character varying(60) NOT NULL,
    "idNPC" integer NOT NULL,

    CONSTRAINT "fk_mundo" FOREIGN KEY ("seedMundo") REFERENCES "mundo" ("seedMundo") ON DELETE CASCADE,
    CONSTRAINT "fk_estabelecimento" FOREIGN KEY ("nomeLocal") REFERENCES "estabelecimento" ("nomeLocal") ON DELETE CASCADE,
    CONSTRAINT "fk_npc" FOREIGN KEY ("idNPC") REFERENCES "npc" ("idNPC") ON DELETE CASCADE
);

CREATE TABLE "inst_forja_item" (
    "idItem" integer NOT NULL,
    "seedMundo" character varying(10) NOT NULL,

    CONSTRAINT "fk_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE,
    CONSTRAINT "fk_inst_item" FOREIGN KEY ("seedMundo") REFERENCES "inst_forja" ("seedMundo") ON DELETE CASCADE
);


CREATE TABLE "inst_varejo" (
    "seedMundo" character varying(30) PRIMARY KEY,
    "nomeLocal" character varying(60) NOT NULL,
    "idNPC" integer NOT NULL,
    "margemLucro" SMALLINT NOT NULL,

    CONSTRAINT "fk_mundo" FOREIGN KEY ("seedMundo") REFERENCES "mundo" ("seedMundo") ON DELETE CASCADE,
    CONSTRAINT "fk_estabelecimento" FOREIGN KEY ("nomeLocal") REFERENCES "estabelecimento" ("nomeLocal") ON DELETE CASCADE,
    CONSTRAINT "fk_npc" FOREIGN KEY ("idNPC") REFERENCES "npc" ("idNPC") ON DELETE CASCADE
);


CREATE TABLE "inst_banco" (
    "seedMundo" character varying(30) PRIMARY KEY,
    "nomeLocal" character varying(60) NOT NULL,
    "idNPC" integer NOT NULL,
    "valorEntrada" SMALLINT NOT NULL,
    "valorAtual" SMALLINT NOT NULL,

    CONSTRAINT "fk_mundo" FOREIGN KEY ("seedMundo") REFERENCES "mundo" ("seedMundo") ON DELETE CASCADE,
    CONSTRAINT "fk_estabelecimento" FOREIGN KEY ("nomeLocal") REFERENCES "estabelecimento" ("nomeLocal") ON DELETE CASCADE,
    CONSTRAINT "fk_npc" FOREIGN KEY ("idNPC") REFERENCES "npc" ("idNPC") ON DELETE CASCADE
);


CREATE TABLE "inst_item" (
    "idItem" integer PRIMARY KEY,
    "quantidade" SMALLINT NOT NULL,

    -- REFERENCIA À TABELA INST_MONSTRO
    "idMonstro" integer,
    "seedMundoInstMonstro" CHARACTER varying(30),
    
    -- REFERENCIA À TABELA INST_INVENTARIO
    "nickname" character varying(60),
    "idInventario" integer,

    -- REFERENCIA À TABELA INST_VAREJO
    "seedMundoInstVarejo" character varying(30),

    -- REFERENCIA À TABELA SALA
    "seedSala" character varying(30),

    -- REFERENCIA À TABELA LOJA_JOGADOR
    "seedMundoLojaJogador" character varying(30),

    CONSTRAINT "fk_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE,
    CONSTRAINT "fk_inst_monstro" FOREIGN KEY ("idMonstro", "seedMundoInstMonstro") REFERENCES "inst_monstro" ("idMonstro", "seedMundo") ON DELETE CASCADE,
    CONSTRAINT "fk_inst_inventario" FOREIGN KEY ("idInventario", "nickname") REFERENCES "inst_inventario" ("idInventario", "nickname") ON DELETE CASCADE,
    CONSTRAINT "fk_inst_varejo" FOREIGN KEY ("seedMundoInstVarejo") REFERENCES "inst_varejo" ("seedMundo") ON DELETE CASCADE,
    CONSTRAINT "fk_sala" FOREIGN KEY ("seedSala") REFERENCES "sala" ("seedSala") ON DELETE CASCADE,
    CONSTRAINT "fk_loja_jogador" FOREIGN KEY ("seedMundoLojaJogador") REFERENCES "loja_jogador" ("seedMundo") ON DELETE CASCADE
);


CREATE TABLE "dialogo" (
    "idDialogo" integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "conteudo" character varying(300) NOT NULL,
    "ordem" SMALLINT NOT NULL,
    "tipo" character varying(60) NOT NULL,
    "idDialogoPai" INTEGER,

    CONSTRAINT "fk_dialogo_pai" FOREIGN KEY ("idDialogoPai") REFERENCES "dialogo" ("idDialogo") ON DELETE SET NULL
);


CREATE TABLE "dialogo_npc" (
    "idDialogo" integer NOT NULL,
    "idNPC" integer NOT NULL,

    CONSTRAINT "fk_dialogo" FOREIGN KEY ("idDialogo") REFERENCES "dialogo" ("idDialogo") ON DELETE CASCADE,
    CONSTRAINT "fk_npc" FOREIGN KEY ("idNPC") REFERENCES "npc" ("idNPC") ON DELETE CASCADE
);