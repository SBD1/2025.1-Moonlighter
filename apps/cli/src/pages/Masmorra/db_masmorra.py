from setup.database import connect_to_db
from setup.database import connect_to_db
from colorama import Fore

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

def salvarMasmorra(dadosMundo, dadosMasmorra, matriz, seedMasmorra):
    maxLinhas = len(matriz)
    maxColunas = len(matriz[0])

    connection = connect_to_db();
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()

    cursor.execute('''
                  INSERT INTO 'inst_masmorra'
                    VALUES
                    (%s, %s, %s, TRUE);
                  ''', (dadosMundo[0], seedMasmorra, dadosMasmorra[0],)
                  )
    
    seedSalasPercorrida = []
    recursaoSalvarSalas(matriz)
            
    def recursaoSalvarSalas(matriz, x = 7, y = 7):
        if matriz[x, y] == 0 or (x == maxLinhas or x == 0) or (y == maxColunas or y == 0):
            return
        if matriz[x, y] in seedSalasPercorrida:
            return
        else:
          seedSalasPercorrida.pop(matriz[x, y])
          cursor.execute('''
                        INSERT INTO 'sala'
                          VALUES 
                          (%s, %s, %s, 'Teste', %s, %s, %s)
                        ''', (matriz[x, y], x, y, dadosMundo[0], dadosMasmorra[0],)
                        )
          
          recursaoSalvarSalas(matriz, x+1, y)
          recursaoSalvarSalas(matriz, x-1, y)
          recursaoSalvarSalas(matriz, x, y+1)
          recursaoSalvarSalas(matriz, x, y-1)