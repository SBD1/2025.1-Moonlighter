from setup.database import connect_to_db
from colorama import Fore
import psycopg2

# FUNÇÕES DA FORJA

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

def visualizar_itens_forja_por_jogador(nickname, categoria):
    """
    Visualiza itens disponíveis para fabricar na forja, filtrando por nome contendo a categoria
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
            WHERE i."nome" ILIKE %s
            ORDER BY i."nome"
        """, (f'%{categoria}%',))
        
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
    Aplica ouro do jogador no banco, validando saldo em Python
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        # Buscar ouro atual do jogador
        cursor.execute('SELECT "ouro" FROM "jogador" WHERE "nickname" = %s', (nickname,))
        resultado = cursor.fetchone()
        if not resultado:
            return False
        ouro_jogador = resultado[0]
        if ouro_jogador < quantidade:
            print(Fore.RED + f"❌ Ouro insuficiente! Jogador {nickname} tem {ouro_jogador} ouros, mas está tentando aplicar {quantidade} ouros.")
            return False
        # Atualizar saldo do banco
        cursor.execute('''
            UPDATE "inst_banco"
            SET "valorAtual" = "valorAtual" + %s
            WHERE "seedMundo" IN (
                SELECT m."seedMundo"
                FROM "mundo" m
                WHERE m."nickname" = %s
            )
        ''', (quantidade, nickname))
        # Atualizar ouro do jogador
        cursor.execute('UPDATE "jogador" SET "ouro" = "ouro" - %s WHERE "nickname" = %s', (quantidade, nickname))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        if connection:
            connection.rollback()
            connection.close()
        return False

def sacar_ouro_banco_por_jogador(nickname, quantidade):
    """
    Saca ouro do banco para o jogador, validando saldo em Python
    """
    connection = connect_to_db()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        # Buscar saldo atual do banco
        cursor.execute('''
            SELECT ib."valorAtual"
            FROM "inst_banco" ib
            JOIN "mundo" m ON ib."seedMundo" = m."seedMundo"
            WHERE m."nickname" = %s
        ''', (nickname,))
        resultado = cursor.fetchone()
        if not resultado:
            return False
        saldo_banco = resultado[0]
        if saldo_banco < quantidade:
            print(Fore.RED + f"❌ Saldo insuficiente! Saldo atual: {saldo_banco} ouro, tentativa de saque: {quantidade} ouro")
            return False
        # Atualizar saldo do banco
        cursor.execute('''
            UPDATE "inst_banco"
            SET "valorAtual" = "valorAtual" - %s
            WHERE "seedMundo" IN (
                SELECT m."seedMundo"
                FROM "mundo" m
                WHERE m."nickname" = %s
            )
        ''', (quantidade, nickname))
        # Atualizar ouro do jogador
        cursor.execute('UPDATE "jogador" SET "ouro" = "ouro" + %s WHERE "nickname" = %s', (quantidade, nickname))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        if connection:
            connection.rollback()
            connection.close()
        return False

def visualizar_juros_banco_por_jogador(nickname):
    """
    Visualiza informações sobre juros do banco do jogador
    """
    connection = connect_to_db()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT ib."valorAtual", m."dia", m."periodo"
            FROM "inst_banco" ib
            JOIN "mundo" m ON ib."seedMundo" = m."seedMundo"
            WHERE m."nickname" = %s
        """, (nickname,))
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        return resultado
    except Exception as e:
        if connection:
            connection.close()
        return None

def aplicar_juros_manualmente_por_jogador(nickname, dias=1):
    """
    Aplica juros manualmente no banco do jogador
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        
        # Buscar dados atuais
        cursor.execute("""
            SELECT ib."valorAtual", m."dia", m."seedMundo"
            FROM "inst_banco" ib
            JOIN "mundo" m ON ib."seedMundo" = m."seedMundo"
            WHERE m."nickname" = %s
        """, (nickname,))
        
        resultado = cursor.fetchone()
        if not resultado:
            print(Fore.RED + "Banco não encontrado para este jogador!")
            return False
            
        valor_atual, dia_atual, seed_mundo = resultado
        taxa_juros = 2.50  # 2.5% ao dia
        
        # Calcular juros
        juros = int(valor_atual * (taxa_juros / 100.0) * dias)
        novo_valor = valor_atual + juros
        
        # Atualizar valor no banco
        cursor.execute("""
            UPDATE "inst_banco" 
            SET "valorAtual" = %s
            WHERE "seedMundo" = %s
        """, (novo_valor, seed_mundo))
        
        # Atualizar dia no mundo (isso vai acionar o trigger automaticamente)
        cursor.execute("""
            UPDATE "mundo" 
            SET "dia" = "dia" + %s
            WHERE "seedMundo" = %s
        """, (dias, seed_mundo))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(Fore.GREEN + f"💰 Juros aplicados: +{juros} ouro ({dias} dia(s))")
        print(Fore.CYAN + f"💳 Saldo anterior: {valor_atual} ouro")
        print(Fore.CYAN + f"💳 Saldo atual: {novo_valor} ouro")
        return True
        
    except Exception as e:
        if connection:
            connection.rollback()
            connection.close()
        return False

def simular_juros_por_jogador(nickname, dias=1):
    """
    Simula quanto de juros seria aplicado sem aplicar de fato
    """
    connection = connect_to_db()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT ib."valorAtual"
            FROM "inst_banco" ib
            JOIN "mundo" m ON ib."seedMundo" = m."seedMundo"
            WHERE m."nickname" = %s
        """, (nickname,))
        
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if resultado:
            valor_atual = resultado[0]
            taxa_juros = 2.50  # 2.5% ao dia
            juros = int(valor_atual * (taxa_juros / 100.0) * dias)
            novo_valor = valor_atual + juros
            
            return {
                'saldo_atual': valor_atual,
                'juros': juros,
                'saldo_futuro': novo_valor,
                'dias': dias
            }
        return None
        
    except Exception as e:
        if connection:
            connection.close()
        return None

def sacar_tudo_banco_por_jogador(nickname):
    """
    Saca todo o saldo disponível do banco para o jogador
    """
    connection = connect_to_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        # Buscar saldo atual do banco
        cursor.execute('''
            SELECT ib."valorAtual"
            FROM "inst_banco" ib
            JOIN "mundo" m ON ib."seedMundo" = m."seedMundo"
            WHERE m."nickname" = %s
        ''', (nickname,))
        resultado = cursor.fetchone()
        if not resultado:
            return False
        saldo_banco = resultado[0]
        if saldo_banco <= 0:
            print(Fore.YELLOW + "Não há saldo disponível para saque.")
            return False
        # Atualizar saldo do banco
        cursor.execute('''
            UPDATE "inst_banco"
            SET "valorAtual" = 0
            WHERE "seedMundo" IN (
                SELECT m."seedMundo"
                FROM "mundo" m
                WHERE m."nickname" = %s
            )
        ''', (nickname,))
        # Atualizar ouro do jogador
        cursor.execute('UPDATE "jogador" SET "ouro" = "ouro" + %s WHERE "nickname" = %s', (saldo_banco, nickname))
        connection.commit()
        cursor.close()
        connection.close()
        print(Fore.GREEN + f"✅ Você sacou {saldo_banco} ouro do banco!")
        return True
    except Exception as e:
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
        
        #atualmente busca todos os itens disponíveis
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