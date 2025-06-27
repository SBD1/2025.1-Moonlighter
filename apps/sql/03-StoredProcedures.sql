-- ---------------------------------------------------------------------------------------------------------------
-- Data de Criação ........: 26/06/2025                                                                         --
-- Autor(es) ..............: Arthur Evangelista Moonlighter                                                                 --
-- Versão .................: 1.0                                                                                --
-- Banco de Dados .........: PostgreSQL                                                                         --
-- Descrição ..............: Stored Procedures para os estabelecimentos do jogo Moonlighter                    --
-- ---------------------------------------------------------------------------------------------------------------


-- FUNÇÕES DO BANCO (inst_banco)


-- Função para verificar se uma instância de banco ja existe para um mundo
CREATE OR REPLACE FUNCTION verificar_instancia_banco(p_seed_mundo VARCHAR(30))
RETURNS BOOLEAN AS $$
DECLARE
    existe BOOLEAN;
BEGIN
    SELECT EXISTS(
        SELECT 1 FROM inst_banco 
        WHERE "seedMundo" = p_seed_mundo
    ) INTO existe;
    
    RETURN existe;
END;
$$ LANGUAGE plpgsql;

-- Função para criar uma nova instância de banco
CREATE OR REPLACE FUNCTION criar_instancia_banco(
    p_seed_mundo VARCHAR(30),
    p_nome_local VARCHAR(60),
    p_id_npc INTEGER,
    p_valor_entrada INTEGER DEFAULT 0
)
RETURNS BOOLEAN AS $$
BEGIN
    -- Verificar se já existe uma instância
    IF verificar_instancia_banco(p_seed_mundo) THEN
        RETURN FALSE; -- Já existe
    END IF;
    
    -- Inserir nova instância
    INSERT INTO inst_banco ("seedMundo", "nomeLocal", "idNPC", "valorEntrada", "valorAtual")
    VALUES (p_seed_mundo, p_nome_local, p_id_npc, p_valor_entrada, p_valor_entrada);
    
    RETURN TRUE; -- Criado com sucesso
EXCEPTION
    WHEN OTHERS THEN
        RETURN FALSE; -- Erro ao criar
END;
$$ LANGUAGE plpgsql;

-- Função para visualizar o saldo atual do banco
CREATE OR REPLACE FUNCTION visualizar_saldo_banco(p_seed_mundo VARCHAR(30))
RETURNS TABLE(
    saldo_atual INTEGER,
    valor_entrada INTEGER,
    nome_local VARCHAR(60)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ib."valorAtual"::INTEGER,
        ib."valorEntrada"::INTEGER,
        ib."nomeLocal"
    FROM inst_banco ib
    WHERE ib."seedMundo" = p_seed_mundo;
END;
$$ LANGUAGE plpgsql;

-- Função para aplicar ouro no banco
CREATE OR REPLACE FUNCTION aplicar_ouro_banco(
    p_seed_mundo VARCHAR(30),
    p_quantidade INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    saldo_atual INTEGER;
BEGIN
    -- Verificar se a instância existe
    IF NOT verificar_instancia_banco(p_seed_mundo) THEN
        RETURN FALSE; -- Instância não existe
    END IF;
    
    -- Verificar se a quantidade é válida
    IF p_quantidade <= 0 THEN
        RETURN FALSE; -- qtd invalida
    END IF;
    
    -- Atualizar o saldo
    UPDATE inst_banco 
    SET "valorAtual" = "valorAtual" + p_quantidade
    WHERE "seedMundo" = p_seed_mundo;
    
    -- Verificar se a atualização foi bem-sucedida
    IF FOUND THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RETURN FALSE; -- Erro ao aplicar
END;
$$ LANGUAGE plpgsql;

-- Função para sacar ouro do banco
CREATE OR REPLACE FUNCTION sacar_ouro_banco(
    p_seed_mundo VARCHAR(30),
    p_quantidade INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    saldo_atual INTEGER;
BEGIN
    -- Verificar se a instância existe
    IF NOT verificar_instancia_banco(p_seed_mundo) THEN
        RETURN FALSE; -- Instância não existe
    END IF;
    
    -- Verificar se a quantidade é válida
    IF p_quantidade <= 0 THEN
        RETURN FALSE; -- Quantidade inválida
    END IF;
    
    -- Verificar se há saldo suficiente
    SELECT "valorAtual" INTO saldo_atual
    FROM inst_banco
    WHERE "seedMundo" = p_seed_mundo;
    
    IF saldo_atual < p_quantidade THEN
        RETURN FALSE; -- Saldo insuficiente
    END IF;
    
    -- Atualizar o saldo
    UPDATE inst_banco 
    SET "valorAtual" = "valorAtual" - p_quantidade
    WHERE "seedMundo" = p_seed_mundo;
    
    -- Verificar se a atualização foi bem-sucedida
    IF FOUND THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RETURN FALSE; -- deu erro ao sacar
END;
$$ LANGUAGE plpgsql;
