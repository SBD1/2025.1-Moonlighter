from colorama import Fore
from setup.database import connect_to_db

def buscarNarracao(busca):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()

    if busca is None:
        cursor.execute("""SELECT D."conteudo", D."idDialogo"
                        FROM "dialogo" D
                        INNER JOIN "dialogo_npc" DN
                        ON D."idDialogo" = DN."idDialogo"
                        INNER JOIN "npc" N
                        ON N."idNPC" = DN."idNPC"
                        WHERE N."idNPC" = (SELECT "idNPC" FROM npc WHERE "nome" = 'Mundo') AND D."idDialogoPai" IS NULL AND D."tipo" = 'Tutorial';""")
    else:
        cursor.execute("""SELECT D."conteudo", D."idDialogo"
                        FROM "dialogo" D 
                            INNER JOIN "dialogo_npc" DN 
                            ON D."idDialogo" = DN."idDialogo"
                            INNER JOIN "npc" N
                            ON N."idNPC" = DN."idNPC"
                        WHERE N."idNPC" = (SELECT "idNPC" FROM npc WHERE "nome" = 'Mundo') AND D."idDialogoPai" = %s AND D."tipo" = 'Tutorial';""",
                        (busca,)
                    )
    narracao = cursor.fetchone()
    cursor.close()
    connection.close()

    return narracao