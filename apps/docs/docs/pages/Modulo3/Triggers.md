<span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.0</span>

# Triggers

## O que são Triggers?

Triggers são blocos de código executados automaticamente pelo banco de dados em resposta a determinados eventos, como inserções, atualizações ou remoções de dados em tabelas. Eles são utilizados para garantir regras de negócio, integridade dos dados e automatizar processos que devem ocorrer de forma transparente para o usuário.

---

## Triggers e Funções

??? info "Trigger: trigger_aplicar_juros_dia"
    ```sql
    CREATE OR REPLACE FUNCTION aplicar_juros_ao_mudar_dia()
    RETURNS TRIGGER AS $$
    DECLARE
        dias_passados INTEGER;
        juros_calculados INTEGER;
        taxa_juros DECIMAL(5,2) := 2.50; -- 2.5% ao dia
    BEGIN
        IF OLD."dia" != NEW."dia" THEN
            dias_passados := NEW."dia" - OLD."dia";
            UPDATE "inst_banco" 
            SET "valorAtual" = "valorAtual" + FLOOR("valorAtual" * (taxa_juros / 100.0) * dias_passados)
            WHERE "seedMundo" = NEW."seedMundo";
            RAISE NOTICE 'Juros aplicados no mundo %: % dias passaram', NEW."seedMundo", dias_passados;
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_aplicar_juros_dia
        AFTER UPDATE ON "mundo"
        FOR EACH ROW
        EXECUTE FUNCTION aplicar_juros_ao_mudar_dia();
    ```

??? info "Trigger: trigger_validar_armadura_unica"
    ```sql
    CREATE OR REPLACE FUNCTION validar_armadura_especializacao_unica()
    RETURNS TRIGGER AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM "arma" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já está classificado como Arma. Um item não pode ter múltiplas especializações.', NEW."idItem";
        END IF;
        IF EXISTS (SELECT 1 FROM "pocao" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já está classificado como Poção. Um item não pode ter múltiplas especializações.', NEW."idItem";
        END IF;
        UPDATE "item" SET "tipo" = 'Armadura' WHERE "idItem" = NEW."idItem";
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_validar_armadura_unica
        BEFORE INSERT ON "armadura"
        FOR EACH ROW
        EXECUTE FUNCTION validar_armadura_especializacao_unica();
    ```

??? info "Trigger: trigger_validar_pocao_unica"
    ```sql
    CREATE OR REPLACE FUNCTION validar_pocao_especializacao_unica()
    RETURNS TRIGGER AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM "arma" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já está classificado como Arma. Um item não pode ter múltiplas especializações.', NEW."idItem";
        END IF;
        IF EXISTS (SELECT 1 FROM "armadura" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já está classificado como Armadura. Um item não pode ter múltiplas especializações.', NEW."idItem";
        END IF;
        UPDATE "item" SET "tipo" = 'Consumível' WHERE "idItem" = NEW."idItem";
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_validar_pocao_unica
        BEFORE INSERT ON "pocao"
        FOR EACH ROW
        EXECUTE FUNCTION validar_pocao_especializacao_unica();
    ```

??? info "Trigger: trigger_validar_arma_unica"
    ```sql
    CREATE OR REPLACE FUNCTION validar_arma_especializacao_unica()
    RETURNS TRIGGER AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM "armadura" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já está classificado como Armadura. Um item não pode ter múltiplas especializações.', NEW."idItem";
        END IF;
        IF EXISTS (SELECT 1 FROM "pocao" WHERE "idItem" = NEW."idItem") THEN
            RAISE EXCEPTION 'Item ID % já está classificado como Poção. Um item não pode ter múltiplas especializações.', NEW."idItem";
        END IF;
        UPDATE "item" SET "tipo" = 'Arma' WHERE "idItem" = NEW."idItem";
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_validar_arma_unica
        BEFORE INSERT ON "arma"
        FOR EACH ROW
        EXECUTE FUNCTION validar_arma_especializacao_unica();
    ```

??? info "Trigger: trigger_validar_estabelecimento_unico"
    ```sql
    CREATE OR REPLACE FUNCTION validar_estabelecimento_especializacao_unica()
    RETURNS TRIGGER AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM "masmorra" WHERE "idLocal" = NEW."idLocal") THEN
            RAISE EXCEPTION 'Local ID % já está classificado como Masmorra. Um local não pode ter múltiplas especializações.', NEW."idLocal";
        END IF;
        UPDATE "local" SET "tipo" = 'Estabelecimento' WHERE "idLocal" = NEW."idLocal";
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_validar_estabelecimento_unico
        BEFORE INSERT ON "estabelecimento"
        FOR EACH ROW
        EXECUTE FUNCTION validar_estabelecimento_especializacao_unica();
    ```

??? info "Trigger: trigger_validar_masmorra_unica"
    ```sql
    CREATE OR REPLACE FUNCTION validar_masmorra_especializacao_unica()
    RETURNS TRIGGER AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM "estabelecimento" WHERE "idLocal" = NEW."idLocal") THEN
            RAISE EXCEPTION 'Local ID % já está classificado como Estabelecimento. Um local não pode ter múltiplas especializações.', NEW."idLocal";
        END IF;
        UPDATE "local" SET "tipo" = 'Masmorra' WHERE "idLocal" = NEW."idLocal";
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_validar_masmorra_unica
        BEFORE INSERT ON "masmorra"
        FOR EACH ROW
        EXECUTE FUNCTION validar_masmorra_especializacao_unica();
    ```

??? info "Trigger: trigger_remover_especializacoes_item"
    ```sql
    CREATE OR REPLACE FUNCTION remover_especializacoes_item()
    RETURNS TRIGGER AS $$
    BEGIN
        -- Remove o item de todas as tabelas especializadas
        DELETE FROM "arma" WHERE "idItem" = OLD."idItem";
        DELETE FROM "armadura" WHERE "idItem" = OLD."idItem";
        DELETE FROM "pocao" WHERE "idItem" = OLD."idItem";
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_remover_especializacoes_item
        BEFORE DELETE ON "item"
        FOR EACH ROW
        EXECUTE FUNCTION remover_especializacoes_item();
    ```

??? info "Trigger: trigger_remover_especializacoes_local"
    ```sql
    CREATE OR REPLACE FUNCTION remover_especializacoes_local()
    RETURNS TRIGGER AS $$
    BEGIN
        -- Remove o local de todas as tabelas especializadas
        DELETE FROM "estabelecimento" WHERE "idLocal" = OLD."idLocal";
        DELETE FROM "masmorra" WHERE "idLocal" = OLD."idLocal";
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_remover_especializacoes_local
        BEFORE DELETE ON "local"
        FOR EACH ROW
        EXECUTE FUNCTION remover_especializacoes_local();
    ```

??? info "Trigger: trigger_atualizar_tipo_apos_remover_arma"
    ```sql
    CREATE OR REPLACE FUNCTION atualizar_tipo_apos_remover_arma()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM "arma" WHERE "idItem" = OLD."idItem") THEN
            UPDATE "item" SET "tipo" = NULL WHERE "idItem" = OLD."idItem";
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_atualizar_tipo_apos_remover_arma
        AFTER DELETE ON "arma"
        FOR EACH ROW
        EXECUTE FUNCTION atualizar_tipo_apos_remover_arma();
    ```

??? info "Trigger: trigger_atualizar_tipo_apos_remover_armadura"
    ```sql
    CREATE OR REPLACE FUNCTION atualizar_tipo_apos_remover_armadura()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM "armadura" WHERE "idItem" = OLD."idItem") THEN
            UPDATE "item" SET "tipo" = NULL WHERE "idItem" = OLD."idItem";
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_atualizar_tipo_apos_remover_armadura
        AFTER DELETE ON "armadura"
        FOR EACH ROW
        EXECUTE FUNCTION atualizar_tipo_apos_remover_armadura();
    ```

??? info "Trigger: trigger_atualizar_tipo_apos_remover_pocao"
    ```sql
    CREATE OR REPLACE FUNCTION atualizar_tipo_apos_remover_pocao()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM "pocao" WHERE "idItem" = OLD."idItem") THEN
            UPDATE "item" SET "tipo" = NULL WHERE "idItem" = OLD."idItem";
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_atualizar_tipo_apos_remover_pocao
        AFTER DELETE ON "pocao"
        FOR EACH ROW
        EXECUTE FUNCTION atualizar_tipo_apos_remover_pocao();
    ```

??? info "Trigger: trigger_atualizar_tipo_apos_remover_estabelecimento"
    ```sql
    CREATE OR REPLACE FUNCTION atualizar_tipo_apos_remover_estabelecimento()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM "estabelecimento" WHERE "idLocal" = OLD."idLocal") THEN
            UPDATE "local" SET "tipo" = NULL WHERE "idLocal" = OLD."idLocal";
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_atualizar_tipo_apos_remover_estabelecimento
        AFTER DELETE ON "estabelecimento"
        FOR EACH ROW
        EXECUTE FUNCTION atualizar_tipo_apos_remover_estabelecimento();
    ```

??? info "Trigger: trigger_atualizar_tipo_apos_remover_masmorra"
    ```sql
    CREATE OR REPLACE FUNCTION atualizar_tipo_apos_remover_masmorra()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM "masmorra" WHERE "idLocal" = OLD."idLocal") THEN
            UPDATE "local" SET "tipo" = NULL WHERE "idLocal" = OLD."idLocal";
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_atualizar_tipo_apos_remover_masmorra
        AFTER DELETE ON "masmorra"
        FOR EACH ROW
        EXECUTE FUNCTION atualizar_tipo_apos_remover_masmorra();
    ```

??? info "Trigger: trig_validar_arma, trig_validar_armadura, trig_validar_pocao"
    ```sql
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
            UPDATE "item" SET "tipo" = 'Arma' WHERE "idItem" = NEW."idItem";
        ELSIF TG_TABLE_NAME = 'armadura' THEN
            IF EXISTS (SELECT 1 FROM "arma" WHERE "idItem" = NEW."idItem") THEN
                RAISE EXCEPTION 'Item ID % já classificado como Arma. Não pode ser salvo como Armadura.', NEW."idItem";
            END IF;
            IF EXISTS (SELECT 1 FROM "pocao" WHERE "idItem" = NEW."idItem") THEN
                RAISE EXCEPTION 'Item ID % já classificado como Poção. Não pode ser salvo como Armadura.', NEW."idItem";
            END IF;
            UPDATE "item" SET "tipo" = 'Armadura' WHERE "idItem" = NEW."idItem";
        ELSIF TG_TABLE_NAME = 'pocao' THEN
            IF EXISTS (SELECT 1 FROM "arma" WHERE "idItem" = NEW."idItem") THEN
                RAISE EXCEPTION 'Item ID % já classificado como Arma. Não pode ser salvo como Poção.', NEW."idItem";
            END IF;
            IF EXISTS (SELECT 1 FROM "armadura" WHERE "idItem" = NEW."idItem") THEN
                RAISE EXCEPTION 'Item ID % já classificado como Armadura. Não pode ser salvo como Poção.', NEW."idItem";
            END IF;
            UPDATE "item" SET "tipo" = 'Consumível' WHERE "idItem" = NEW."idItem";
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trig_validar_arma
        BEFORE INSERT ON "arma"
        FOR EACH ROW EXECUTE FUNCTION validar_especializacao_item();
    CREATE TRIGGER trig_validar_armadura
        BEFORE INSERT ON "armadura"
        FOR EACH ROW EXECUTE FUNCTION validar_especializacao_item();
    CREATE TRIGGER trig_validar_pocao
        BEFORE INSERT ON "pocao"
        FOR EACH ROW EXECUTE FUNCTION validar_especializacao_item();
    ```

??? info "Trigger: trig_validar_masmorra, trig_validar_estabelecimento"
    ```sql
    CREATE OR REPLACE FUNCTION validar_especializacao_local()
    RETURNS TRIGGER AS $$
    BEGIN
        IF TG_TABLE_NAME = 'masmorra' THEN
            IF EXISTS (SELECT 1 FROM "estabelecimento" WHERE "nomeLocal" = NEW."nomeLocal") THEN
                RAISE EXCEPTION 'Local % já classificado como Estabelecimento. Não pode ser salvo como Masmorra.', NEW."nomeLocal";
            END IF;
            UPDATE "local" SET "tipoLocal" = 'Masmorra' WHERE "nomeLocal" = NEW."nomeLocal";
        ELSIF TG_TABLE_NAME = 'estabelecimento' THEN
            IF EXISTS (SELECT 1 FROM "masmorra" WHERE "nomeLocal" = NEW."nomeLocal") THEN
                RAISE EXCEPTION 'Local % já classificado como Masmorra. Não pode ser salvo como Estabelecimento.', NEW."nomeLocal";
            END IF;
            UPDATE "local" SET "tipoLocal" = 'Estabelecimento' WHERE "nomeLocal" = NEW."nomeLocal";
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trig_validar_masmorra
        BEFORE INSERT ON "masmorra"
        FOR EACH ROW EXECUTE FUNCTION validar_especializacao_local();
    CREATE TRIGGER trig_validar_estabelecimento
        BEFORE INSERT ON "estabelecimento"
        FOR EACH ROW EXECUTE FUNCTION validar_especializacao_local();
    ```

??? info "Trigger: trig_atualizar_tipo_arma, trig_atualizar_tipo_armadura, trig_atualizar_tipo_pocao"
    ```sql
    CREATE OR REPLACE FUNCTION atualizar_tipo_item_apos_delete()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM "arma" WHERE "idItem" = OLD."idItem"
            UNION ALL
            SELECT 1 FROM "armadura" WHERE "idItem" = OLD."idItem"
            UNION ALL  
            SELECT 1 FROM "pocao" WHERE "idItem" = OLD."idItem"
        ) THEN
            UPDATE "item" SET "tipo" = NULL WHERE "idItem" = OLD."idItem";
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trig_atualizar_tipo_arma
        AFTER DELETE ON "arma"
        FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_item_apos_delete();
    CREATE TRIGGER trig_atualizar_tipo_armadura
        AFTER DELETE ON "armadura"
        FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_item_apos_delete();
    CREATE TRIGGER trig_atualizar_tipo_pocao
        AFTER DELETE ON "pocao"
        FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_item_apos_delete();
    ```

??? info "Trigger: trig_atualizar_tipo_masmorra, trig_atualizar_tipo_estabelecimento"
    ```sql
    CREATE OR REPLACE FUNCTION atualizar_tipo_local_apos_delete()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM "masmorra" WHERE "nomeLocal" = OLD."nomeLocal"
            UNION ALL
            SELECT 1 FROM "estabelecimento" WHERE "nomeLocal" = OLD."nomeLocal"
        ) THEN
            UPDATE "local" SET "tipoLocal" = 'Local' WHERE "nomeLocal" = OLD."nomeLocal";
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trig_atualizar_tipo_masmorra
        AFTER DELETE ON "masmorra"
        FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_local_apos_delete();
    CREATE TRIGGER trig_atualizar_tipo_estabelecimento
        AFTER DELETE ON "estabelecimento"
        FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_local_apos_delete();
    ```

??? info "Trigger: trig_deletar_item_especializacao, trig_deletar_local_especializacao"
    ```sql
    CREATE OR REPLACE FUNCTION deletar_especializacao_item()
    RETURNS TRIGGER AS $$
    BEGIN
        DELETE FROM "arma" WHERE "idItem" = OLD."idItem";
        DELETE FROM "armadura" WHERE "idItem" = OLD."idItem";
        DELETE FROM "pocao" WHERE "idItem" = OLD."idItem";
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trig_deletar_item_especializacao
        BEFORE DELETE ON "item"
        FOR EACH ROW EXECUTE FUNCTION deletar_especializacao_item();

    CREATE OR REPLACE FUNCTION deletar_especializacao_local()
    RETURNS TRIGGER AS $$
    BEGIN
        DELETE FROM "masmorra" WHERE "nomeLocal" = OLD."nomeLocal";
        DELETE FROM "estabelecimento" WHERE "nomeLocal" = OLD."nomeLocal";
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trig_deletar_local_especializacao
        BEFORE DELETE ON "local"
        FOR EACH ROW EXECUTE FUNCTION deletar_especializacao_local();
    ```

---

| Data       | Versão | Autor(es)        | Mudanças                                               |
| ---------- | ------ | ---------------- | ------------------------------------------------------ |
| 06/07/2025 | `1.0`  | Todos da Equipe  | Criação da Página e Inserção Triggers                 |
