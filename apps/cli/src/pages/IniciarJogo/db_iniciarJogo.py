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


def buscar_local_jogador():
    connection = connect_to_db()

    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        enter_continue()
        return None
    
    cursor = connection.cursor()
    cursor.execute("""SELECT "jogador"."nomeLocal" 
                    FROM "jogador" 
                    JOIN "local" ON "local"."nomeLocal" = "jogador"."nomeLocal";
                    """)
    resultado = cursor.fetchone()

    cursor.close()
    connection.close()

    if resultado:
        return resultado[0]
    else:
        return None

def atualizar_local_jogador(novo_local):
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
                   SET "nomeLocal" = %s;
                    """, (resultadoselect[0],))
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

def buscar_seed_mundo(jogador):
    """
    Busca o seed do mundo do jogador
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        enter_continue()
        return None
    
    cursor = connection.cursor()
    cursor.execute("""SELECT "seedMundo" 
                    FROM "mundo"
                    WHERE "nickname" = %s;
                    """, (jogador,))
    resultado = cursor.fetchone()

    cursor.close()
    connection.close()

    if resultado:
        return resultado[0]
    else:
        return None

def buscar_nome_jogador():
    """
    Busca o nome do jogador atual
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        enter_continue()
        return None
    
    cursor = connection.cursor()
    cursor.execute("""SELECT "nickname" 
                    FROM "jogador";
                    """)
    resultado = cursor.fetchone()

    cursor.close()
    connection.close()

    if resultado:
        return resultado[0]
    else:
        return None