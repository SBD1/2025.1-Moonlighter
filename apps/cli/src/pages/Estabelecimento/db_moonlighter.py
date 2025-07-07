from setup.database import connect_to_db
from colorama import Fore

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
                        WHERE N."idNPC" = (SELECT "idNPC" FROM npc WHERE "nome" = 'Mundo') AND D."idDialogoPai" IS NULL AND D."tipo" = 'Sono';""")
    else:
        cursor.execute("""SELECT D."conteudo", D."idDialogo"
                        FROM "dialogo" D 
                            INNER JOIN "dialogo_npc" DN 
                            ON D."idDialogo" = DN."idDialogo"
                            INNER JOIN "npc" N
                            ON N."idNPC" = DN."idNPC"
                        WHERE N."idNPC" = (SELECT "idNPC" FROM npc WHERE "nome" = 'Mundo') AND D."idDialogoPai" = %s AND D."tipo" = 'Sono';""",
                        (busca,)
                    )
    narracao = cursor.fetchone()
    cursor.close()
    connection.close()

    return narracao

def restaurarSaudeJogador(nickname):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("""
                       UPDATE "jogador" SET "atualHP" = "maxHP", "updatedAt" = NOW() WHERE "nickname" = %s;
                       """, (nickname,))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao restaurar saúde do jogador: {e}")
        return False

def mudarLocalizacaoJogador(nickname, nova_localizacao):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("""
                       UPDATE "jogador" SET "nomeLocal" = %s, "updatedAt" = NOW() WHERE "nickname" = %s;
                       """, (nova_localizacao, nickname))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao mudar localização do jogador: {e}")
        return False
    
def atualizarParaLocalAnterior(nickname):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("""
                       UPDATE "jogador" SET "nomeLocal" = (SELECT "acesso" FROM "local" WHERE "nomeLocal" = 'Moonlighter'), "updatedAt" = NOW() WHERE "nickname" = %s;
                       """, (nickname,))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao atualizar localização do jogador: {e}")
        return False
    
def buscarItensJogador(nickname):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return []

    cursor = connection.cursor()
    try:
        cursor.execute("""
              SELECT I."nome", II."quantidade", II."idInventario", II."idInstItem", II."idInventario", II."idItem"
              FROM "inst_item" II
                JOIN "item" I ON II."idItem" = I."idItem"
              WHERE II."nickname" = %s AND II."idInventario" <> 5;
                       """, (nickname,))
        itens = cursor.fetchall()
        cursor.close()
        connection.close()
        return itens
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao buscar itens do jogador: {e}")
        return []

def buscarItensBaudeCasa(nickname):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return []

    cursor = connection.cursor()
    try:
        cursor.execute("""
              SELECT I."nome", II."quantidade", II."idInventario", II."idInstItem", II."idInventario", II."idItem"
              FROM "inst_item" II
                JOIN "item" I ON II."idItem" = I."idItem"
              WHERE II."nickname" = %s AND II."idInventario" = 5;
                       """, (nickname,))
        itens = cursor.fetchall()
        cursor.close()
        connection.close()
        return itens
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao buscar itens do baú: {e}")
        return []
    
def buscarItensMoonlighter(nickname):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return []

    cursor = connection.cursor()
    try:
        cursor.execute("""
              SELECT I."nome", II."quantidade", II."idInventario", II."idInstItem", II."idInventario", II."idItem"
              FROM "inst_item" II
                JOIN "item" I ON II."idItem" = I."idItem"
              WHERE II."nickname" = %s AND II."seedMundoLojaJogador" IS NOT NULL;
                       """, (nickname,))
        itens = cursor.fetchall()
        cursor.close()
        connection.close()
        return itens
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao buscar itens do Moonlighter: {e}")
        return []

def moverItemParaBaudeCasa(nickname, idInstItem, quantidade, localInventario, idItem):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("""
              SELECT "quantidade" FROM "inst_item" WHERE "nickname" = %s AND "idInstItem" = %s;
                       """, (nickname, idInstItem))
        quantidadeItem = cursor.fetchone()
        cursor.execute("""
              SELECT "idInstItem" FROM "inst_item" WHERE "nickname" = %s AND "idItem" = %s AND "idInventario" = 5;
        """, (nickname, idItem))
        itemExistente = cursor.fetchone()

        if quantidadeItem == quantidade:
            if itemExistente:
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" + %s WHERE "idInstItem" = %s;
                                """, (quantidade, itemExistente[0]))
            else:
                cursor.execute("""
                        UPDATE "inst_item" SET "idInventario" = 5 WHERE "idInstItem" = %s;
                                """, (idInstItem,))
            cursor.execute("""
                    UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" - %s WHERE "nickname" = %s AND "idInventario" = %s;
                        """, (quantidade, nickname, localInventario))
        else:
            if itemExistente:
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" + %s WHERE "idInstItem" = %s;
                                """, (quantidade, itemExistente[0]))
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" - %s WHERE "idInstItem" = %s;
                                """, (quantidade, idInstItem))
                cursor.execute("""
                        UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" + %s WHERE "nickname" = %s AND "idInventario" = 5;
                            """, (quantidade, nickname))
                cursor.execute("""
                        UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" - %s WHERE "nickname" = %s AND "idInventario" = %s;
                            """, (quantidade, nickname, localInventario))
            else:
                cursor.execute("""
                        INSERT INTO "inst_item" ("idItem", "quantidade", "nickname", "idInventario") VALUES
                                (%s, %s, %s, %s)
                                """, (idItem, quantidade, nickname, 5))
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" - %s WHERE "idInstItem" = %s;
                                """, (quantidade, idInstItem))
                cursor.execute("""
                        UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" + %s WHERE "nickname" = %s AND "idInventario" = 5;
                            """, (quantidade, nickname))
                cursor.execute("""
                        UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" - %s WHERE "nickname" = %s AND "idInventario" = %s;
                            """, (quantidade, nickname, localInventario))
          
        cursor.execute("""
              DELETE FROM "inst_item" WHERE "quantidade" <= 0 AND "nickname" = %s;
                       """, (nickname,))

        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao mover item para o baú: {e}")
        return False

def moverItemDoBaudeCasa(nickname, idItem, quantidade, idInstItem):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("""
                SELECT "quantidade" FROM "inst_item" WHERE "nickname" = %s AND "idItem" = %s AND "idInventario" = 5;
                          """, (nickname, idItem))
        quantidadeItem = cursor.fetchone()
        cursor.execute("""
                SELECT "idInstItem" FROM "inst_item" WHERE "nickname" = %s AND "idItem" = %s AND "idInventario" = 1;
        """, (nickname, idItem))
        itemExistente = cursor.fetchone()

        if quantidadeItem == quantidade:
            if itemExistente:
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" + %s WHERE "idInstItem" = %s;
                                """, (quantidade, itemExistente[0]))
            else:
                cursor.execute("""
                        UPDATE "inst_item" SET "idInventario" = 1 WHERE "idItem" = %s AND "nickname" = %s AND "idInventario" = 5;
                                """, (idItem, nickname))
            cursor.execute("""
                    UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" + %s WHERE "nickname" = %s AND "idInventario" = 1;
                        """, (quantidade, nickname))
            cursor.execute("""
                    UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" - %s WHERE "nickname" = %s AND "idInventario" = 5;
                        """, (quantidade, nickname))
        else:
            if itemExistente:
                cursor.execute("""
                    UPDATE "inst_item" SET "quantidade" = "quantidade" + %s WHERE "idInstItem" = %s;
                                """, (quantidade, itemExistente[0]))
                cursor.execute("""
                    UPDATE "inst_item" SET "quantidade" = "quantidade" - %s WHERE "idInstItem" = %s;
                                """, (quantidade, idInstItem))
                cursor.execute("""
                    UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" + %s WHERE "nickname" = %s AND "idInventario" = 1;
                            """, (quantidade, nickname))
                cursor.execute("""
                    UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" - %s WHERE "nickname" = %s AND "idInventario" = 5;
                            """, (quantidade, nickname))
            else:
                cursor.execute("""
                    INSERT INTO "inst_item" ("idItem", "quantidade", "nickname", "idInventario") VALUES
                                (%s, %s, %s, %s)
                                """, (idItem, quantidade, nickname, 1))
                cursor.execute("""
                    UPDATE "inst_item" SET "quantidade" = "quantidade" - %s WHERE "idInstItem" = %s;
                                """, (quantidade, idInstItem))
                cursor.execute("""
                    UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" + %s WHERE "nickname" = %s AND "idInventario" = 1;
                            """, (quantidade, nickname))
                cursor.execute("""
                    UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" - %s WHERE "nickname" = %s AND "idInventario" = 5;
                            """, (quantidade, nickname))
                
        cursor.execute("""
              DELETE FROM "inst_item" WHERE "quantidade" <= 0 AND "nickname" = %s;
                       """, (nickname,))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao mover item do baú para o inventário: {e}")
        return False
    
def buscarSeedMundoLojaJogador(nickname):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT M."seedMundo" FROM "loja_jogador" LJ
                       JOIN "mundo" M ON LJ."seedMundo" = M."seedMundo" 
            WHERE M."nickname" = %s;
                       """, (nickname,))
        seed = cursor.fetchone()
        cursor.close()
        connection.close()
        return seed[0] if seed else None
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao buscar seed do mundo loja do jogador: {e}")
        return None

def adicionarItemMoonlighter(nickname, idItem, quantidade, localInventario, idInstItem):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    cursor = connection.cursor()
    try:
        seedMundoLojaJogador = buscarSeedMundoLojaJogador(nickname)
        cursor.execute("""
                SELECT "idInstItem" FROM "inst_item" WHERE "nickname" = %s AND "idItem" = %s AND "idInventario" = %s;
                        """, (nickname, idItem, localInventario))
        quantidadeItem = cursor.fetchone()
        cursor.execute("""
                SELECT "idInstItem" FROM "inst_item" WHERE "nickname" = %s AND "idItem" = %s AND "seedMundoLojaJogador" = %s;
                        """, (nickname, idItem, seedMundoLojaJogador))
        itemExistente = cursor.fetchone()

        if quantidadeItem == quantidade:
            if itemExistente:
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" + %s WHERE "idInstItem" = %s;
                                """, (quantidade, itemExistente[0]))
                cursor.execute("""
                        DELETE FROM "inst_item" WHERE "idInstItem" = %s
                               """, (idInstItem,))
            else:
                cursor.execute("""
                        INSERT INTO "inst_item" ("idItem", "quantidade", "nickname", "seedMundoLojaJogador") VALUES
                                (%s, %s, %s, %s)
                                """, (idItem, quantidade, nickname, seedMundoLojaJogador))
                cursor.execute("""
                        DELETE FROM "inst_item" WHERE "idInstItem" = %s
                               """, (idInstItem,))
            cursor.execute("""
                    UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" - %s WHERE "nickname" = %s AND "idInventario" = %s;
                        """, (quantidade, nickname, localInventario))
            cursor.execute("""
                    UPDATE "loja_jogador" SET "exposicaoUsada" = "exposicaoUsada" + %s WHERE "seedMundo" = %s;
                           """, (quantidade, seedMundoLojaJogador))
        else:
            if itemExistente:
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" + %s WHERE "idInstItem" = %s;
                                """, (quantidade, itemExistente[0]))
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" - %s WHERE "idInstItem" = %s;
                                """, (quantidade, idInstItem))
            else:
                cursor.execute("""
                        INSERT INTO "inst_item" ("idItem", "quantidade", "nickname", "seedMundoLojaJogador") VALUES
                                (%s, %s, %s, %s)
                                """, (idItem, quantidade, nickname, seedMundoLojaJogador))
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" - %s WHERE "idInstItem" = %s;
                                """, (quantidade, idInstItem))
            cursor.execute("""
                    UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" - %s WHERE "nickname" = %s AND "idInventario" = %s;
                        """, (quantidade, nickname, localInventario))
            cursor.execute("""
                    UPDATE "loja_jogador" SET "exposicaoUsada" = "exposicaoUsada" + %s WHERE "seedMundo" = %s;
                           """, (quantidade, seedMundoLojaJogador))
            
        cursor.execute("""
              DELETE FROM "inst_item" WHERE "quantidade" <= 0 AND "nickname" = %s;
                       """, (nickname,))

        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao adicionar item no Moonlighter: {e}")
        return False
    
def removerItemMoonlighter(nickname, idInstItem, quantidade, idItem):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    cursor = connection.cursor()
    try:
        seedMundoLojaJogador = buscarSeedMundoLojaJogador(nickname)
        cursor.execute("""
              SELECT "quantidade" FROM "inst_item" WHERE "nickname" = %s AND "idInstItem" = %s;
                       """, (nickname, idInstItem))
        quantidadeItem = cursor.fetchone()
        cursor.execute("""
              SELECT "idInstItem" FROM "inst_item" WHERE "nickname" = %s AND "idItem" = %s AND "idInventario" = 1;
                       """, (nickname, idItem))
        itemExistente = cursor.fetchone()

        if quantidadeItem == quantidade:
            if itemExistente:
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" + %s WHERE "idInstItem" = %s;
                                """, (quantidade, itemExistente[0]))
            else:
                cursor.execute("""
                        INSERT INTO "inst_item" ("idItem", "quantidade", "nickname", "idInventario") VALUES
                                (%s, %s, %s, 1)
                                """, (idItem, quantidade, nickname))
            cursor.execute("""
                        DELETE FROM "inst_item" WHERE "idInstItem" = %s
                               """, (idInstItem,))
            cursor.execute("""
                    UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" + %s WHERE "nickname" = %s AND "idInventario" = 1;
                        """, (quantidade, nickname))
            cursor.execute("""
                    UPDATE "loja_jogador" SET "exposicaoUsada" = "exposicaoUsada" - %s WHERE "seedMundo" = %s;
                       """, (quantidade, seedMundoLojaJogador))
        else:
            if itemExistente:
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" + %s WHERE "idInstItem" = %s;
                                """, (quantidade, itemExistente[0]))
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" - %s WHERE "idInstItem" = %s;
                                """, (quantidade, idInstItem))
            else:
                cursor.execute("""
                        INSERT INTO "inst_item" ("idItem", "quantidade", "nickname", "idInventario") VALUES
                                (%s, %s, %s, 1)
                                """, (idItem, quantidade, nickname))
                cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" - %s WHERE "idInstItem" = %s;
                                """, (quantidade, idInstItem))
            cursor.execute("""
                    UPDATE "inst_inventario" SET "slotOcupado" = "slotOcupado" + %s WHERE "nickname" = %s AND "idInventario" = 1;
                        """, (quantidade, nickname))
            cursor.execute("""
                    UPDATE "loja_jogador" SET "exposicaoUsada" = "exposicaoUsada" - %s WHERE "seedMundo" = %s;
                       """, (quantidade, seedMundoLojaJogador))
            
        cursor.execute("""
              DELETE FROM "inst_item" WHERE "quantidade" <= 0 AND "nickname" = %s;
                       """, (nickname,))

        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao remover item do Moonlighter: {e}")
        return False

def passarDiaMundo(nickname):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("""
              UPDATE "mundo" SET "dia" = "dia" + 1, "periodo" = 'Manhã' WHERE "nickname" = %s;
                       """, (nickname,))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        cursor.rollback()
        connection.close()
        print(Fore.RED + f"Erro ao passar dia no mundo: {e}")
        return False
