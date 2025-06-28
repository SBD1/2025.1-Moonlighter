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
            if x == 7 and y == 7:
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

    recursaoSalvarSalas(matriz, 7, 7)

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
        SELECT "posicaoX", "posicaoY", "conexão", "categoria"
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