-- CONFIG DO DATABASE
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

-- ZERAR O SCHEMA
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- CRIACAO DE TABELAS
CREATE TABLE "masmorra" (
    "nomeMasmorra" character varying(30) PRIMARY KEY,
    "descricao" character varying(100) NOT NULL,
    "nivel" SMALLINT NOT NULL,
    "qtdAndar" SMALLINT NOT NULL
);


CREATE TABLE "inst_masmorra" (
    "nomeMasmorra" character varying(30),
    "seedMasmorra" character varying(10) UNIQUE,
    "posicaoX_Jogador" integer NOT NULL,
    "posicaoY_Jogador" integer NOT NULL,

    CONSTRAINT "fk_masmorra" FOREIGN KEY ("nomeMasmorra") REFERENCES "masmorra" ("nomeMasmorra") ON DELETE CASCADE,
    CONSTRAINT "pk_inst_masmorra" PRIMARY KEY ("nomeMasmorra", "seedMasmorra")
);


CREATE TABLE "sala" (
    "seedSala" character varying(10) PRIMARY KEY,
    "posicaoX" integer NOT NULL,
    "posicaoY" integer NOT NULL,
    "categoria" character varying(60) NOT NULL,
    "nomeMasmorra" character varying(30) NOT NULL,

    CONSTRAINT "fk_inst_masmorra" FOREIGN KEY ("nomeMasmorra") REFERENCES "masmorra" ("nomeMasmorra") ON DELETE CASCADE
);


CREATE TABLE "sala_inst_masmorra" (
    "seedSala" character varying(10) NOT NULL,
    "seedMasmorra" character varying(10) NOT NULL,
    "explorada" boolean NOT NULL,

    CONSTRAINT "fk_sala" FOREIGN KEY ("seedSala") REFERENCES "sala" ("seedSala") ON DELETE CASCADE,
    CONSTRAINT "fk_inst_masmorra" FOREIGN KEY ("seedMasmorra") REFERENCES "inst_masmorra" ("seedMasmorra") ON DELETE CASCADE
);


CREATE TABLE "mapa" (
    "idMapa" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "periodo" character varying(8) NOT NULL,
    "dia" integer NOT NULL
);


CREATE TABLE "masmorra_mapa" (
    "nomeMasmorra" character varying(30) NOT NULL,
    "idMapa" integer NOT NULL,
    "desbloqueado" boolean NOT NULL,

    CONSTRAINT "fk_masmorra" FOREIGN KEY ("nomeMasmorra") REFERENCES "masmorra" ("nomeMasmorra") ON DELETE CASCADE,
    CONSTRAINT "fk_mapa" FOREIGN KEY ("idMapa") REFERENCES "mapa" ("idMapa") ON DELETE CASCADE
);


CREATE TABLE "efeito" (
    "idEfeito" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "descricao" character varying(100) NOT NULL,
    "tipo" character varying(15) NOT NULL,
    "valor" SMALLINT NOT NULL,
    "duracaoTurnos" SMALLINT
);


CREATE TABLE "monstro" (
    "idMonstro" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "descricao" character varying(100) NOT NULL,
    "nivel" SMALLINT NOT NULL,
    "vidaMaxima" SMALLINT NOT NULL,
    "ouroDropado" SMALLINT NOT NULL,
    "dadoAtaque" character varying(3) NOT NULL,
    "chanceCritico" REAL NOT NULL,
    "multiplicador" SMALLINT NOT NULL,
    "multiplicadorCritico" SMALLINT NOT NULL,
    "chefe" boolean NOT NULL,
    "nomeMasmorra" character varying(60) NOT NULL,
    "idEfeito" integer,

    CONSTRAINT "fk_masmorra" FOREIGN KEY ("nomeMasmorra") REFERENCES "masmorra" ("nomeMasmorra") ON DELETE CASCADE,
    CONSTRAINT "fk_efeito" FOREIGN KEY ("idEfeito") REFERENCES "efeito" ("idEfeito") ON DELETE CASCADE
);


CREATE TABLE "inst_monstro" (
    "seedMonstro" CHARACTER varying(10) UNIQUE,
    "idMonstro" integer,
    "vidaAtual" SMALLINT NOT NULL,
    "status" integer NOT NULL,
    "seedSala" character varying(10) NOT NULL,

    CONSTRAINT "pk_inst_monstro" PRIMARY KEY ("seedMonstro", "idMonstro"),
    CONSTRAINT "fk_monstro" FOREIGN KEY ("idMonstro") REFERENCES "monstro" ("idMonstro") ON DELETE CASCADE,
    CONSTRAINT "fk_sala" FOREIGN KEY ("seedSala") REFERENCES "sala" ("seedSala") ON DELETE CASCADE
);


CREATE TABLE "item" (
    "idItem" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(80) NOT NULL,
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


CREATE TABLE "jogador" (
    "nickName" character varying(60) PRIMARY KEY,
    "maxHP" SMALLINT NOT NULL,
    "atualHP" SMALLINT NOT NULL,
    "ouro" SMALLINT NOT NULL,
    "idEfeito" integer,

    CONSTRAINT "fk_efeito" FOREIGN KEY ("idEfeito") REFERENCES "efeito" ("idEfeito") ON DELETE CASCADE
);


CREATE TABLE "lojaJogador" (
    "nickName" character varying(60) PRIMARY KEY,
    "nivel" SMALLINT NOT NULL,
    "exposicaoMaxima" SMALLINT NOT NULL,
    "exposicaoUsada" SMALLINT NOT NULL,
    "idMapa" integer NOT NULL,

    CONSTRAINT "fk_jogador" FOREIGN KEY ("nickName") REFERENCES "jogador" ("nickName") ON DELETE CASCADE,
    CONSTRAINT "fk_mapa" FOREIGN KEY ("idMapa") REFERENCES "mapa" ("idMapa") ON DELETE CASCADE
);


CREATE TABLE "inventario" (
    "idInventario" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "slotMaximo" SMALLINT NOT NULL
);

-- REVISAR ESSA TABELA
CREATE TABLE "inst_inventario" (
    "idInventario" integer PRIMARY KEY,
    "nickname" character varying(60) NOT NULL,
    "slotOcupado" integer NOT NULL,

    CONSTRAINT "fk_inventario" FOREIGN KEY ("idInventario") REFERENCES "inventario" ("idInventario") ON DELETE CASCADE,
    CONSTRAINT "fk_jogador" FOREIGN KEY ("nickname") REFERENCES "jogador" ("nickName") ON DELETE CASCADE
);


CREATE TABLE "npc" (
    "idNPC" integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "nome" character varying(60) NOT NULL,
    "tipoNPC" character varying(30) NOT NULL,
    "descricao" character varying(60) NOT NULL,
    "ativo" boolean NOT NULL
);


CREATE TABLE "lojaNPC" (
    "idLojaNPC" integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "tipoLoja" character varying(30) NOT NULL,
    "descricao" character varying(120) NOT NULL,
    "status" boolean NOT NULL,
    "idNPC" integer NOT NULL,
    "idMapa" integer NOT NULL,

    CONSTRAINT "fk_npc" FOREIGN KEY ("idNPC") REFERENCES "npc" ("idNPC") ON DELETE CASCADE,
    CONSTRAINT "fk_mapa" FOREIGN KEY ("idMapa") REFERENCES "mapa" ("idMapa") ON DELETE CASCADE
);


CREATE TABLE "forjaria" (
    "idLojaNPC" integer PRIMARY KEY,

    CONSTRAINT "fk_lojaNPC" FOREIGN KEY ("idLojaNPC") REFERENCES "lojaNPC" ("idLojaNPC") ON DELETE CASCADE
);


CREATE TABLE "varejo" (
    "idLojaNPC" integer PRIMARY KEY,
    "margemLucro" SMALLINT NOT NULL,

    CONSTRAINT "fk_lojaNPC" FOREIGN KEY ("idLojaNPC") REFERENCES "lojaNPC" ("idLojaNPC") ON DELETE CASCADE
);


CREATE TABLE "banco" (
    "idLojaNPC" integer PRIMARY KEY,
    "valorEntrada" SMALLINT,
    "valorAtual" SMALLINT NOT NULL,

    CONSTRAINT "fk_lojaNPC" FOREIGN KEY ("idLojaNPC") REFERENCES "lojaNPC" ("idLojaNPC") ON DELETE CASCADE
);


CREATE TABLE "inst_item" (
    "idItem" integer PRIMARY KEY,
    "quantidade" SMALLINT NOT NULL,
    "seedMonstro" character varying(10),
    "idInventario" integer,
    "idLojaNPC" integer,
    "seedSala" character varying(10),
    "nickName" character varying(60),

    CONSTRAINT "fk_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE,
    CONSTRAINT "fk_inst_monstro" FOREIGN KEY ("seedMonstro") REFERENCES "inst_monstro" ("seedMonstro") ON DELETE CASCADE,
    CONSTRAINT "fk_inst_inventario" FOREIGN KEY ("idInventario") REFERENCES "inst_inventario" ("idInventario") ON DELETE CASCADE,
    CONSTRAINT "fk_lojaNPC" FOREIGN KEY ("idLojaNPC") REFERENCES "lojaNPC" ("idLojaNPC") ON DELETE CASCADE,
    CONSTRAINT "fk_sala" FOREIGN KEY ("seedSala") REFERENCES "sala" ("seedSala") ON DELETE CASCADE,
    CONSTRAINT "fk_lojaJogador" FOREIGN KEY ("nickName") REFERENCES "lojaJogador" ("nickName") ON DELETE CASCADE
);


CREATE TABLE "dialogo" (
    "idDialogo" integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "conteudo" character varying(300) NOT NULL,
    "ordem" SMALLINT NOT NULL,
    "tipo" character varying(60) NOT NULL,
    "idDialogoPai" integer,

    CONSTRAINT "fk_dialogo" FOREIGN KEY ("idDialogoPai") REFERENCES "dialogo" ("idDialogo") ON DELETE CASCADE
);


CREATE TABLE "dialogo_npc" (
    "idDialogo" integer NOT NULL,
    "idNPC" integer NOT NULL,

    CONSTRAINT "fk_dialogo" FOREIGN KEY ("idDialogo") REFERENCES "dialogo" ("idDialogo") ON DELETE CASCADE,
    CONSTRAINT "fk_npc" FOREIGN KEY ("idNPC") REFERENCES "npc" ("idNPC") ON DELETE CASCADE
);