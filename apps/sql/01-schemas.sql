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
    "nivel" integer NOT NULL,
    "qtdAndar" integer NOT NULL
);


CREATE TABLE "inst_masmorra" (
    "nomeMasmorra" character varying(30) PRIMARY KEY,
    "seedMasmorra" character varying(10) UNIQUE NOT NULL,
    "posicaoX_Jogador" integer NOT NULL,
    "posicaoY_Jogador" integer NOT NULL,

    CONSTRAINT "fk_masmorra" FOREIGN KEY ("nomeMasmorra") REFERENCES "masmorra" ("nomeMasmorra") ON DELETE CASCADE
);


CREATE TABLE "sala" (
    "seedSala" character varying(10) PRIMARY KEY,
    "posicaoX" integer NOT NULL,
    "posicaoY" integer NOT NULL,
    "categoria" character varying(60) NOT NULL,
    "explorada" boolean NOT NULL,
    "nomeMasmorra" character varying(30) NOT NULL,

    CONSTRAINT "fk_inst_masmorra" FOREIGN KEY ("nomeMasmorra") REFERENCES "inst_masmorra" ("nomeMasmorra") ON DELETE CASCADE
);


CREATE TABLE "sala_inst_masmorra" (
    "seedSala" character varying(10) NOT NULL,
    "nomeMasmorra" character varying(30) NOT NULL,

    CONSTRAINT "fk_sala" FOREIGN KEY ("seedSala") REFERENCES "sala" ("seedSala") ON DELETE CASCADE,
    CONSTRAINT "fk_inst_masmorra" FOREIGN KEY ("nomeMasmorra") REFERENCES "inst_masmorra" ("nomeMasmorra") ON DELETE CASCADE
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


CREATE TABLE "monstro" (
    "idMonstro" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "descricao" character varying(100) NOT NULL,
    "nivel" integer NOT NULL,
    "vidaMaxima" integer NOT NULL,
    "ouroDropado" integer NOT NULL,
    "dadoAtaque" character varying(3) NOT NULL,
    "chanceCritico" integer NOT NULL,
    "multiplicador" integer NOT NULL,
    "multiplicadorCritico" integer NOT NULL,
    "chefe" boolean NOT NULL,
    "nomeMasmorra" character varying(60) NOT NULL,
    "idEfeito" integer,

    CONSTRAINT "fk_masmorra" FOREIGN KEY ("nomeMasmorra") REFERENCES "masmorra" ("nomeMasmorra") ON DELETE CASCADE,
    CONSTRAINT "fk_efeito" FOREIGN KEY ("idEfeito") REFERENCES "efeito" ("idEfeito") ON DELETE CASCADE
);


CREATE TABLE "inst_monstro" (
    "idMonstro" integer PRIMARY KEY,
    "vidaAtual" integer NOT NULL,
    "status" integer NOT NULL,
    "seedSala" character varying(10) NOT NULL,

    CONSTRAINT "fk_mnstro" FOREIGN KEY ("idMonstro") REFERENCES "monstro" ("idMonstro") ON DELETE CASCADE,
    CONSTRAINT "fk_sala" FOREIGN KEY ("seedSala") REFERENCES "sala" ("seedSala") ON DELETE CASCADE
);


CREATE TABLE "item" (
    "idItem" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "descricao" character varying(60) NOT NULL,
    "tipo" character varying(15) NOT NULL,
    "precoBase" integer NOT NULL,
    "raridade" integer NOT NULL,
    "stackMaximo" integer NOT NULL,
    "idEfeito" integer,

    CONSTRAINT "fk_efeito" FOREIGN KEY ("idEfeito") REFERENCES "efeito" ("idEfeito") ON DELETE CASCADE
);


CREATE TABLE "arma" (
    "idItem" integer NOT NULL,
    "dadoAtaque" character varying(3) NOT NULL,
    "chanceCritico" integer NOT NULL,
    "multiplicador" integer NOT NULL,
    "multiplicadorCritico" integer NOT NULL,
    "alcance" integer NOT NULL,
    "tipoArma" character varying(15) NOT NULL,

    CONSTRAINT "fk_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE
);


CREATE TABLE "armadura" (
    "idItem" integer NOT NULL,
    "dadoDefesa" character varying(3) NOT NULL,
    "defesaPassiva" integer NOT NULL,
    "criticoDefensivo" integer NOT NULL,
    "bonusDefesa" integer NOT NULL,
    "tipoArmadura" character varying(15) NOT NULL,

    CONSTRAINT "fk_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE
);


CREATE TABLE "pocao" (
    "idItem" integer NOT NULL,
    "duracaoTurnos" integer NOT NULL,

    CONSTRAINT "fk_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE
);


CREATE TABLE "inst_item" (
    "idItem" integer PRIMARY KEY,
    "quantidade" integer NOT NULL,
    "idMonstro" integer,
    "idInventario" integer,
    "idLojaNPC" integer,
    "seedSala" character varying(10),
    "nickName" character varying(60),

    CONSTRAINT "fk_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE,
    CONSTRAINT "fk_inst_monstro" FOREIGN KEY ("idMonstro") REFERENCES "inst_monstro" ("idMonstro") ON DELETE CASCADE,
    CONSTRAINT "fk_inst_inventario" FOREIGN KEY ("idInventario") REFERENCES "inst_inventario" ("idInventario") ON DELETE CASCADE,
    CONSTRAINT "fk_lojaNPC" FOREIGN KEY ("idLojaNPC") REFERENCES "lojaNPC" ("idLojaNPC") ON DELETE CASCADE,
    CONSTRAINT "fk_sala" FOREIGN KEY ("seedSala") REFERENCES "sala" ("seedSala") ON DELETE CASCADE,
    CONSTRAINT "fk_lojaJogador" FOREIGN KEY ("nickName") REFERENCES "lojaJogador" ("nickName") ON DELETE CASCADE
);


CREATE TABLE "monstro_item" (
    "idMonstro" integer NOT NULL,
    "idItem" integer NOT NULL,
    "chanceDrop" real NOT NULL,
    "qtdMinima" integer NOT NULL,
    "qtdMaxima" integer NOT NULL,

    CONSTRAINT "fk_monstro" FOREIGN KEY ("idMonstro") REFERENCES "monstro" ("idMonstro") ON DELETE CASCADE,
    CONSTRAINT "fk_monstrp" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE
);


CREATE TABLE "efeito" (
    "idEfeito" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "descricao" character varying(100) NOT NULL,
    "tipo" character varying(15) NOT NULL,
    "valor" integer NOT NULL,
    "duracaoTurnos" integer NOT NULL
);


CREATE TABLE "receita" (
    "idItem" integer NOT NULL,
    "idItemr" integer NOT NULL,
    "quantidade" integer NOT NULL,

    CONSTRAINT "fk_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE,
    CONSTRAINT "fk_item" FOREIGN KEY ("idItemr") REFERENCES "item" ("idItem") ON DELETE CASCADE
);


CREATE TABLE "jogador" (
    "nickName" character varying(60) PRIMARY KEY,
    "maxHP" integer NOT NULL,
    "atualHP" integer NOT NULL,
    "ouro" real NOT NULL,
    "idEfeito" integer,

    CONSTRAINT "fk_efeito" FOREIGN KEY ("idEfeito") REFERENCES "efeito" ("idEfeito") ON DELETE CASCADE
);


CREATE TABLE "lojaJogador" (
    "nickName" character varying(60) PRIMARY KEY,
    "nivel" integer NOT NULL,
    "exposicaoMaxima" integer NOT NULL,
    "exposicaoUsada" integer NOT NULL,
    "idMapa" integer NOT NULL,

    CONSTRAINT "fk_jogador" FOREIGN KEY ("nickName") REFERENCES "jogador" ("nickName") ON DELETE CASCADE,
    CONSTRAINT "fk_mapa" FOREIGN KEY ("idMapa") REFERENCES "mapa" ("idMapa") ON DELETE CASCADE
);


CREATE TABLE "inventario" (
    "idInventario" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "slotMaximo" integer NOT NULL
);


CREATE TABLE "inst_inventario" (
    "idInventario" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "nickname" character varying(60) NOT NULL,
    "slotOcupado" integer NOT NULL,

    CONSTRAINT "fk_inventario" FOREIGN KEY ("idInventario") REFERENCES "inventario" ("idInventario") ON DELETE CASCADE,
    CONSTRAINT "fk_jogador" FOREIGN KEY ("nickname") REFERENCES "jogador" ("nickName") ON DELETE CASCADE
);


CREATE TABLE "npc" (
    "idNPC" integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "nome" character varying(30) NOT NULL,
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
    "idLojaNPC" integer NOT NULL,

    CONSTRAINT "fk_lojaNPC" PRIMARY KEY ("idLojaNPC") REFERENCES "lojaNPC" ("idLojaNPC") ON DELETE CASCADE
);


CREATE TABLE "varejo" (
    "idLojaNPC" integer NOT NULL,
    "margemLucro" integer NOT NULL,

    CONSTRAINT "fk_lojaNPC" PRIMARY KEY ("idLojaNPC") REFERENCES "lojaNPC" ("idLojaNPC") ON DELETE CASCADE
);


CREATE TABLE "banco" (
    "idLojaNPC" integer NOT NULL,
    "valorEntrada" integer,
    "valorAtual" integer NOT NULL,

    CONSTRAINT "fk_lojaNPC" PRIMARY KEY ("idLojaNPC") REFERENCES "lojaNPC" ("idLojaNPC") ON DELETE CASCADE
);


CREATE TABLE "dialogo" (
    "idDialogo" integer PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "conteudo" character varying(300) NOT NULL,
    "ordem" integer NOT NULL,
    "tipo" character varying(60) NOT NULL,
    "idDialogo" integer,

    CONSTRAINT "fk_dialogo" FOREIGN KEY ("idDialogo") REFERENCES "dialogo" ("idDialogo") ON DELETE CASCADE
);


CREATE TABLE "dialogo_npc" (
    "idDialogo" integer NOT NULL,
    "idNPC" integer NOT NULL,

    CONSTRAINT "fk_dialogo" FOREIGN KEY ("idDialogo") REFERENCES "dialogo" ("idDialogo") ON DELETE CASCADE,
    CONSTRAINT "fk_npc" FOREIGN KEY ("idNPC") REFERENCES "npc" ("idNPC") ON DELETE CASCADE
);