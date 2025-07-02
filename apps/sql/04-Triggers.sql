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
DROP TRIGGER IF EXISTS trigger_aplicar_juros_dia ON "mundo";
CREATE TRIGGER trigger_aplicar_juros_dia
    AFTER UPDATE ON "mundo"
    FOR EACH ROW
    EXECUTE FUNCTION aplicar_juros_ao_mudar_dia(); 