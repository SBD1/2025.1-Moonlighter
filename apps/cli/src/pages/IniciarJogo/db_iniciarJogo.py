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

def listar_jogadores():
    """
    Lista todos os jogadores disponíveis
    """
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None
    
    cursor = connection.cursor()
    cursor.execute("""SELECT "nickname", "ouro", "nomeLocal" 
                    FROM "jogador"
                    ORDER BY "nickname";
                    """)
    resultado = cursor.fetchall()

    cursor.close()
    connection.close()

    return resultado

def selecionar_jogador():
    """
    Permite ao usuário selecionar um jogador
    """
    jogadores = listar_jogadores()
    
    if not jogadores:
        print(Fore.RED + "Nenhum jogador encontrado!")
        return None
    
    if len(jogadores) == 1:
        # Se só há um jogador, retorna ele automaticamente
        return jogadores[0][0]
    
    # se tiver mais de um, agora da para escolher
    print(f"\n{Fore.CYAN}=== JOGADORES DISPONÍVEIS ===\n")
    
    for i, (nickname, ouro, local) in enumerate(jogadores, 1):
        print(f"{i} - {nickname} (Ouro: {ouro}, Local: {local})")
    
    while True:
        try:
            escolha = int(input(f"\n{Fore.YELLOW}Escolha um jogador (1-{len(jogadores)}): "))
            if 1 <= escolha <= len(jogadores):
                return jogadores[escolha-1][0]
            else:
                print(f"{Fore.RED}Opção inválida! Escolha entre 1 e {len(jogadores)}")
        except ValueError:
            print(f"{Fore.RED}Por favor, digite um número válido!")