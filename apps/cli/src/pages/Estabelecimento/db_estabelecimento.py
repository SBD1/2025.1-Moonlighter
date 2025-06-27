from setup.database import connect_to_db
from colorama import Fore

# FUNÇÕES SIMPLIFICADAS DA FORJA (usando nickname diretamente)

def verificar_instancia_forja_por_jogador(nickname):
    """
    Verifica se uma instância de forja já existe para um jogador
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) > 0 
            FROM "inst_forja" ifj
            JOIN "mundo" m ON ifj."seedMundo" = m."seedMundo"
            WHERE m."nickname" = %s
        """, (nickname,))
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado[0] if resultado else False
    except Exception as e:
        print(Fore.RED + f"Erro ao verificar instância da forja: {e}")
        if connection:
            connection.close()
        return None

def criar_instancia_forja_por_jogador(nickname, nome_local, id_npc):
    """
    Cria instância da forja diretamente pelo nickname
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO "inst_forja" ("seedMundo", "nomeLocal", "idNPC")
            SELECT m."seedMundo", %s, %s
            FROM "mundo" m
            WHERE m."nickname" = %s
            AND NOT EXISTS (
                SELECT 1 FROM "inst_forja" ifj 
                WHERE ifj."seedMundo" = m."seedMundo"
            )
        """, (nome_local, id_npc, nickname))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(Fore.RED + f"Erro ao criar instância da forja: {e}")
        if connection:
            connection.rollback()
            connection.close()
        return False

def visualizar_itens_forja_por_jogador(nickname):
    """
    Visualiza itens disponíveis para fabricar na forja
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT i."idItem", i."nome", i."precoBase", i."descricao"
            FROM "item" i
            JOIN "receita" r ON i."idItem" = r."idItemFabricado"
            ORDER BY i."nome"
        """)
        resultado = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultado
    except Exception as e:
        print(Fore.RED + f"Erro ao visualizar itens da forja: {e}")
        if connection:
            connection.close()
        return None

def forjar_item_por_jogador(nickname, item_id):
    """
    Forja um item para o jogador
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    try:
        cursor = connection.cursor()
        
        # Verificar se o jogador tem ouro suficiente
        cursor.execute("""
            SELECT j."ouro", i."precoBase"
            FROM "jogador" j
            CROSS JOIN "item" i
            WHERE j."nickname" = %s AND i."idItem" = %s
        """, (nickname, item_id))
        
        resultado = cursor.fetchone()
        if not resultado:
            print(Fore.RED + "Jogador ou item não encontrado!")
            return False
            
        ouro_jogador, preco_item = resultado
        
        if ouro_jogador < preco_item:
            print(Fore.RED + f"Ouro insuficiente! Você tem {ouro_jogador} ouros, mas precisa de {preco_item} ouros.")
            return False
        
        # Deduzir ouro do jogador
        cursor.execute("""
            UPDATE "jogador"
            SET "ouro" = "ouro" - %s
            WHERE "nickname" = %s
        """, (preco_item, nickname))
        
        # TODO: Adicionar item ao inventário do jogador
        # TODO: Verificar materiais necessários
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(Fore.RED + f"Erro ao forjar item: {e}")
        if connection:
            connection.rollback()
            connection.close()
        return False


# FUNÇÕES SIMPLIFICADAS DO BANCO (usando nickname diretamente)


def verificar_instancia_banco_por_jogador(nickname):
    """
    Verifica se uma instância de banco já existe para um jogador
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) > 0 
            FROM "inst_banco" ib
            JOIN "mundo" m ON ib."seedMundo" = m."seedMundo"
            WHERE m."nickname" = %s
        """, (nickname,))
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado[0] if resultado else False
    except Exception as e:
        print(Fore.RED + f"Erro ao verificar instância do banco: {e}")
        if connection:
            connection.close()
        return None

def criar_instancia_banco_por_jogador(nickname, nome_local, id_npc, valor_entrada=0):
    """
    Cria instância do banco diretamente pelo nickname
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO "inst_banco" ("seedMundo", "nomeLocal", "idNPC", "valorEntrada", "valorAtual")
            SELECT m."seedMundo", %s, %s, %s, %s
            FROM "mundo" m
            WHERE m."nickname" = %s
            AND NOT EXISTS (
                SELECT 1 FROM "inst_banco" ib 
                WHERE ib."seedMundo" = m."seedMundo"
            )
        """, (nome_local, id_npc, valor_entrada, valor_entrada, nickname))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(Fore.RED + f"Erro ao criar instância do banco: {e}")
        if connection:
            connection.rollback()
            connection.close()
        return False

def visualizar_saldo_banco_por_jogador(nickname):
    """
    Visualiza o saldo atual do banco usando nickname do jogador
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT ib."valorAtual", ib."valorEntrada", ib."nomeLocal"
            FROM "inst_banco" ib
            JOIN "mundo" m ON ib."seedMundo" = m."seedMundo"
            WHERE m."nickname" = %s
        """, (nickname,))
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado
    except Exception as e:
        print(Fore.RED + f"Erro ao visualizar saldo do banco: {e}")
        if connection:
            connection.close()
        return None

def aplicar_ouro_banco_por_jogador(nickname, quantidade):
    """
    Aplica ouro no banco usando nickname do jogador
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE "inst_banco" 
            SET "valorAtual" = "valorAtual" + %s
            WHERE "seedMundo" IN (
                SELECT m."seedMundo" 
                FROM "mundo" m 
                WHERE m."nickname" = %s
            )
        """, (quantidade, nickname))
        
        linhas_afetadas = cursor.rowcount
        connection.commit()
        cursor.close()
        connection.close()
        return linhas_afetadas > 0
    except Exception as e:
        print(Fore.RED + f"Erro ao aplicar ouro no banco: {e}")
        if connection:
            connection.rollback()
            connection.close()
        return False


# FUNÇÕES SIMPLIFICADAS DO VAREJO (usando nickname diretamente)
# 
def verificar_instancia_varejo_por_jogador(nickname):
    """
    Verifica se uma instância de varejo já existe para um jogador
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) > 0 
            FROM "inst_varejo" iv
            JOIN "mundo" m ON iv."seedMundo" = m."seedMundo"
            WHERE m."nickname" = %s
        """, (nickname,))
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado[0] if resultado else False
    except Exception as e:
        print(Fore.RED + f"Erro ao verificar instância do varejo: {e}")
        if connection:
            connection.close()
        return None

def criar_instancia_varejo_por_jogador(nickname, nome_local, id_npc, margem_lucro=15):
    """
    Cria instância do varejo diretamente pelo nickname
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO "inst_varejo" ("seedMundo", "nomeLocal", "idNPC", "margemLucro")
            SELECT m."seedMundo", %s, %s, %s
            FROM "mundo" m
            WHERE m."nickname" = %s
            AND NOT EXISTS (
                SELECT 1 FROM "inst_varejo" iv 
                WHERE iv."seedMundo" = m."seedMundo"
            )
        """, (nome_local, id_npc, margem_lucro, nickname))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(Fore.RED + f"Erro ao criar instância do varejo: {e}")
        if connection:
            connection.rollback()
            connection.close()
        return False

def visualizar_itens_varejo_por_jogador(nickname):
    """
    Visualiza todos os itens disponíveis para compra no varejo
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    try:
        cursor = connection.cursor()
        
        # Busca todos os itens disponíveis
        # TODO:immplementar logica para buscar itens aleatorios
        cursor.execute("""
            SELECT i."idItem", i."nome", 
                   ROUND(i."precoBase" * (1 + iv."margemLucro" / 100.0)) as preco_final,
                   i."descricao"
            FROM "item" i
            CROSS JOIN "inst_varejo" iv
            JOIN "mundo" m ON iv."seedMundo" = m."seedMundo"
            WHERE m."nickname" = %s
            ORDER BY i."nome"
        """, (nickname,))
        resultado = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultado
    except Exception as e:
        print(Fore.RED + f"Erro ao visualizar itens do varejo: {e}")
        if connection:
            connection.close()
        return None

def comprar_item_varejo_por_jogador(nickname, item_id, quantidade):
    """
    Compra um item no varejo para o jogador
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    try:
        cursor = connection.cursor()
        
        # Verificar se o jogador tem ouro suficiente
        cursor.execute("""
            SELECT j."ouro", 
                   ROUND(i."precoBase" * (1 + iv."margemLucro" / 100.0)) as preco_final
            FROM "jogador" j
            CROSS JOIN "item" i
            CROSS JOIN "inst_varejo" iv
            JOIN "mundo" m ON iv."seedMundo" = m."seedMundo"
            WHERE j."nickname" = %s AND i."idItem" = %s AND m."nickname" = %s
        """, (nickname, item_id, nickname))
        
        resultado = cursor.fetchone()
        if not resultado:
            print(Fore.RED + "Jogador ou item não encontrado!")
            return False
            
        ouro_jogador, preco_final = resultado
        custo_total = preco_final * quantidade
        
        if ouro_jogador < custo_total:
            print(Fore.RED + f"Ouro insuficiente! Você tem {ouro_jogador} ouros, mas precisa de {custo_total} ouros.")
            return False
        
        # Deduzir ouro do jogador
        cursor.execute("""
            UPDATE "jogador"
            SET "ouro" = "ouro" - %s
            WHERE "nickname" = %s
        """, (custo_total, nickname))
        
        # TODO: Adicionar item ao inventário do jogador
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(Fore.RED + f"Erro ao comprar item: {e}")
        if connection:
            connection.rollback()
            connection.close()
        return False


# FUNÇÕES UTILITÁRIAS


def buscar_itens_forja():
    """
    Busca itens disponíveis na forja
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT i."idItem", i."nome", i."descricao", i."precoBase"
            FROM "item" i
            JOIN "receita" r ON i."idItem" = r."idItemFabricado"
            ORDER BY i."nome"
        """)
        itens = cursor.fetchall()
        cursor.close()
        connection.close()
        return itens
    except Exception as e:
        print(Fore.RED + f"Erro ao buscar itens: {e}")
        if connection:
            connection.close()
        return None

def comprar_item_jogador(jogador, item_id, quantidade):
    """
    Compra um item para o jogador
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    try:
        cursor = connection.cursor()
        # TODO: Implementar lógica para comprar item
        # 1. Verificar se o jogador tem ouro suficiente
        # 2. Atualizar inventário do jogador
        # 3. Deduzir ouro do jogador
        # 4. Criar registro na inst_item se necessário
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(Fore.RED + f"Erro ao comprar item: {e}")
        if connection:
            connection.rollback()
            connection.close()
        return False

def forjar_item_jogador(jogador, item_id, materiais):
    """
    Forja um item para o jogador
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    try:
        cursor = connection.cursor()
        # TODO: Implementar lógica para forjar item
        # 1. Verificar se o jogador tem os materiais necessários
        # 2. Verificar se o jogador tem ouro suficiente
        # 3. Atualizar inventário do jogador
        # 4. Deduzir materiais e ouro do jogador
        # 5. Criar registro na inst_item se necessário
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(Fore.RED + f"Erro ao forjar item: {e}")
        if connection:
            connection.rollback()
            connection.close()
        return False 