"""
Funções Auxiliares para Sistema de Inventário
Data: 30/06/2025
Descrição: Funções para gerenciamento completo do inventário
"""

from colorama import Fore, Style
from setup.database import connect_to_db
from utils.enterContinue import enter_continue
import random
from datetime import datetime, timedelta

def inicializar_dados_inventario():
    """
    Inicializa dados básicos necessários para o sistema de inventário
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # Verificar e inserir tipos de inventário padrão
        inventarios = [
            ('Mochila Principal', 20),
            ('Equipamentos', 10),
            ('Baú da Casa', 40)
        ]
        
        for nome, slots in inventarios:
            cursor.execute("""
                INSERT INTO "inventario" ("nome", "slotMaximo") 
                SELECT %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM "inventario" WHERE "nome" = %s
                );
            """, (nome, slots, nome))
        
        # Verificar e inserir efeitos básicos
        efeitos = [
            ('Cura Básica', 'Restaura pontos de vida', 'Cura', 20, 0),
            ('Força Básica', 'Aumenta o ataque temporariamente', 'Buff', 5, 3),
            ('Proteção Básica', 'Aumenta a defesa', 'Buff', 3, 0)
        ]
        
        for nome, desc, tipo, valor, duracao in efeitos:
            cursor.execute("""
                INSERT INTO "efeito" ("nome", "descricao", "tipo", "valor", "duracaoTurnos") 
                SELECT %s, %s, %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM "efeito" WHERE "nome" = %s
                );
            """, (nome, desc, tipo, valor, duracao, nome))
        
        # Verificar e inserir itens básicos
        itens = [
            ('Espada de Madeira', 'Uma espada básica feita de madeira', 'Arma', 10, 'Comum', 1, None),
            ('Armadura de Couro', 'Uma armadura simples de couro', 'Armadura', 15, 'Comum', 1, None),
            ('Poção de Vida Pequena', 'Restaura uma pequena quantidade de HP', 'Consumível', 5, 'Comum', 10, 1),
            ('Espada de Ferro', 'Uma espada mais resistente feita de ferro', 'Arma', 25, 'Comum', 1, None),
            ('Armadura de Ferro', 'Uma armadura resistente de ferro', 'Armadura', 40, 'Comum', 1, None),
            ('Poção de Vida Grande', 'Restaura uma grande quantidade de HP', 'Consumível', 15, 'Comum', 5, 1),
            ('Cristal Mágico', 'Um cristal com propriedades mágicas', 'Material', 50, 'Raro', 20, None),
            ('Pão', 'Alimento básico que restaura um pouco de energia', 'Consumível', 2, 'Comum', 50, None)
        ]
        
        for nome, desc, tipo, preco, cultura, stack, efeito in itens:
            cursor.execute("""
                INSERT INTO "item" ("nome", "descricao", "tipo", "precoBase", "cultura", "stackMaximo", "idEfeito") 
                SELECT %s, %s, %s, %s, %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM "item" WHERE "nome" = %s
                );
            """, (nome, desc, tipo, preco, cultura, stack, efeito, nome))
        
        # Verificar e inserir dados específicos das armas
        armas = [
            (1, '1d6', 0.05, 1, 2, 'Espada'),
            (4, '1d8', 0.10, 1, 2, 'Espada')
        ]
        
        for id_item, dado, critico, mult, mult_crit, tipo_arma in armas:
            cursor.execute("""
                INSERT INTO "arma" ("idItem", "dadoAtaque", "chanceCritico", "multiplicador", "multiplicadorCritico", "tipoArma") 
                SELECT %s, %s, %s, %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM "arma" WHERE "idItem" = %s
                ) AND EXISTS (
                    SELECT 1 FROM "item" WHERE "idItem" = %s
                );
            """, (id_item, dado, critico, mult, mult_crit, tipo_arma, id_item, id_item))
        
        # Verificar e inserir dados específicos das armaduras
        armaduras = [
            (2, '1d4', 2, 1, 0, 'Peito'),
            (5, '1d6', 3, 2, 1, 'Peito')
        ]
        
        for id_item, dado, def_pass, crit_def, bonus, tipo_arm in armaduras:
            cursor.execute("""
                INSERT INTO "armadura" ("idItem", "dadoDefesa", "defesaPassiva", "criticoDefensivo", "bonusDefesa", "tipoArmadura") 
                SELECT %s, %s, %s, %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM "armadura" WHERE "idItem" = %s
                ) AND EXISTS (
                    SELECT 1 FROM "item" WHERE "idItem" = %s
                );
            """, (id_item, dado, def_pass, crit_def, bonus, tipo_arm, id_item, id_item))
        
        # Verificar e inserir dados específicos das poções
        pocoes = [
            (3, 0),
            (6, 0),
            (8, 0)
        ]
        
        for id_item, duracao in pocoes:
            cursor.execute("""
                INSERT INTO "pocao" ("idItem", "duracaoTurnos") 
                SELECT %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM "pocao" WHERE "idItem" = %s
                ) AND EXISTS (
                    SELECT 1 FROM "item" WHERE "idItem" = %s
                );
            """, (id_item, duracao, id_item, id_item))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        # Criar views do sistema
        if not criar_views_inventario():
            print("Aviso: Erro ao criar views do inventário")
        
        # Criar funções SQL do inventário
        if not criar_funcoes_sql_inventario():
            print("Aviso: Erro ao criar funções SQL do inventário")
        
        # Criar triggers de especialização
        if not criar_triggers_especializacao():
            print("Aviso: Erro ao criar triggers de especialização")
        
        return True
        
    except Exception as e:
        print(f"Erro ao inicializar dados do inventário: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False

def criar_inventarios_jogador(nickname):
    """
    Cria os inventários padrão para um novo jogador
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # Buscar IDs dos inventários padrão
        cursor.execute("""
            SELECT "idInventario" FROM "inventario" 
            WHERE "nome" IN ('Mochila Principal', 'Equipamentos', 'Baú da Casa')
            ORDER BY "nome"
        """)
        
        inventarios_ids = cursor.fetchall()
        
        if len(inventarios_ids) < 3:
            print("Erro: Nem todos os inventários padrão foram encontrados")
            return False
        
        # Criar inventários para o jogador
        for (id_inventario,) in inventarios_ids:
            cursor.execute("""
                INSERT INTO "inst_inventario" ("idInventario", "nickname", "slotOcupado") 
                SELECT %s, %s, 0
                WHERE NOT EXISTS (
                    SELECT 1 FROM "inst_inventario" 
                    WHERE "idInventario" = %s AND "nickname" = %s
                );
            """, (id_inventario, nickname, id_inventario, nickname))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"Erro ao criar inventários do jogador: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False

def atualizar_slots_ocupados(nickname, id_inventario):
    """
    Atualiza o número de slots ocupados em um inventário
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # Contar itens únicos no inventário
        cursor.execute("""
            SELECT COUNT(DISTINCT "idItem") as slots_ocupados
            FROM "inst_item"
            WHERE "nickname" = %s AND "idInventario" = %s
        """, (nickname, id_inventario))
        
        slots_ocupados = cursor.fetchone()[0]
        
        # Atualizar registro
        cursor.execute("""
            UPDATE "inst_inventario"
            SET "slotOcupado" = %s
            WHERE "nickname" = %s AND "idInventario" = %s
        """, (slots_ocupados, nickname, id_inventario))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"Erro ao atualizar slots ocupados: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False

def validar_item_no_inventario(id_item, id_inventario):
    """
    Valida se um item pode ser colocado em um inventário específico
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # Buscar tipo do item e nome do inventário
        cursor.execute("""
            SELECT i."tipo", inv."nome"
            FROM "item" i
            CROSS JOIN "inventario" inv
            WHERE i."idItem" = %s AND inv."idInventario" = %s
        """, (id_item, id_inventario))
        
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not resultado:
            return False
        
        tipo_item, nome_inventario = resultado
        
        # Validar regras por tipo de inventário
        if nome_inventario == 'Equipamentos':
            return tipo_item in ['Arma', 'Armadura']
        
        return True
        
    except Exception as e:
        print(f"Erro ao validar item no inventário: {e}")
        cursor.close()
        connection.close()
        return False

def validar_categoria_inventario(id_item, id_inventario):
    """
    Valida se um item pode ser colocado em um inventário específico baseado na categoria
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # Buscar tipo do inventário e tipo do item
        cursor.execute("""
            SELECT inv."nome", i."tipo"
            FROM "inventario" inv, "item" i
            WHERE inv."idInventario" = %s AND i."idItem" = %s
        """, (id_inventario, id_item))
        
        resultado = cursor.fetchone()
        if not resultado:
            return False
        
        tipo_inventario, tipo_item = resultado
        
        # Regras de categoria
        if tipo_inventario == 'Equipamentos':
            # Apenas armas e armaduras podem ir para inventário de equipamentos
            if tipo_item not in ['Arma', 'Armadura']:
                return False
        elif tipo_inventario == 'Mochila Principal':
            # Mochila principal aceita tudo exceto equipamentos já equipados
            pass
        elif tipo_inventario == 'Baú da Casa':
            # Baú da casa aceita qualquer item
            pass
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"Erro ao validar categoria: {e}")
        if connection:
            cursor.close()
            connection.close()
        return False

def criar_views_inventario():
    """
    Cria views básicas para consultas do inventário
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # View básica para itens no chão
        cursor.execute("""
            CREATE OR REPLACE VIEW view_itens_chao AS
            SELECT 
                ic."idItemChao",
                i."nome" AS "nome_item",
                ic."quantidade",
                ic."posicaoX",
                ic."posicaoY",
                ic."nomeLocal",
                ic."seedMundo",
                ic."tempoDropado",
                i."descricao"
            FROM "item_chao" ic
            JOIN "item" i ON ic."idItem" = i."idItem"
            ORDER BY ic."tempoDropado" DESC;
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"Erro ao criar views: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False

def executar_limpeza_completa():
    """
    Executa uma limpeza completa do sistema
    """
    itens_zero = limpar_itens_quantidade_zero()
    itens_expirados = limpar_itens_expirados()
    
    return itens_zero + itens_expirados

def limpar_itens_quantidade_zero():
    """
    Remove itens com quantidade zero do inventário
    """
    connection = connect_to_db()
    if connection is None:
        return 0

    try:
        cursor = connection.cursor()
        
        # Remover itens com quantidade zero
        cursor.execute("""
            DELETE FROM "inst_item" 
            WHERE "quantidade" <= 0
        """)
        
        itens_removidos = cursor.rowcount
        connection.commit()
        cursor.close()
        connection.close()
        return itens_removidos
        
    except Exception as e:
        print(f"Erro ao limpar itens com quantidade zero: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return 0

def limpar_itens_expirados():
    """
    Remove itens expirados do chão
    """
    connection = connect_to_db()
    if connection is None:
        return 0

    try:
        cursor = connection.cursor()
        
        # Remover itens expirados do chão
        cursor.execute("""
            DELETE FROM "item_chao" 
            WHERE "tempoExpiracao" IS NOT NULL 
            AND "tempoExpiracao" < CURRENT_TIMESTAMP
        """)
        
        itens_removidos = cursor.rowcount
        connection.commit()
        cursor.close()
        connection.close()
        return itens_removidos
        
    except Exception as e:
        print(f"Erro ao limpar itens expirados: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return 0

def criar_triggers_especializacao():
    """
    Cria triggers para manter integridade entre tabelas generalizadas e especializadas
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # =====================================
        # TRIGGERS PARA ITEM E SUAS ESPECIALIZAÇÕES
        # =====================================
        
        # Trigger para prevenir salvamento de item em múltiplas especializações
        cursor.execute("""
            CREATE OR REPLACE FUNCTION validar_especializacao_item()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Verificar se item já existe em outra especialização
                IF TG_TABLE_NAME = 'arma' THEN
                    IF EXISTS (SELECT 1 FROM "armadura" WHERE "idItem" = NEW."idItem") THEN
                        RAISE EXCEPTION 'Item já classificado como Armadura. Não pode ser salvo como Arma.';
                    END IF;
                    IF EXISTS (SELECT 1 FROM "pocao" WHERE "idItem" = NEW."idItem") THEN
                        RAISE EXCEPTION 'Item já classificado como Poção. Não pode ser salvo como Arma.';
                    END IF;
                    
                ELSIF TG_TABLE_NAME = 'armadura' THEN
                    IF EXISTS (SELECT 1 FROM "arma" WHERE "idItem" = NEW."idItem") THEN
                        RAISE EXCEPTION 'Item já classificado como Arma. Não pode ser salvo como Armadura.';
                    END IF;
                    IF EXISTS (SELECT 1 FROM "pocao" WHERE "idItem" = NEW."idItem") THEN
                        RAISE EXCEPTION 'Item já classificado como Poção. Não pode ser salvo como Armadura.';
                    END IF;
                    
                ELSIF TG_TABLE_NAME = 'pocao' THEN
                    IF EXISTS (SELECT 1 FROM "arma" WHERE "idItem" = NEW."idItem") THEN
                        RAISE EXCEPTION 'Item já classificado como Arma. Não pode ser salvo como Poção.';
                    END IF;
                    IF EXISTS (SELECT 1 FROM "armadura" WHERE "idItem" = NEW."idItem") THEN
                        RAISE EXCEPTION 'Item já classificado como Armadura. Não pode ser salvo como Poção.';
                    END IF;
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Aplicar triggers nas tabelas de especialização de item
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_validar_arma ON "arma";
            CREATE TRIGGER trig_validar_arma
                BEFORE INSERT ON "arma"
                FOR EACH ROW EXECUTE FUNCTION validar_especializacao_item();
        """)
        
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_validar_armadura ON "armadura";
            CREATE TRIGGER trig_validar_armadura
                BEFORE INSERT ON "armadura"
                FOR EACH ROW EXECUTE FUNCTION validar_especializacao_item();
        """)
        
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_validar_pocao ON "pocao";
            CREATE TRIGGER trig_validar_pocao
                BEFORE INSERT ON "pocao"
                FOR EACH ROW EXECUTE FUNCTION validar_especializacao_item();
        """)
        
        # =====================================
        # TRIGGERS PARA LOCAL E SUAS ESPECIALIZAÇÕES
        # =====================================
        
        # Trigger para prevenir salvamento de local em múltiplas especializações
        cursor.execute("""
            CREATE OR REPLACE FUNCTION validar_especializacao_local()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Verificar se local já existe em outra especialização
                IF TG_TABLE_NAME = 'masmorra' THEN
                    IF EXISTS (SELECT 1 FROM "estabelecimento" WHERE "nomeLocal" = NEW."nomeLocal") THEN
                        RAISE EXCEPTION 'Local já classificado como Estabelecimento. Não pode ser salvo como Masmorra.';
                    END IF;
                    
                ELSIF TG_TABLE_NAME = 'estabelecimento' THEN
                    IF EXISTS (SELECT 1 FROM "masmorra" WHERE "nomeLocal" = NEW."nomeLocal") THEN
                        RAISE EXCEPTION 'Local já classificado como Masmorra. Não pode ser salvo como Estabelecimento.';
                    END IF;
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Aplicar triggers nas tabelas de especialização de local
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_validar_masmorra ON "masmorra";
            CREATE TRIGGER trig_validar_masmorra
                BEFORE INSERT ON "masmorra"
                FOR EACH ROW EXECUTE FUNCTION validar_especializacao_local();
        """)
        
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_validar_estabelecimento ON "estabelecimento";
            CREATE TRIGGER trig_validar_estabelecimento
                BEFORE INSERT ON "estabelecimento"
                FOR EACH ROW EXECUTE FUNCTION validar_especializacao_local();
        """)
        
        # =====================================
        # TRIGGERS PARA DELEÇÃO EM CASCATA
        # =====================================
        
        # Trigger para deletar especializações quando item generalizado é deletado
        cursor.execute("""
            CREATE OR REPLACE FUNCTION deletar_especializacao_item()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Deletar da tabela de especialização correspondente
                DELETE FROM "arma" WHERE "idItem" = OLD."idItem";
                DELETE FROM "armadura" WHERE "idItem" = OLD."idItem";
                DELETE FROM "pocao" WHERE "idItem" = OLD."idItem";
                
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_deletar_item_especializacao ON "item";
            CREATE TRIGGER trig_deletar_item_especializacao
                BEFORE DELETE ON "item"
                FOR EACH ROW EXECUTE FUNCTION deletar_especializacao_item();
        """)
        
        # Trigger para deletar especializações quando local generalizado é deletado
        cursor.execute("""
            CREATE OR REPLACE FUNCTION deletar_especializacao_local()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Deletar da tabela de especialização correspondente
                DELETE FROM "masmorra" WHERE "nomeLocal" = OLD."nomeLocal";
                DELETE FROM "estabelecimento" WHERE "nomeLocal" = OLD."nomeLocal";
                
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_deletar_local_especializacao ON "local";
            CREATE TRIGGER trig_deletar_local_especializacao
                BEFORE DELETE ON "local"
                FOR EACH ROW EXECUTE FUNCTION deletar_especializacao_local();
        """)
        
        # =====================================
        # TRIGGERS PARA ATUALIZAR TIPO QUANDO ESPECIALIZAÇÃO É DELETADA
        # =====================================
        
        # Trigger para atualizar tipo do item quando especialização é deletada
        cursor.execute("""
            CREATE OR REPLACE FUNCTION atualizar_tipo_item_apos_delete()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Atualizar tipo para genérico quando especialização é deletada
                UPDATE "item" SET "tipo" = NULL WHERE "idItem" = OLD."idItem";
                
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_atualizar_tipo_arma ON "arma";
            CREATE TRIGGER trig_atualizar_tipo_arma
                AFTER DELETE ON "arma"
                FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_item_apos_delete();
        """)
        
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_atualizar_tipo_armadura ON "armadura";
            CREATE TRIGGER trig_atualizar_tipo_armadura
                AFTER DELETE ON "armadura"
                FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_item_apos_delete();
        """)
        
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_atualizar_tipo_pocao ON "pocao";
            CREATE TRIGGER trig_atualizar_tipo_pocao
                AFTER DELETE ON "pocao"
                FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_item_apos_delete();
        """)
        
        # Trigger para atualizar tipo do local quando especialização é deletada
        cursor.execute("""
            CREATE OR REPLACE FUNCTION atualizar_tipo_local_apos_delete()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Atualizar tipo para genérico quando especialização é deletada
                UPDATE "local" SET "tipoLocal" = 'Local' WHERE "nomeLocal" = OLD."nomeLocal";
                
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_atualizar_tipo_masmorra ON "masmorra";
            CREATE TRIGGER trig_atualizar_tipo_masmorra
                AFTER DELETE ON "masmorra"
                FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_local_apos_delete();
        """)
        
        cursor.execute("""
            DROP TRIGGER IF EXISTS trig_atualizar_tipo_estabelecimento ON "estabelecimento";
            CREATE TRIGGER trig_atualizar_tipo_estabelecimento
                AFTER DELETE ON "estabelecimento"
                FOR EACH ROW EXECUTE FUNCTION atualizar_tipo_local_apos_delete();
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"Erro ao criar triggers de especialização: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False

def criar_funcoes_sql_inventario():
    """
    Cria funções SQL para operações do inventário
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # Função para obter itens no chão por localização do jogador
        cursor.execute("""
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
        """)
        
        # Função para obter inventário completo do jogador
        cursor.execute("""
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
                LEFT JOIN "item" i ON ii."idItem" = i."idItem"
                WHERE j."nickname" = p_nickname AND i."nome" IS NOT NULL
                ORDER BY inv."nome", i."nome";
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Função para verificar se jogador pode pegar item
        cursor.execute("""
            CREATE OR REPLACE FUNCTION pode_pegar_item(p_nickname VARCHAR, p_id_item_chao INTEGER)
            RETURNS BOOLEAN AS $$
            DECLARE
                v_id_item INTEGER;
                v_quantidade_chao SMALLINT;
                v_slots_livres INTEGER;
                v_stack_maximo SMALLINT;
                v_quantidade_atual SMALLINT := 0;
            BEGIN
                -- Buscar informações do item no chão
                SELECT ic."idItem", ic."quantidade", i."stackMaximo"
                INTO v_id_item, v_quantidade_chao, v_stack_maximo
                FROM "item_chao" ic
                JOIN "item" i ON ic."idItem" = i."idItem"
                WHERE ic."idItemChao" = p_id_item_chao;
                
                IF NOT FOUND THEN
                    RETURN FALSE;
                END IF;
                
                -- Verificar se item já existe no inventário
                SELECT COALESCE(ii."quantidade", 0)
                INTO v_quantidade_atual
                FROM "inst_item" ii
                WHERE ii."nickname" = p_nickname 
                AND ii."idItem" = v_id_item 
                AND ii."idInventario" = 1; -- Inventário principal
                
                -- Se item existe, verificar se pode adicionar mais
                IF v_quantidade_atual > 0 THEN
                    RETURN (v_quantidade_atual + v_quantidade_chao) <= v_stack_maximo;
                END IF;
                
                -- Se item não existe, verificar se há espaço
                SELECT (inv."slotMaximo" - iinv."slotOcupado")
                INTO v_slots_livres
                FROM "inst_inventario" iinv
                JOIN "inventario" inv ON iinv."idInventario" = inv."idInventario"
                WHERE iinv."nickname" = p_nickname AND iinv."idInventario" = 1;
                
                RETURN v_slots_livres > 0;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Função para verificar se jogador pode dropar item
        cursor.execute("""
            CREATE OR REPLACE FUNCTION pode_dropar_item(p_nickname VARCHAR, p_id_item INTEGER, p_quantidade SMALLINT)
            RETURNS BOOLEAN AS $$
            DECLARE
                v_quantidade_atual SMALLINT := 0;
            BEGIN
                -- Verificar se jogador tem item suficiente
                SELECT COALESCE(ii."quantidade", 0)
                INTO v_quantidade_atual
                FROM "inst_item" ii
                WHERE ii."nickname" = p_nickname 
                AND ii."idItem" = p_id_item;
                
                RETURN v_quantidade_atual >= p_quantidade;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Função para limpeza automática
        cursor.execute("""
            CREATE OR REPLACE FUNCTION limpar_itens_expirados()
            RETURNS INTEGER AS $$
            DECLARE
                v_itens_removidos INTEGER := 0;
            BEGIN
                -- Remover itens expirados
                DELETE FROM "item_chao" 
                WHERE "tempoExpiracao" IS NOT NULL 
                AND "tempoExpiracao" < CURRENT_TIMESTAMP;
                
                GET DIAGNOSTICS v_itens_removidos = ROW_COUNT;
                
                -- Remover itens com quantidade zero
                DELETE FROM "inst_item" WHERE "quantidade" <= 0;
                DELETE FROM "item_chao" WHERE "quantidade" <= 0;
                
                RETURN v_itens_removidos;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"Erro ao criar funções SQL: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False

