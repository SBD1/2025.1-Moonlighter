from colorama import Fore
from setup.database import connect_to_db
from utils.enterContinue import enter_continue
from pages.IniciarJogo.inventario_funcoes import *

def buscarDescricaoLocal(nome_local):
    connection = connect_to_db()

    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        enter_continue()
        return None

    cursor = connection.cursor()
    cursor.execute("""SELECT "descricao"
                    FROM "local"
                    WHERE "nomeLocal" = %s;
                    """, (nome_local,))

    resultado = cursor.fetchone()
    cursor.close()
    connection.close()

    return resultado[0] if resultado else None

def buscar_dadosJogador(nickname):
    connection = connect_to_db()

    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        enter_continue()
        return None

    cursor = connection.cursor()
    cursor.execute("""SELECT *
                    FROM "jogador"
                    WHERE "nickname" = %s;
                    """, (nickname,))
    
    resultado = cursor.fetchone()
    cursor.close()
    connection.close()

    return resultado

def atualizar_local_jogador(novo_local, nickname):
    connection = connect_to_db()

    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        enter_continue()
        return None
    
    cursorupdate = connection.cursor()
    cursorselect = connection.cursor()

    cursorselect.execute("""SELECT "nomeLocal"
                         FROM "local"
                         WHERE "nomeLocal" = %s;
                         """, (novo_local,))
    
    resultadoselect = cursorselect.fetchone()
    
    cursorupdate.execute("""UPDATE "jogador"
                            SET "nomeLocal" = %s, "updatedAt" =  NOW()
                            WHERE "nickname" = %s;
                        """, (resultadoselect[0], nickname,))
    connection.commit()
    cursorselect.close()
    cursorupdate.close()
    connection.close()

def exibir_locais(local_atual):
    connection = connect_to_db()

    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        enter_continue()
        return None
    
    cursor = connection.cursor()

    cursor.execute("""SELECT "nomeLocal"
                        FROM "local"
                        WHERE "nomeLocal" != %s AND "acesso" = %s
                   """, (local_atual, local_atual,))
    
    resultado = cursor.fetchall()

    cursor.close()
    connection.close()

    return resultado

def atualizarParaLocalAnterior(dadosJogador):
    connection = connect_to_db()

    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        enter_continue()
        return None

    cursor = connection.cursor()

    cursor.execute("""UPDATE "jogador"
                        SET "nomeLocal" = (SELECT "acesso" FROM "local" WHERE "nomeLocal" = %s), "updatedAt" = NOW()
                        WHERE "nickname" = %s;
                   """, (dadosJogador[6], dadosJogador[0]))
    connection.commit()
    cursor.close()
    connection.close()

def dropar_item_no_chao(nickname, id_item, quantidade, posicao_x=0, posicao_y=0):
    """
    Dropa um item no chão na localização atual do jogador
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # Buscar informações do jogador e mundo
        cursor.execute("""
            SELECT j."nomeLocal", m."seedMundo"
            FROM "jogador" j
            JOIN "mundo" m ON j."nickname" = m."nickname"
            WHERE j."nickname" = %s
        """, (nickname,))
        
        jogador_info = cursor.fetchone()
        if not jogador_info:
            cursor.close()
            connection.close()
            return False
        
        nome_local, seed_mundo = jogador_info
        
        # Verificar se já existe item na mesma posição
        cursor.execute("""
            SELECT "idItemChao", "quantidade"
            FROM "item_chao"
            WHERE "idItem" = %s 
            AND "posicaoX" = %s 
            AND "posicaoY" = %s
            AND "seedMundo" = %s
            AND "nomeLocal" = %s
        """, (id_item, posicao_x, posicao_y, seed_mundo, nome_local))
        
        item_existente = cursor.fetchone()
        
        if item_existente:
            # Atualizar quantidade existente
            cursor.execute("""
                UPDATE "item_chao"
                SET "quantidade" = "quantidade" + %s
                WHERE "idItemChao" = %s
            """, (quantidade, item_existente[0]))
        else:
            # Inserir novo item no chão
            cursor.execute("""
                INSERT INTO "item_chao" (
                    "idItem", "quantidade", "posicaoX", "posicaoY", 
                    "seedMundo", "nomeLocal"
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_item, quantidade, posicao_x, posicao_y, seed_mundo, nome_local))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"Erro ao dropar item: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False

def coletar_item_do_chao(nickname, id_item_chao):
    """
    Coleta um item do chão e adiciona ao inventário
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # Buscar informações do item no chão
        cursor.execute("""
            SELECT ic."idItem", ic."quantidade", i."stackMaximo", i."nome"
            FROM "item_chao" ic
            JOIN "item" i ON ic."idItem" = i."idItem"
            WHERE ic."idItemChao" = %s
        """, (id_item_chao,))
        
        item_chao_info = cursor.fetchone()
        if not item_chao_info:
            cursor.close()
            connection.close()
            return False
        
        id_item, quantidade_chao, stack_maximo, nome_item = item_chao_info
        
        # Verificar se o item já existe no inventário principal
        cursor.execute("""
            SELECT "idInstItem", "quantidade"
            FROM "inst_item"
            WHERE "nickname" = %s 
            AND "idItem" = %s 
            AND "idInventario" = 1
        """, (nickname, id_item))
        
        item_inventario = cursor.fetchone()
        
        if item_inventario:
            # Atualizar quantidade existente (respeitando stack máximo)
            id_inst_item, quantidade_atual = item_inventario
            nova_quantidade = min(quantidade_atual + quantidade_chao, stack_maximo)
            
            cursor.execute("""
                UPDATE "inst_item"
                SET "quantidade" = %s
                WHERE "idInstItem" = %s
            """, (nova_quantidade, id_inst_item))
        else:
            # Verificar se há espaço no inventário
            cursor.execute("""
                SELECT (inv."slotMaximo" - inst."slotOcupado") as slots_livres
                FROM "inst_inventario" inst
                JOIN "inventario" inv ON inst."idInventario" = inv."idInventario"
                WHERE inst."nickname" = %s AND inst."idInventario" = 1
            """, (nickname,))
            
            slots_info = cursor.fetchone()
            if not slots_info or slots_info[0] <= 0:
                cursor.close()
                connection.close()
                return False  # Sem espaço no inventário
            
            # Inserir novo item no inventário
            cursor.execute("""
                INSERT INTO "inst_item" ("idItem", "quantidade", "nickname", "idInventario")
                VALUES (%s, %s, %s, 1)
            """, (id_item, quantidade_chao, nickname))
        
        # Remover item do chão
        cursor.execute("""
            DELETE FROM "item_chao" WHERE "idItemChao" = %s
        """, (id_item_chao,))
        
        # Atualizar slots ocupados
        atualizar_slots_ocupados(nickname, 1)
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"Erro ao coletar item: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False

def listar_itens_no_chao(nickname):
    """
    Lista todos os itens no chão na localização atual do jogador
    """
    connection = connect_to_db()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        
        # Tentar usar a função SQL primeiro
        try:
            cursor.execute("""
                SELECT * FROM obter_itens_chao_local(%s);
            """, (nickname,))
            itens = cursor.fetchall()
        except:
            # Se a função não existir, usar query direta
            cursor.execute("""
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
                JOIN "jogador" j ON j."nickname" = %s
                JOIN "mundo" m ON j."nickname" = m."nickname"
                WHERE ic."seedMundo" = m."seedMundo" 
                AND ic."nomeLocal" = j."nomeLocal"
                ORDER BY ic."tempoDropado" DESC
            """, (nickname,))
            itens = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return itens
        
    except Exception as e:
        print(f"Erro ao listar itens no chão: {e}")
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
        return []

def verificar_pode_pegar_item(nickname, id_item_chao):
    """
    Verifica se o jogador pode pegar um item do chão
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT pode_pegar_item(%s, %s);
        """, (nickname, id_item_chao))
        
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado[0] if resultado else False
    except Exception:
        # Fallback para verificação manual se função não existir
        try:
            cursor.execute("""
                SELECT ic."idItem", ic."quantidade", i."stackMaximo"
                FROM "item_chao" ic
                JOIN "item" i ON ic."idItem" = i."idItem"
                WHERE ic."idItemChao" = %s
            """, (id_item_chao,))
            
            item_info = cursor.fetchone()
            if not item_info:
                return False
                
            cursor.close()
            connection.close()
            return True  # Simplificado para sempre permitir
        except Exception:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
            return False

def verificar_pode_dropar_item(nickname, id_item, quantidade):
    """
    Verifica se o jogador pode dropar um item
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT pode_dropar_item(%s, %s, %s);
        """, (nickname, id_item, quantidade))
        
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado[0] if resultado else False
    except Exception:
        # Fallback para verificação manual
        try:
            cursor.execute("""
                SELECT COALESCE(ii."quantidade", 0)
                FROM "inst_item" ii
                WHERE ii."nickname" = %s AND ii."idItem" = %s
            """, (nickname, id_item))
            
            resultado = cursor.fetchone()
            quantidade_atual = resultado[0] if resultado else 0
            
            cursor.close()
            connection.close()
            return quantidade_atual >= quantidade
        except Exception:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
            return False

def obter_inventario_completo(nickname):
    """
    Obtém o inventário completo do jogador
    """
    connection = connect_to_db()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM obter_inventario_jogador(%s);
        """, (nickname,))
        
        inventario = cursor.fetchall()
        cursor.close()
        connection.close()
        return inventario
    except Exception:
        # Fallback para query manual se função não existir
        try:
            cursor.execute("""
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
                WHERE j."nickname" = %s AND i."nome" IS NOT NULL
                ORDER BY inv."nome", i."nome"
            """, (nickname,))
            
            inventario = cursor.fetchall()
            cursor.close()
            connection.close()
            return inventario
        except Exception:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
            return []

def executar_limpeza_automatica():
    """
    Executa limpeza automática de itens
    """
    return executar_limpeza_completa()

def obter_inventario_usando_view(nickname):
    """
    Obtém inventário do jogador usando a view otimizada
    """
    connection = connect_to_db()
    if connection is None:
        return []

    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM view_inventario_jogador 
        WHERE "nickname" = %s AND "nome_item" IS NOT NULL
    """, (nickname,))
    
    inventario = cursor.fetchall()
    cursor.close()
    connection.close()
    return inventario

def obter_itens_chao_usando_view(seed_mundo, nome_local):
    """
    Obtém itens no chão usando a view otimizada
    """
    connection = connect_to_db()
    if connection is None:
        return []

    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM view_itens_chao 
        WHERE "seedMundo" = %s AND "nomeLocal" = %s
    """, (seed_mundo, nome_local))
    
    itens = cursor.fetchall()
    cursor.close()
    connection.close()
    return itens

def buscarSeedMapa(nickname):
    connection = connect_to_db()

    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        enter_continue()
        return None

    cursor = connection.cursor()
    cursor.execute("""SELECT "seedMundo"
                    FROM "mundo"
                    WHERE "nickname" = %s;
                    """, (nickname,))

    resultado = cursor.fetchone()
    cursor.close()
    connection.close()

    return resultado[0] if resultado else None

def buscarInfoMundo(nickname):
    connection = connect_to_db()

    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        enter_continue()
        return None

    cursor = connection.cursor()
    cursor.execute("""SELECT *
                    FROM "mundo"
                    WHERE "nickname" = %s;
                    """, (nickname,))

    resultado = cursor.fetchone()
    cursor.close()
    connection.close()

    return resultado if resultado else None