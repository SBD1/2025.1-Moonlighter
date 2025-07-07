import random
from setup.database import connect_to_db
from colorama import Fore
import hashlib
from utils.geradorSeed import gerarSeed
import time

def ObterDadosMundo(nickname):
    connection = connect_to_db()

    if connection is None:
        print("Erro ao conectar ao banco de dados.")
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

def ObterDadosJogador(nickname):
    connection = connect_to_db()

    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()
    cursor.execute("""SELECT *
                      FROM "jogador"
                      WHERE "nickname" = %s;
                    """, (nickname,))

    resultado = cursor.fetchone()
    cursor.close()
    connection.close()

    return resultado if resultado else None

def ObterDadosMasmorra(nomeMasmorra):
    connection = connect_to_db()

    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()
    cursor.execute("""SELECT *
                      FROM "masmorra"
                      WHERE "nomeLocal" = %s;
                    """, (nomeMasmorra,))

    resultado = cursor.fetchone()
    cursor.close()
    connection.close()

    return resultado if resultado else None

def atualizarParaLocalAnterior(dadosJogador):
    connection = connect_to_db()

    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()

    cursor.execute("""UPDATE "jogador"
                        SET "nomeLocal" = (SELECT "acesso" FROM "local" WHERE "nomeLocal" = %s), "updatedAt" = NOW()
                        WHERE "nickname" = %s;
                   """, (dadosJogador[6], dadosJogador[0]))
    
    connection.commit()
    cursor.close()
    connection.close()

def salvarMasmorra(dadosMundo, dadosMasmorra, seedMasmorra, matriz):
    maxLinhas = len(matriz)
    maxColunas = len(matriz[0])

    connection = connect_to_db();
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None
    
    stringCompleta = f"{dadosMundo[1]}{dadosMasmorra[0]}"
    hashVal = hashlib.sha256(stringCompleta.encode()).hexdigest()
    seedMasmorraCompleta = f"{seedMasmorra}-{hashVal[:20]}-{gerarSeed(10)}"

    cursor = connection.cursor()

    cursor.execute('''INSERT INTO "inst_masmorra" ("seedMundo", "seedMasmorra", "nomeLocal", "ativo")
                    VALUES
                    (%s, %s, %s, %s);
                  ''', (dadosMundo[0], seedMasmorraCompleta, dadosMasmorra[0], True)
                  )
    connection.commit()

    seedSalasPercorrida = []

    def recursaoSalvarSalas(matriz, x, y):
        if (
            x < 0 or x >= maxLinhas or
            y < 0 or y >= maxColunas
        ):
            return
        elif matriz[x][y] == 0:
            return
        elif matriz[x][y]["seed"] in seedSalasPercorrida:
            return
        else:
            seedSalasPercorrida.append(matriz[x][y]["seed"])
            if x == 12 and y == 12:
                tipoSala = "Entrada"
            elif matriz[x][y]["boss"]:
                tipoSala = "Boss"
            else:
                tipoSala = "Comum"
            
            conexoes = "".join(matriz[x][y]["conexoes"])
            cursor.execute('''
                            INSERT INTO "sala" ("seedSala", "posicaoX", "posicaoY", "conexão", "categoria", "seedMundo", "seedMasmorra")
                            VALUES 
                            (%s, %s, %s, %s, %s, %s, %s)
                            ''', (matriz[x][y]["seed"], x, y, conexoes, tipoSala, dadosMundo[0], seedMasmorraCompleta)
            )
            connection.commit()
            recursaoSalvarSalas(matriz, x, y+1)
            recursaoSalvarSalas(matriz, x, y-1)
            recursaoSalvarSalas(matriz, x+1, y)
            recursaoSalvarSalas(matriz, x-1, y)

    recursaoSalvarSalas(matriz, 12, 12)

    cursor.close()
    connection.close()
    return seedMasmorraCompleta

def carregar_salas(seed_masmorra):
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()
    cursor.execute('''
        SELECT "posicaoX", "posicaoY", "conexão", "categoria", "seedSala"
        FROM "sala"
        WHERE "seedMasmorra" = %s;
    ''', (seed_masmorra,))
    
    salas = cursor.fetchall()
    cursor.close()
    connection.close()

    return salas

def atualiza_posicao_jogador(nickname, x, y):
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return False
    
    cursor = connection.cursor()
    cursor.execute('''
            UPDATE "jogador"
            SET "PosiçãoX_Jogador" = %s, "PosiçãoY_Jogador" = %s
                   WHERE "nickname" = %s
                   ''', (x, y, nickname))
    
    connection.commit()
    cursor.close()
    connection.close()
    return True

def obter_monstros(nickname):
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return False
    
    # Primeiro, obtém o nomeLocal do jogador
    cursor = connection.cursor()
    cursor.execute("""
        SELECT "nomeLocal" FROM "jogador" WHERE "nickname" = %s
        """, (nickname,))
    resultado = cursor.fetchone()
    if not resultado:
        print("Jogador não encontrado.")
        return []

    nome_local = resultado[0]

    # Busca monstros associados a esse local
    cursor.execute('''
            SELECT "idMonstro", "nome", "vidaMaxima", "nivel", "chanceCritico", "dadoAtaque", "multiplicador", "multiplicadorCritico", "chefe" FROM "monstro" WHERE "nomeLocal" = %s
                   ''', (nome_local,))
    monstros = cursor.fetchall()
    cursor.close()
    connection.close()
    return monstros

def obter_arma(nickname):
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return False
    
    cursor = connection.cursor()
    cursor.execute('''
            SELECT a.*
            FROM "inst_item" ii2
            JOIN "item" i ON ii2."idItem" = i."idItem"
            JOIN "arma" a ON i."idItem" = a."idItem"
            WHERE ii2."nickname" = %s AND ii2."idInventario" = 4
            LIMIT 1;
        ''', (nickname,))
    arma = cursor.fetchone()
    cursor.close()
    connection.close()
    return arma

def obter_armadura(nickname):
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()
    cursor.execute('''
            SELECT ar.*
            FROM "inst_item" ii2
            JOIN "item" i ON ii2."idItem" = i."idItem"
            JOIN "armadura" ar ON i."idItem" = ar."idItem"
            WHERE ii2."nickname" = %s AND ii2."idInventario" = 3
            LIMIT 1;
    ''', (nickname,))
    
    armadura = cursor.fetchone()
    cursor.close()
    connection.close()
    return armadura

def obter_vida_jogador(nickname):
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()
    cursor.execute('''
        SELECT "atualHP" FROM "jogador" WHERE "nickname" = %s;
    ''', (nickname,))
    
    vida = cursor.fetchone()
    cursor.close()
    connection.close()
    return vida[0] if vida is not None else None

def atualizar_vida_jogador(nickname, nova_vida):
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()
    cursor.execute('''
        UPDATE "jogador" SET "atualHP" = %s WHERE "nickname" = %s;
    ''', (nova_vida, nickname))

    connection.commit()
    cursor.close()
    connection.close()

def desbloquear_masmorra(nickname, nome_masmorra):
    conn = connect_to_db()
    if conn is None:
        print("Erro ao conectar ao banco de dados.")
        return
    
    cursor = conn.cursor()

    try:
        # Obter nível de desbloqueio da masmorra informada
        cursor.execute("""
            SELECT "nivelDesbloqueio"
            FROM "masmorra"
            WHERE "nomeLocal" = %s
        """, (nome_masmorra,))
        resultado = cursor.fetchone()

        if resultado is None:
            print(f"Masmorra '{nome_masmorra}' não encontrada no banco de dados.")
            return

        nivel_desejado = resultado[0]

        # Obter o nível atual do mundo do jogador
        cursor.execute("""
            SELECT "nivelMundo"
            FROM "mundo"
            WHERE "nickname" = %s
        """, (nickname,))
        nivel_atual = cursor.fetchone()[0]

        # Só atualiza se o nível da masmorra for maior que o atual
        if nivel_desejado > nivel_atual:
            cursor.execute("""
                UPDATE "mundo"
                SET "nivelMundo" = %s
                WHERE "nickname" = %s
            """, (nivel_desejado, nickname))
            conn.commit()
            print(f"{Fore.LIGHTBLUE_EX}  Novo nível do mundo: {nivel_desejado}")
        else:
            print(f"{Fore.LIGHTBLACK_EX}  Masmorra já estava desbloqueada.")

    except Exception as e:
        conn.rollback()
        print(f"Erro ao desbloquear masmorra: {e}")

    finally:
        cursor.close()
        conn.close()

def musica_masmorra(nickname):
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()
    cursor.execute('''
        SELECT "nomeLocal" FROM "jogador" WHERE "nickname" = %s;
    ''', (nickname,))

    resultado = cursor.fetchone()
    cursor.close()
    connection.close()

    if resultado:
        return resultado[0]  # Pega só o nomeLocal, que está na tupla
    else:
        return None

def obter_drops_monstro(id_monstro):
    """
    Obtém todos os possíveis drops de um monstro específico
    Retorna uma lista de tuplas com (id_item, nome_item, chance_drop, qtd_minima, qtd_maxima)
    """
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return []
    
    cursor = connection.cursor()
    cursor.execute('''
        SELECT mi."idItem", i."nome", mi."chanceDrop", mi."qtdMinima", mi."qtdMaxima"
        FROM "monstro_item" mi
        JOIN "item" i ON mi."idItem" = i."idItem"
        WHERE mi."idMonstro" = %s
        ORDER BY mi."chanceDrop" DESC
    ''', (id_monstro,))
    
    drops = cursor.fetchall()
    cursor.close()
    connection.close()
    return drops

def processar_drops_monstro(id_monstro):
    """
    Processa os drops de um monstro baseado nas chances definidas no banco
    Retorna uma lista de itens que foram dropados com suas quantidades
    """
    drops_possiveis = obter_drops_monstro(id_monstro)
    drops_obtidos = []
    
    for id_item, nome_item, chance_drop, qtd_minima, qtd_maxima in drops_possiveis:
        # Gera um número aleatório entre 0 e 1
        if random.random() <= chance_drop:
            # Se passou na chance, sorteia a quantidade
            quantidade = random.randint(qtd_minima, qtd_maxima)
            drops_obtidos.append({
                'id_item': id_item,
                'nome': nome_item,
                'quantidade': quantidade
            })
    
    return drops_obtidos

def adicionar_item_ao_inventario(nickname, id_item, quantidade):
    """
    Adiciona um item ao inventário do jogador
    """
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return False
    
    cursor = connection.cursor()
    
    try:
        # Verifica se o jogador já tem o item no inventário
        cursor.execute('''
            SELECT ii2."quantidade"
            FROM "inst_inventario" ii
            JOIN "inst_item" ii2 ON ii."idInventario" = ii2."idInventario" AND ii."nickname" = ii2."nickname"
            WHERE ii."nickname" = %s AND ii2."idItem" = %s
        ''', (nickname, id_item))
        
        resultado = cursor.fetchone()
        
        if resultado is not None and len(resultado) > 0 and resultado[0] is not None:
            # Se já tem o item, atualiza a quantidade
            quantidade_atual = resultado[0]
            nova_quantidade = quantidade_atual + quantidade
            
            cursor.execute('''
                UPDATE "inst_item"
                SET "quantidade" = %s
                FROM "inst_inventario" ii
                WHERE "inst_item"."idInventario" = ii."idInventario" 
                AND ii."nickname" = %s 
                AND "inst_item"."idItem" = %s
            ''', (nova_quantidade, nickname, id_item))
        else:
            # Se não tem o item, adiciona um novo
            cursor.execute('''
                INSERT INTO "inst_item" ("idInventario", "idItem", "quantidade", "nickname")
                SELECT ii."idInventario", %s, %s, %s
                FROM "inst_inventario" ii
                WHERE ii."nickname" = %s
                LIMIT 1
            ''', (id_item, quantidade, nickname, nickname))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        connection.rollback()
        cursor.close()
        connection.close()
        print(f"Erro ao adicionar item ao inventário: {e}")
        return False