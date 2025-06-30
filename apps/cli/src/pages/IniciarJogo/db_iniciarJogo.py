from colorama import Fore
from setup.database import connect_to_db
from utils.enterContinue import enter_continue

def local_inicial(local_inicial):
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
                         """, (local_inicial,))
    
    resultadoselect: str = cursorselect.fetchone()
    
    cursorupdate.execute("""UPDATE "jogador"
                   SET "nomeLocal" = %s;
                    """, (resultadoselect[0],))
    connection.commit()
    cursorselect.close()
    cursorupdate.close()
    connection.close()

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
        atualizar_slots_ocupados_inventario(nickname, 1, cursor)
        
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

def atualizar_slots_ocupados_inventario(nickname, id_inventario, cursor):
    """
    Atualiza o número de slots ocupados em um inventário
    """
    cursor.execute("""
        SELECT COUNT(DISTINCT "idItem") as slots_ocupados
        FROM "inst_item"
        WHERE "nickname" = %s AND "idInventario" = %s
    """, (nickname, id_inventario))
    
    slots_ocupados = cursor.fetchone()[0]
    
    cursor.execute("""
        UPDATE "inst_inventario"
        SET "slotOcupado" = %s
        WHERE "nickname" = %s AND "idInventario" = %s
    """, (slots_ocupados, nickname, id_inventario))

def listar_itens_no_chao(nickname):
    """
    Lista todos os itens no chão na localização atual do jogador
    """
    connection = connect_to_db()
    if connection is None:
        return []

    cursor = connection.cursor()
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
        JOIN "jogador" j ON ic."nomeLocal" = j."nomeLocal"
        JOIN "mundo" m ON ic."seedMundo" = m."seedMundo" AND j."nickname" = m."nickname"
        WHERE j."nickname" = %s
        ORDER BY i."nome"
    """, (nickname,))
    
    itens = cursor.fetchall()
    cursor.close()
    connection.close()
    return itens