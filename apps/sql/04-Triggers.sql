-- ---------------------------------------------------------------------------------------------------------------
-- Data de Criação ........: 26/06/2025                                                                         --
-- Autor(es) ..............: Arthur Evangelista Moonlighter                                                                 --
-- Versão .................: 1.0                                                                                --
-- Banco de Dados .........: PostgreSQL                                                                         --
-- Descrição ..............: Triggers para validações do jogo Moonlighter                                        --
-- ---------------------------------------------------------------------------------------------------------------

-- TRIGGER PARA APLICAR JUROS QUANDO O DIA MUDA
-- Aplica juros diários (2.5% ao dia) quando o dia do mundo é atualizado
CREATE OR REPLACE FUNCTION aplicar_juros_ao_mudar_dia()
RETURNS TRIGGER AS $$
DECLARE
    dias_passados INTEGER;
    juros_calculados INTEGER;
    taxa_juros DECIMAL(5,2) := 2.50; -- 2.5% ao dia
BEGIN
    -- Se o dia mudou, aplicar juros aos bancos do mundo
    IF OLD."dia" != NEW."dia" THEN
        dias_passados := NEW."dia" - OLD."dia";
        

        UPDATE "inst_banco" 
        SET "valorAtual" = "valorAtual" + FLOOR("valorAtual" * (taxa_juros / 100.0) * dias_passados)
        WHERE "seedMundo" = NEW."seedMundo";
        
        -- Log da aplicação de juros
        RAISE NOTICE 'Juros aplicados no mundo %: % dias passaram', NEW."seedMundo", dias_passados;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger
CREATE TRIGGER trigger_aplicar_juros_dia
    AFTER UPDATE ON "mundo"
    FOR EACH ROW
    EXECUTE FUNCTION aplicar_juros_ao_mudar_dia();

-- ================================================================
-- TRIGGER PARA VALIDAÇÃO DE ESPECIALIZAÇÃO ÚNICA DE ARMADURAS
-- Data: 04/07/2025
-- ================================================================

-- TRIGGER PARA VALIDAR ESPECIALIZAÇÃO ÚNICA DE ARMADURAS
-- Garante que um item classificado como "Armadura" não possa ser salvo nas demais especializações
CREATE OR REPLACE FUNCTION validar_armadura_especializacao_unica()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o item já existe em outras especializações
    IF EXISTS (SELECT 1 FROM "arma" WHERE "idItem" = NEW."idItem") THEN
        RAISE EXCEPTION 'Item ID % já está classificado como Arma. Um item não pode ter múltiplas especializações.', NEW."idItem";
    END IF;
    
    IF EXISTS (SELECT 1 FROM "pocao" WHERE "idItem" = NEW."idItem") THEN
        RAISE EXCEPTION 'Item ID % já está classificado como Poção. Um item não pode ter múltiplas especializações.', NEW."idItem";
    END IF;
    
    -- Se passou nas validações, atualizar o tipo na tabela principal
    UPDATE "item" SET "tipo" = 'Armadura' WHERE "idItem" = NEW."idItem";
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger para armaduras
CREATE TRIGGER trigger_validar_armadura_unica
    BEFORE INSERT ON "armadura"
    FOR EACH ROW
    EXECUTE FUNCTION validar_armadura_especializacao_unica();

-- ================================================================
-- TRIGGER PARA VALIDAÇÃO DE ESPECIALIZAÇÃO ÚNICA DE POÇÕES
-- Data: 04/07/2025
-- ================================================================

-- TRIGGER PARA VALIDAR ESPECIALIZAÇÃO ÚNICA DE POÇÕES
-- Garante que um item classificado como "Poção" não possa ser salvo nas demais especializações
CREATE OR REPLACE FUNCTION validar_pocao_especializacao_unica()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o item já existe em outras especializações
    IF EXISTS (SELECT 1 FROM "arma" WHERE "idItem" = NEW."idItem") THEN
        RAISE EXCEPTION 'Item ID % já está classificado como Arma. Um item não pode ter múltiplas especializações.', NEW."idItem";
    END IF;
    
    IF EXISTS (SELECT 1 FROM "armadura" WHERE "idItem" = NEW."idItem") THEN
        RAISE EXCEPTION 'Item ID % já está classificado como Armadura. Um item não pode ter múltiplas especializações.', NEW."idItem";
    END IF;
    
    -- Se passou nas validações, atualizar o tipo na tabela principal
    UPDATE "item" SET "tipo" = 'Consumível' WHERE "idItem" = NEW."idItem";
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger para poções
CREATE TRIGGER trigger_validar_pocao_unica
    BEFORE INSERT ON "pocao"
    FOR EACH ROW
    EXECUTE FUNCTION validar_pocao_especializacao_unica();

-- ================================================================
-- TRIGGER PARA VALIDAÇÃO DE ESPECIALIZAÇÃO ÚNICA DE ARMAS
-- Data: 04/07/2025
-- ================================================================

-- TRIGGER PARA VALIDAR ESPECIALIZAÇÃO ÚNICA DE ARMAS
-- Garante que um item classificado como "Arma" não possa ser salvo nas demais especializações
CREATE OR REPLACE FUNCTION validar_arma_especializacao_unica()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o item já existe em outras especializações
    IF EXISTS (SELECT 1 FROM "armadura" WHERE "idItem" = NEW."idItem") THEN
        RAISE EXCEPTION 'Item ID % já está classificado como Armadura. Um item não pode ter múltiplas especializações.', NEW."idItem";
    END IF;
    
    IF EXISTS (SELECT 1 FROM "pocao" WHERE "idItem" = NEW."idItem") THEN
        RAISE EXCEPTION 'Item ID % já está classificado como Poção. Um item não pode ter múltiplas especializações.', NEW."idItem";
    END IF;
    
    -- Se passou nas validações, atualizar o tipo na tabela principal
    UPDATE "item" SET "tipo" = 'Arma' WHERE "idItem" = NEW."idItem";
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger para armas
CREATE TRIGGER trigger_validar_arma_unica
    BEFORE INSERT ON "arma"
    FOR EACH ROW
    EXECUTE FUNCTION validar_arma_especializacao_unica();

-- ================================================================
-- TRIGGER PARA VALIDAÇÃO DE ESPECIALIZAÇÃO ÚNICA DE ESTABELECIMENTOS
-- Data: 04/07/2025
-- ================================================================

-- TRIGGER PARA VALIDAR ESPECIALIZAÇÃO ÚNICA DE ESTABELECIMENTOS
-- Garante que um local classificado como "Estabelecimento" não possa ser salvo como Masmorra
CREATE OR REPLACE FUNCTION validar_estabelecimento_especializacao_unica()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o local já existe como Masmorra
    IF EXISTS (SELECT 1 FROM "masmorra" WHERE "nomeLocal" = NEW."nomeLocal") THEN
        RAISE EXCEPTION 'Local % já está classificado como Masmorra. Um local não pode ter múltiplas especializações.', NEW."nomeLocal";
    END IF;
    
    -- Se passou nas validações, atualizar o tipo na tabela principal
    UPDATE "local" SET "tipoLocal" = 'Estabelecimento' WHERE "nomeLocal" = NEW."nomeLocal";
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger para estabelecimentos
CREATE TRIGGER trigger_validar_estabelecimento_unico
    BEFORE INSERT ON "estabelecimento"
    FOR EACH ROW
    EXECUTE FUNCTION validar_estabelecimento_especializacao_unica();

-- ================================================================
-- TRIGGER PARA VALIDAÇÃO DE ESPECIALIZAÇÃO ÚNICA DE MASMORRAS
-- Data: 04/07/2025
-- ================================================================

-- TRIGGER PARA VALIDAR ESPECIALIZAÇÃO ÚNICA DE MASMORRAS
-- Garante que um local classificado como "Masmorra" não possa ser salvo como Estabelecimento
CREATE OR REPLACE FUNCTION validar_masmorra_especializacao_unica()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o local já existe como Estabelecimento
    IF EXISTS (SELECT 1 FROM "estabelecimento" WHERE "nomeLocal" = NEW."nomeLocal") THEN
        RAISE EXCEPTION 'Local % já está classificado como Estabelecimento. Um local não pode ter múltiplas especializações.', NEW."nomeLocal";
    END IF;
    
    -- Se passou nas validações, atualizar o tipo na tabela principal
    UPDATE "local" SET "tipoLocal" = 'Masmorra' WHERE "nomeLocal" = NEW."nomeLocal";
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger para masmorras
CREATE TRIGGER trigger_validar_masmorra_unica
    BEFORE INSERT ON "masmorra"
    FOR EACH ROW
    EXECUTE FUNCTION validar_masmorra_especializacao_unica();

-- ================================================================
-- TRIGGERS PARA REMOÇÃO EM CASCATA DAS ESPECIALIZAÇÕES
-- Data: 04/07/2025
-- ================================================================

-- TRIGGER PARA APAGAR ESPECIALIZAÇÕES DE ITENS QUANDO ITEM É REMOVIDO
-- Garante que quando um item é apagado da tabela generalizada, suas especializações também sejam removidas
CREATE OR REPLACE FUNCTION remover_especializacoes_item()
RETURNS TRIGGER AS $$
BEGIN
    -- Remover item de todas as tabelas especializadas
    DELETE FROM "arma" WHERE "idItem" = OLD."idItem";
    DELETE FROM "armadura" WHERE "idItem" = OLD."idItem";
    DELETE FROM "pocao" WHERE "idItem" = OLD."idItem";
    
    -- Log da remoção
    RAISE NOTICE 'Especializações do item ID % foram removidas automaticamente.', OLD."idItem";
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger para remoção de especializações de itens
CREATE TRIGGER trigger_remover_especializacoes_item
    BEFORE DELETE ON "item"
    FOR EACH ROW
    EXECUTE FUNCTION remover_especializacoes_item();

-- TRIGGER PARA APAGAR ESPECIALIZAÇÕES DE LOCAIS QUANDO LOCAL É REMOVIDO
-- Garante que quando um local é apagado da tabela generalizada, suas especializações também sejam removidas
CREATE OR REPLACE FUNCTION remover_especializacoes_local()
RETURNS TRIGGER AS $$
BEGIN
    -- Remover local de todas as tabelas especializadas
    DELETE FROM "estabelecimento" WHERE "nomeLocal" = OLD."nomeLocal";
    DELETE FROM "masmorra" WHERE "nomeLocal" = OLD."nomeLocal";
    
    -- Log da remoção
    RAISE NOTICE 'Especializações do local % foram removidas automaticamente.', OLD."nomeLocal";
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger para remoção de especializações de locais
CREATE TRIGGER trigger_remover_especializacoes_local
    BEFORE DELETE ON "local"
    FOR EACH ROW
    EXECUTE FUNCTION remover_especializacoes_local();

-- ================================================================
-- TRIGGERS PARA ATUALIZAÇÃO DE TIPO APÓS REMOÇÃO DE ESPECIALIZAÇÕES
-- Data: 04/07/2025
-- ================================================================

-- TRIGGER PARA ATUALIZAR TIPO DO ITEM QUANDO ESPECIALIZAÇÃO DE ARMA É REMOVIDA
-- Garante que quando uma arma é removida, o tipo do item generalizado seja atualizado
CREATE OR REPLACE FUNCTION atualizar_tipo_apos_remover_arma()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o item ainda existe em outras especializações
    IF NOT EXISTS (
        SELECT 1 FROM "armadura" WHERE "idItem" = OLD."idItem"
        UNION ALL
        SELECT 1 FROM "pocao" WHERE "idItem" = OLD."idItem"
    ) THEN
        -- Se não existe em nenhuma outra especialização, definir tipo como NULL
        UPDATE "item" SET "tipo" = NULL WHERE "idItem" = OLD."idItem";
        RAISE NOTICE 'Tipo do item ID % atualizado para NULL após remoção da especialização Arma.', OLD."idItem";
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER PARA ATUALIZAR TIPO DO ITEM QUANDO ESPECIALIZAÇÃO DE ARMADURA É REMOVIDA
-- Garante que quando uma armadura é removida, o tipo do item generalizado seja atualizado
CREATE OR REPLACE FUNCTION atualizar_tipo_apos_remover_armadura()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o item ainda existe em outras especializações
    IF NOT EXISTS (
        SELECT 1 FROM "arma" WHERE "idItem" = OLD."idItem"
        UNION ALL
        SELECT 1 FROM "pocao" WHERE "idItem" = OLD."idItem"
    ) THEN
        -- Se não existe em nenhuma outra especialização, definir tipo como NULL
        UPDATE "item" SET "tipo" = NULL WHERE "idItem" = OLD."idItem";
        RAISE NOTICE 'Tipo do item ID % atualizado para NULL após remoção da especialização Armadura.', OLD."idItem";
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER PARA ATUALIZAR TIPO DO ITEM QUANDO ESPECIALIZAÇÃO DE POÇÃO É REMOVIDA
-- Garante que quando uma poção é removida, o tipo do item generalizado seja atualizado
CREATE OR REPLACE FUNCTION atualizar_tipo_apos_remover_pocao()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o item ainda existe em outras especializações
    IF NOT EXISTS (
        SELECT 1 FROM "arma" WHERE "idItem" = OLD."idItem"
        UNION ALL
        SELECT 1 FROM "armadura" WHERE "idItem" = OLD."idItem"
    ) THEN
        -- Se não existe em nenhuma outra especialização, definir tipo como NULL
        UPDATE "item" SET "tipo" = NULL WHERE "idItem" = OLD."idItem";
        RAISE NOTICE 'Tipo do item ID % atualizado para NULL após remoção da especialização Poção.', OLD."idItem";
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER PARA ATUALIZAR TIPO DO LOCAL QUANDO ESPECIALIZAÇÃO DE ESTABELECIMENTO É REMOVIDA
-- Garante que quando um estabelecimento é removido, o tipo do local generalizado seja atualizado
CREATE OR REPLACE FUNCTION atualizar_tipo_apos_remover_estabelecimento()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o local ainda existe em outras especializações
    IF NOT EXISTS (
        SELECT 1 FROM "masmorra" WHERE "nomeLocal" = OLD."nomeLocal"
    ) THEN
        -- Se não existe em nenhuma outra especialização, definir tipo como 'Local'
        UPDATE "local" SET "tipoLocal" = 'Local' WHERE "nomeLocal" = OLD."nomeLocal";
        RAISE NOTICE 'Tipo do local % atualizado para Local após remoção da especialização Estabelecimento.', OLD."nomeLocal";
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER PARA ATUALIZAR TIPO DO LOCAL QUANDO ESPECIALIZAÇÃO DE MASMORRA É REMOVIDA
-- Garante que quando uma masmorra é removida, o tipo do local generalizado seja atualizado
CREATE OR REPLACE FUNCTION atualizar_tipo_apos_remover_masmorra()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o local ainda existe em outras especializações
    IF NOT EXISTS (
        SELECT 1 FROM "estabelecimento" WHERE "nomeLocal" = OLD."nomeLocal"
    ) THEN
        -- Se não existe em nenhuma outra especialização, definir tipo como 'Local'
        UPDATE "local" SET "tipoLocal" = 'Local' WHERE "nomeLocal" = OLD."nomeLocal";
        RAISE NOTICE 'Tipo do local % atualizado para Local após remoção da especialização Masmorra.', OLD."nomeLocal";
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Criar os triggers para atualização de tipo após remoção de especializações de itens
CREATE TRIGGER trigger_atualizar_tipo_apos_remover_arma
    AFTER DELETE ON "arma"
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_tipo_apos_remover_arma();

CREATE TRIGGER trigger_atualizar_tipo_apos_remover_armadura
    AFTER DELETE ON "armadura"
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_tipo_apos_remover_armadura();

CREATE TRIGGER trigger_atualizar_tipo_apos_remover_pocao
    AFTER DELETE ON "pocao"
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_tipo_apos_remover_pocao();

-- Criar os triggers para atualização de tipo após remoção de especializações de locais
CREATE TRIGGER trigger_atualizar_tipo_apos_remover_estabelecimento
    AFTER DELETE ON "estabelecimento"
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_tipo_apos_remover_estabelecimento();

CREATE TRIGGER trigger_atualizar_tipo_apos_remover_masmorra
    AFTER DELETE ON "masmorra"
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_tipo_apos_remover_masmorra();
