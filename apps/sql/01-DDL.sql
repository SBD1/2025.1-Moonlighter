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
    "descricao" CHARACTER varying(800) NOT NULL,
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
    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

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

    CONSTRAINT "fk_local" FOREIGN KEY ("nomeLocal") REFERENCES "local" ("nomeLocal") ON DELETE CASCADE
);

CREATE TABLE "estabelecimento" (
    "nomeLocal" character varying(60) PRIMARY KEY,

    CONSTRAINT "fk_local" FOREIGN KEY ("nomeLocal") REFERENCES "local" ("nomeLocal") ON DELETE CASCADE
);

CREATE TABLE "inst_masmorra" (
    "seedMundo" CHARACTER varying(30) NOT NULL,
    "seedMasmorra" character varying(36) NOT NULL,
    "nomeLocal" character varying(60) NOT NULL,
    "ativo" BOOLEAN NOT NULL,

    CONSTRAINT "fk_masmorra" FOREIGN KEY ("nomeLocal") REFERENCES "masmorra" ("nomeLocal") ON DELETE CASCADE,
    CONSTRAINT "pk_inst_masmorra" PRIMARY KEY ("seedMundo", "seedMasmorra")
);


CREATE TABLE "sala" (
    "seedSala" character varying(30) PRIMARY KEY,
    "posicaoX" integer NOT NULL,
    "posicaoY" integer NOT NULL,
    "conexão" CHARACTER varying(4) NOT NULL,
    "categoria" character varying(60) NOT NULL,
    "seedMundo" character varying(30) NOT NULL,
    "seedMasmorra" character varying(36) NOT NULL,

    CONSTRAINT "fk_inst_masmorra" FOREIGN KEY ("seedMasmorra", "seedMundo") REFERENCES "inst_masmorra" ("seedMasmorra", "seedMundo") ON DELETE CASCADE
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
    CONSTRAINT "fk_monstro" FOREIGN KEY ("idMonstro" ) REFERENCES "monstro" ("idMonstro") ON DELETE CASCADE,
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
    "quantidade" SMALLINT NOT NULL,

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


-- Tabela para instâncias de itens - permite o mesmo item estar em múltiplos locais
CREATE TABLE "inst_item" (
    "idInstItem" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "idItem" integer NOT NULL,
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
    CONSTRAINT "fk_loja_jogador" FOREIGN KEY ("seedMundoLojaJogador") REFERENCES "loja_jogador" ("seedMundo") ON DELETE CASCADE,
    
    -- Garantir que um item não seja duplicado no mesmo inventário
    CONSTRAINT "uk_item_inventario" UNIQUE ("idItem", "idInventario", "nickname")
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

-- ================================================================
-- TABELA DE ITENS NO CHÃO (MUNDO)
-- Data: 30/06/2025
-- Descrição: Tabela para armazenar itens dropados no mundo
-- ================================================================

CREATE TABLE "item_chao" (
    "idItemChao" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "idItem" integer NOT NULL,
    "quantidade" SMALLINT NOT NULL DEFAULT 1,
    "posicaoX" integer NOT NULL,
    "posicaoY" integer NOT NULL,
    "seedMundo" character varying(30) NOT NULL,
    "nomeLocal" character varying(60) NOT NULL,
    "tempoDropado" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "tempoExpiracao" TIMESTAMP, -- NULL = não expira
    
    CONSTRAINT "fk_item_chao_item" FOREIGN KEY ("idItem") REFERENCES "item" ("idItem") ON DELETE CASCADE,
    CONSTRAINT "fk_item_chao_mundo" FOREIGN KEY ("seedMundo") REFERENCES "mundo" ("seedMundo") ON DELETE CASCADE,
    CONSTRAINT "fk_item_chao_local" FOREIGN KEY ("nomeLocal") REFERENCES "local" ("nomeLocal") ON DELETE CASCADE,
    CONSTRAINT "ck_quantidade_positiva" CHECK ("quantidade" > 0)
);

-- Índices para melhorar performance
CREATE INDEX "idx_item_chao_localizacao" ON "item_chao" ("seedMundo", "nomeLocal", "posicaoX", "posicaoY");
CREATE INDEX "idx_item_chao_expiracao" ON "item_chao" ("tempoExpiracao") WHERE "tempoExpiracao" IS NOT NULL;

-- ================================================================
-- TRIGGERS PARA MANTER INTEGRIDADE DAS ESPECIALIZAÇÕES
-- Data: 30/06/2025
-- Descrição: Triggers para validar especialização única e cascata
-- ================================================================

-- Função para validar especialização única de itens
CREATE OR REPLACE FUNCTION validar_especializacao_item()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se item já existe em outra especialização
    IF TG_TABLE_NAME = 'arma' THEN
        IF EXISTS (SELECT 1 FROM "armadura" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já classificado como Armadura. Não pode ser salvo como Arma.', NEW."idItem";
        END IF;
        IF EXISTS (SELECT 1 FROM "pocao" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já classificado como Poção. Não pode ser salvo como Arma.', NEW."idItem";
        END IF;
        -- Atualizar tipo na tabela item
        UPDATE "item" SET "tipo" = 'Arma' WHERE "idItem" = NEW."idItem";
        
    ELSIF TG_TABLE_NAME = 'armadura' THEN
        IF EXISTS (SELECT 1 FROM "arma" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já classificado como Arma. Não pode ser salvo como Armadura.', NEW."idItem";
        END IF;
        IF EXISTS (SELECT 1 FROM "pocao" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já classificado como Poção. Não pode ser salvo como Armadura.', NEW."idItem";
        END IF;
        -- Atualizar tipo na tabela item
        UPDATE "item" SET "tipo" = 'Armadura' WHERE "idItem" = NEW."idItem";
        
    ELSIF TG_TABLE_NAME = 'pocao' THEN
        IF EXISTS (SELECT 1 FROM "arma" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já classificado como Arma. Não pode ser salvo como Poção.', NEW."idItem";
        END IF;
        IF EXISTS (SELECT 1 FROM "armadura" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já classificado como Armadura. Não pode ser salvo como Poção.', NEW."idItem";
        END IF;
        -- Atualizar tipo na tabela item
        UPDATE "item" SET "tipo" = 'Consumível' WHERE "idItem" = NEW."idItem";
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Função para validar especialização única de locais
CREATE OR REPLACE FUNCTION validar_especializacao_local()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se local já existe em outra especialização
    IF TG_TABLE_NAME = 'masmorra' THEN
        IF EXISTS (SELECT 1 FROM "estabelecimento" WHERE "nomeLocal" = NEW."nomeLocal") THEN
            RAISE EXCEPTION 'Local % já classificado como Estabelecimento. Não pode ser salvo como Masmorra.', NEW."nomeLocal";
        END IF;
        -- Atualizar tipo na tabela local
        UPDATE "local" SET "tipoLocal" = 'Masmorra' WHERE "nomeLocal" = NEW."nomeLocal";
        
    ELSIF TG_TABLE_NAME = 'estabelecimento' THEN
        IF EXISTS (SELECT 1 FROM "masmorra" WHERE "nomeLocal" = NEW."nomeLocal") THEN
            RAISE EXCEPTION 'Local % já classificado como Masmorra. Não pode ser salvo como Estabelecimento.', NEW."nomeLocal";
        END IF;
        -- Atualizar tipo na tabela local
        UPDATE "local" SET "tipoLocal" = 'Estabelecimento' WHERE "nomeLocal" = NEW."nomeLocal";
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar tipo quando especialização é deletada (itens)
CREATE OR REPLACE FUNCTION atualizar_tipo_item_apos_delete()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o item ainda existe em outras especializações
    IF NOT EXISTS (
        SELECT 1 FROM "arma" WHERE "idItem" = OLD."idItem"
        UNION ALL
        SELECT 1 FROM "armadura" WHERE "idItem" = OLD."idItem"
        UNION ALL  
        SELECT 1 FROM "pocao" WHERE "idItem" = OLD."idItem"
    ) THEN
        -- Se não existe em nenhuma especialização, definir tipo como NULL
        UPDATE "item" SET "tipo" = NULL WHERE "idItem" = OLD."idItem";
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Função para atualizar tipo quando especialização é deletada (locais)
CREATE OR REPLACE FUNCTION atualizar_tipo_local_apos_delete()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o local ainda existe em outras especializações
    IF NOT EXISTS (
        SELECT 1 FROM "masmorra" WHERE "nomeLocal" = OLD."nomeLocal"
        UNION ALL
        SELECT 1 FROM "estabelecimento" WHERE "nomeLocal" = OLD."nomeLocal"
    ) THEN
        -- Se não existe em nenhuma especialização, definir tipo como 'Local'
        UPDATE "local" SET "tipoLocal" = 'Local' WHERE "nomeLocal" = OLD."nomeLocal";
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Função para deletar especialização quando item generalizado é deletado
CREATE OR REPLACE FUNCTION deletar_especializacao_item()
RETURNS TRIGGER AS $$
BEGIN
    -- Deletar das tabelas especializadas quando item é deletado
    DELETE FROM "arma" WHERE "idItem" = OLD."idItem";
    DELETE FROM "armadura" WHERE "idItem" = OLD."idItem";
    DELETE FROM "pocao" WHERE "idItem" = OLD."idItem";
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Função para deletar especialização quando local generalizado é deletado
CREATE OR REPLACE FUNCTION deletar_especializacao_local()
RETURNS TRIGGER AS $$
BEGIN
    -- Deletar das tabelas especializadas quando local é deletado
    DELETE FROM "masmorra" WHERE "nomeLocal" = OLD."nomeLocal";
    DELETE FROM "estabelecimento" WHERE "nomeLocal" = OLD."nomeLocal";
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Triggers para validação de especialização única (itens)
CREATE TRIGGER trig_validar_arma
    BEFORE INSERT ON "arma"
    FOR EACH ROW EXECUTE FUNCTION validar_especializacao_item();

CREATE TRIGGER trig_validar_armadura
    BEFORE INSERT ON "armadura"
    FOR EACH ROW EXECUTE FUNCTION validar_especializacao_item();

CREATE TRIGGER trig_validar_pocao
    BEFORE INSERT ON "pocao"
    FOR EACH ROW EXECUTE FUNCTION validar_especializacao_item();

-- Triggers para validação de especialização única (locais)
CREATE TRIGGER trig_validar_masmorra
    BEFORE INSERT ON "masmorra"
    FOR EACH ROW EXECUTE FUNCTION validar_especializacao_local();

CREATE TRIGGER trig_validar_estabelecimento
    BEFORE INSERT ON "estabelecimento"
    FOR EACH ROW EXECUTE FUNCTION validar_especializacao_local();

-- Triggers para atualizar tipo quando especialização é deletada (itens)
CREATE TRIGGER trig_atualizar_tipo_arma
    AFTER DELETE ON "arma"
    FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_item_apos_delete();

CREATE TRIGGER trig_atualizar_tipo_armadura
    AFTER DELETE ON "armadura"
    FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_item_apos_delete();

CREATE TRIGGER trig_atualizar_tipo_pocao
    AFTER DELETE ON "pocao"
    FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_item_apos_delete();

-- Triggers para atualizar tipo quando especialização é deletada (locais)
CREATE TRIGGER trig_atualizar_tipo_masmorra
    AFTER DELETE ON "masmorra"
    FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_local_apos_delete();

CREATE TRIGGER trig_atualizar_tipo_estabelecimento
    AFTER DELETE ON "estabelecimento"
    FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_local_apos_delete();

-- Triggers para deletar especializações quando generalização é deletada
CREATE TRIGGER trig_deletar_item_especializacao
    BEFORE DELETE ON "item"
    FOR EACH ROW EXECUTE FUNCTION deletar_especializacao_item();

CREATE TRIGGER trig_deletar_local_especializacao
    BEFORE DELETE ON "local"
    FOR EACH ROW EXECUTE FUNCTION deletar_especializacao_local();

-- ================================================================
-- VIEWS ESSENCIAIS
-- ================================================================

-- View para inventário do jogador
CREATE OR REPLACE VIEW view_inventario_jogador AS
SELECT 
    j."nickname",
    inv."nome" AS "tipo_inventario",
    i."nome" AS "nome_item",
    ii."quantidade",
    i."tipo" AS "categoria_item",
    i."precoBase",
    i."descricao",
    ii."idInstItem"
FROM "jogador" j
JOIN "inst_inventario" iinv ON j."nickname" = iinv."nickname"
JOIN "inventario" inv ON iinv."idInventario" = inv."idInventario"
LEFT JOIN "inst_item" ii ON iinv."idInventario" = ii."idInventario" 
    AND iinv."nickname" = ii."nickname"
LEFT JOIN "item" i ON ii."idItem" = i."idItem";

-- View para itens no chão
CREATE OR REPLACE VIEW view_itens_chao AS
SELECT 
    ic."idItemChao",
    ic."idItem",
    i."nome",
    ic."quantidade",
    ic."posicaoX",
    ic."posicaoY",
    i."descricao",
    ic."seedMundo",
    ic."nomeLocal",
    ic."tempoDropado"
FROM "item_chao" ic
JOIN "item" i ON ic."idItem" = i."idItem"
ORDER BY ic."tempoDropado" DESC;

-- ================================================================
-- FUNÇÕES AUXILIARES
-- ================================================================

-- Função para obter itens no chão por localização do jogador
CREATE OR REPLACE FUNCTION obter_itens_chao_local(p_nickname VARCHAR)
RETURNS TABLE(
    "idItemChao" INTEGER,
    "idItem" INTEGER,
    "nome" VARCHAR,
    "quantidade" SMALLINT,
    "posicaoX" INTEGER,
    "posicaoY" INTEGER,
    "descricao" VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ic."idItemChao",
        ic."idItem",
        i."nome",
        ic."quantidade",
        ic."posicaoX",
        ic."posicaoY",
        i."descricao"
    FROM "item_chao" ic
    JOIN "item" i ON ic."idItem" = i."idItem"
    JOIN "jogador" j ON j."nickname" = p_nickname
    JOIN "mundo" m ON j."nickname" = m."nickname"
    WHERE ic."seedMundo" = m."seedMundo" 
    AND ic."nomeLocal" = j."nomeLocal"
    ORDER BY ic."tempoDropado" DESC;
END;
$$ LANGUAGE plpgsql;

-- Função para obter inventário completo do jogador
CREATE OR REPLACE FUNCTION obter_inventario_jogador(p_nickname VARCHAR)
RETURNS TABLE(
    "nickname" VARCHAR,
    "tipo_inventario" VARCHAR,
    "nome_item" VARCHAR,
    "quantidade" SMALLINT,
    "categoria_item" VARCHAR,
    "precoBase" INTEGER,
    "descricao" VARCHAR,
    "idInstItem" INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM view_inventario_jogador 
    WHERE "nickname" = p_nickname AND "nome_item" IS NOT NULL
    ORDER BY "tipo_inventario", "nome_item";
END;
$$ LANGUAGE plpgsql;

