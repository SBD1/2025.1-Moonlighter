from colorama import Fore
from setup.database import connect_to_db
from utils.enterContinue import enter_continue

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
