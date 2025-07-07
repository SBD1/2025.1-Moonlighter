"""
Interface do Sistema de Inventário para Moonlighter
Data: 29/06/2025
Descrição: Interface principal para gerenciamento do inventário do jogador
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

import time
import shutil
from colorama import Fore, Style, init
from pages.IniciarJogo.db_iniciarJogo import *
from utils.limparTerminal import limpar_terminal
import pyfiglet

# Inicializar colorama
init(autoreset=True)

# Obter largura do terminal
largura_terminal = shutil.get_terminal_size().columns

# Logo do jogo
ascii = pyfiglet.figlet_format("MOONLIGHTER")
centralizacao = "\n".join([linha.center(largura_terminal) for linha in ascii.splitlines()])
logo = f"{Style.BRIGHT + Fore.LIGHTGREEN_EX}\n\n{centralizacao}\n\n\n"

def obter_itens_inventario(nickname):
    """
    Obtém todos os itens do inventário do jogador
    """
    connection = connect_to_db()
    if connection is None:
        return []

    cursor = connection.cursor()
    cursor.execute("""
        SELECT 
            II."idInstItem",
            I."idItem",
            I."nome", 
            II."quantidade", 
            INV."nome" AS "tipo_inventario",
            INV."idInventario",
            I."tipo",
            I."descricao",
            I."precoBase"
        FROM "item" I
        INNER JOIN "inst_item" II ON I."idItem" = II."idItem"
        INNER JOIN "inst_inventario" INV_INST ON II."idInventario" = INV_INST."idInventario" 
            AND II."nickname" = INV_INST."nickname"
        INNER JOIN "inventario" INV ON INV_INST."idInventario" = INV."idInventario"
        WHERE II."nickname" = %s
        ORDER BY INV."idInventario", I."nome";
    """, (nickname,))

    itens = cursor.fetchall()
    cursor.close()
    connection.close()
    return itens

def obter_equipamentos_jogador(nickname):
    """
    Obtém os equipamentos atualmente equipados pelo jogador
    """
    connection = connect_to_db()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("""
        SELECT I_arma."idItem", I_arma."nome", I_arma."tipo"
        FROM "jogador" J
            JOIN "inst_item" II_arma ON J."nickname" = II_arma."nickname"
            JOIN "item" I_arma ON II_arma."idItem" = I_arma."idItem"
        WHERE J."nickname" = %s AND II_arma."idInventario" = 4
        UNION
        SELECT I_armadura."idItem", I_armadura."nome", I_armadura."tipo"
        FROM "jogador" J
            JOIN "inst_item" II_armadura ON J."nickname" = II_armadura."nickname"
            JOIN "item" I_armadura ON II_armadura."idItem" = I_armadura."idItem"
        WHERE J."nickname" = %s AND II_armadura."idInventario" = 3;
    """, (nickname, nickname,))

    resultado = cursor.fetchall()
    cursor.close()
    connection.close()

    equipamento = {
        'id_arma': None,
        'id_armadura': None,
        'arma_nome': "Nenhum",
        'armadura_nome': "Nenhum"
    }

    if resultado:
        for linha in resultado:
            if linha[2] == 'Arma':
                equipamento['id_arma'] = linha[0]
                equipamento['arma_nome'] = linha[1]
            elif linha[2] == 'Armadura':
                equipamento['id_armadura'] = linha[0]
                equipamento['armadura_nome'] = linha[1]

        return equipamento
    return None

def exibir_inventario_completo(nickname):
    """
    Exibe o inventário completo do jogador de forma organizada
    """
    limpar_terminal()
    print(logo)
    
    print(f"{Style.BRIGHT}{Fore.YELLOW}{'═' * largura_terminal}")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}INVENTÁRIO DE {nickname.upper()}".center(largura_terminal))
    print(f"{Style.BRIGHT}{Fore.YELLOW}{'═' * largura_terminal}")
    
    # Mostrar equipamentos atuais
    equipamentos = obter_equipamentos_jogador(nickname)
    if equipamentos:
        print(f"\n{Style.BRIGHT}{Fore.LIGHTCYAN_EX}EQUIPAMENTOS ATUAIS:")
        print(f"{Fore.LIGHTBLUE_EX}  Arma: {Fore.YELLOW}{equipamentos['arma_nome']}")
        print(f"{Fore.LIGHTBLUE_EX}  Armadura: {Fore.YELLOW}{equipamentos['armadura_nome']}")
    
    # Obter e organizar itens por inventário
    itens = obter_itens_inventario(nickname)
    
    if not itens:
        print(f"\n{Fore.YELLOW}Inventário vazio.")
        return []
    
    # Organizar itens por tipo de inventário
    inventarios = {}
    for item in itens:
        tipo_inv = item[4]  # tipo_inventario
        if tipo_inv not in inventarios:
            inventarios[tipo_inv] = []
        inventarios[tipo_inv].append(item)
    
    # Exibir itens organizados
    contador_item = 1
    itens_numerados = []
    
    for tipo_inventario, itens_do_tipo in inventarios.items():
        print(f"\n{Style.BRIGHT}{Fore.LIGHTCYAN_EX}[{tipo_inventario.upper()}]")
        print(f"{Style.BRIGHT}{Fore.YELLOW}{'─' * 50}")
        
        for item in itens_do_tipo:
            id_inst_item, id_item, nome, quantidade, _, id_inventario, tipo_item, descricao, preco = item
            itens_numerados.append(item)
            
            print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}{contador_item:2d}. {Fore.YELLOW}{nome}")
            print(f"     {Fore.LIGHTBLUE_EX}Quantidade: {Fore.WHITE}{quantidade}")
            print(f"     {Fore.LIGHTBLUE_EX}Tipo: {Fore.WHITE}{tipo_item or 'N/A'}")
            if descricao:
                desc_limitada = descricao[:60] + "..." if len(descricao) > 60 else descricao
                print(f"     {Fore.LIGHTBLACK_EX}{desc_limitada}")
            print()
            contador_item += 1
    
    return itens_numerados

def dropar_item(nickname, item_info):
    """
    Permite ao jogador dropar um item específico
    """
    id_inst_item, id_item, nome, quantidade_atual, tipo_inventario, id_inventario, tipo_item, descricao, preco = item_info
    
    print(f"\n{Style.BRIGHT}{Fore.YELLOW}Dropar item: {Fore.LIGHTGREEN_EX}{nome}")
    print(f"{Fore.LIGHTBLUE_EX}Quantidade atual: {Fore.WHITE}{quantidade_atual}")
    
    if quantidade_atual > 1:
        print(f"\n{Fore.LIGHTGREEN_EX}Quantas unidades deseja dropar? (1-{quantidade_atual})")
        try:
            quantidade_dropar = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>> "))
            if quantidade_dropar < 1 or quantidade_dropar > quantidade_atual:
                print(f"{Fore.RED}Quantidade inválida!")
                time.sleep(2)
                return False
        except ValueError:
            print(f"{Fore.RED}Por favor, digite um número válido!")
            time.sleep(2)
            return False
    else:
        quantidade_dropar = 1
    
    # Confirmar ação
    print(f"\n{Style.BRIGHT}{Fore.YELLOW}Confirma dropar {quantidade_dropar}x {nome}?")
    print(f"{Fore.WHITE}Digite 's' para confirmar ou 'n' para cancelar.")
    confirmacao = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip().lower()
    
    if confirmacao != 's':
        print(f"{Fore.YELLOW}Ação cancelada.")
        time.sleep(1)
        return False
    
    # Executar drop no banco de dados
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Primeiro, dropar o item no chão
        if dropar_item_no_chao(nickname, id_item, quantidade_dropar):
            # Em seguida, remover/atualizar do inventário
            if quantidade_dropar == quantidade_atual:
                # Remover item completamente
                cursor.execute("""
                    DELETE FROM "inst_item" 
                    WHERE "idInstItem" = %s;
                """, (id_inst_item,))
            else:
                # Reduzir quantidade
                nova_quantidade = quantidade_atual - quantidade_dropar
                cursor.execute("""
                    UPDATE "inst_item" 
                    SET "quantidade" = %s 
                    WHERE "idInstItem" = %s;
                """, (nova_quantidade, id_inst_item))
            
            # Atualizar slots ocupados
            atualizar_slots_ocupados(nickname, id_inventario)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}✓ {quantidade_dropar}x {nome} foi dropado com sucesso!")
            time.sleep(2)
            return True
        else:
            cursor.close()
            connection.close()
            print(f"{Fore.RED}Erro ao dropar item no chão!")
            time.sleep(2)
            return False
        
    except Exception as e:
        print(f"{Fore.RED}Erro ao dropar item: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        time.sleep(2)
        return False

def cadastrar_arma(id_item, dado_ataque, chance_critico, multiplicador, multiplicador_critico, tipo_arma='arma'):
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO "arma" (
                "idItem", "dadoAtaque", "chanceCritico", "multiplicador", "multiplicadorCritico", "tipoArma"
            ) VALUES (%s, %s, %s, %s, %s, %s)
        ''', (id_item, dado_ataque, chance_critico, multiplicador, multiplicador_critico, tipo_arma))

        connection.commit()
        cursor.close()
        connection.close()
        return True

    except Exception as e:
        print(f"Erro ao cadastrar arma: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False

def cadastrar_armadura(id_item, dado_defesa, defesa_passiva, critico_defensivo, bonus_defesa, tipo_armadura='armadura'):
    connection = connect_to_db()
    if connection is None:
        print("Erro ao conectar ao banco de dados.")
        return False

    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO "armadura" (
                "idItem", "dadoDefesa", "defesaPassiva", "criticoDefensivo", "bonusDefesa", "tipoArmadura"
            ) VALUES (%s, %s, %s, %s, %s, %s)
        ''', (id_item, dado_defesa, defesa_passiva, critico_defensivo, bonus_defesa, tipo_armadura))

        connection.commit()
        cursor.close()
        connection.close()
        return True

    except Exception as e:
        print(f"Erro ao cadastrar armadura: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False


def equipar_item(nickname, item_info):
    """
    Permite equipar armas ou armaduras
    """
    id_inst_item, id_item, nome, quantidade, tipo_inventario, id_inventario, tipo_item, descricao, preco = item_info
    
    # Verificar se é equipável
    if tipo_item not in ['Arma', 'Armadura']:
        print(f"{Fore.RED}Este item não pode ser equipado!")
        time.sleep(2)
        return False
    
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False
    
    try:
        cursor = connection.cursor()
        
        if tipo_item == 'Arma':
             # Verifica se a arma já está na tabela 'arma'
            cursor.execute('''
                SELECT 1 FROM "arma" WHERE "idItem" = %s;
            ''', (id_item,))
            existe = cursor.fetchone()

            if not existe:
                cadastrar_arma(id_item, 'd6', 10, 1.0, 1.5)

            # Remove todas as outras armas do slot de equipamento primeiro
            cursor.execute("""
                UPDATE "inst_item" 
                SET "idInventario" = 1 
                WHERE "nickname" = %s AND "idInventario" = 4;
            """, (nickname,))
            
            # Equipa a nova arma
            cursor.execute("""
                UPDATE "inst_item" 
                SET "idInventario" = 4 
                WHERE "nickname" = %s AND "idItem" = %s;
            """, (nickname, id_item))
            cursor.execute("""
                UPDATE "inst_inventario"
                SET "slotOcupado" = 1
                WHERE "nickname" = %s AND "idInventario" = 4;
            """, (nickname,))
            cursor.execute("""
                UPDATE "inst_inventario"
                SET "slotOcupado" = "slotOcupado" - 1
                WHERE "nickname" = %s AND "idInventario" = 1;
            """, (nickname,))
            tipo_equipamento = "arma"
        else:  # Armadura
            # Verifica se a armadura já está na tabela 'armadura'
            cursor.execute('''
                SELECT 1 FROM "armadura" WHERE "idItem" = %s;
            ''', (id_item,))
            existe = cursor.fetchone()

            if not existe:
                # Cadastra com atributos padrão
                cadastrar_armadura(id_item, 'd4', 2, 10, 1, 'leve')

            # Remove todas as outras armaduras do slot de equipamento primeiro
            cursor.execute("""
                UPDATE "inst_item" 
                SET "idInventario" = 1 
                WHERE "nickname" = %s AND "idInventario" = 3;
            """, (nickname,))
            
            # Equipa a nova armadura
            cursor.execute("""
                UPDATE "inst_item" 
                SET "idInventario" = 3 
                WHERE "nickname" = %s AND "idItem" = %s;
            """, (nickname, id_item))
            cursor.execute("""
                UPDATE "inst_inventario"
                SET "slotOcupado" = 1
                WHERE "nickname" = %s AND "idInventario" = 3;
            """, (nickname,))
            cursor.execute("""
                UPDATE "inst_inventario"
                SET "slotOcupado" = "slotOcupado" - 1
                WHERE "nickname" = %s AND "idInventario" = 1;
            """, (nickname,))
            tipo_equipamento = "armadura"
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX} {nome} foi equipado como {tipo_equipamento}!")
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"{Fore.RED}Erro ao equipar item: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        time.sleep(2)
        return False

def menu_inventario(nickname):
    """
    Menu principal do inventário com opções de interação
    """
    while True:
        itens_numerados = exibir_inventario_completo(nickname)
        
        if not itens_numerados:
            print(f"{Fore.LIGHTBLACK_EX}\nPressione Enter para voltar...")
            input()
            return
        
        print(f"\n{Style.BRIGHT}{Fore.YELLOW}OPÇÕES:")
        print(f"{Fore.LIGHTGREEN_EX}• Digite o número do item para interagir")
        print(f"{Fore.LIGHTGREEN_EX}• Digite 'E' para selecionar arma para equipar")
        print(f"{Fore.LIGHTGREEN_EX}• Digite 'A' para selecionar armadura para equipar")
        print(f"{Fore.RED}• Digite '0' para voltar ao menu principal")
        
        escolha = input(f"\n{Style.BRIGHT}{Fore.MAGENTA}>> ").strip().upper()
        
        if escolha == '0':
            return
        elif escolha == 'E':
            selecionar_arma_para_equipar(nickname)
        elif escolha == 'A':
            selecionar_armadura_para_equipar(nickname)
        else:
            try:
                num_item = int(escolha)
                if 1 <= num_item <= len(itens_numerados):
                    item_selecionado = itens_numerados[num_item - 1]
                    menu_item_individual(nickname, item_selecionado)
                else:
                    print(f"{Fore.RED}Número de item inválido!")
                    time.sleep(1)
            except ValueError:
                print(f"{Fore.RED}Por favor, digite um número válido, 'E' para arma ou 'A' para armadura!")
                time.sleep(1)

def menu_item_individual(nickname, item_info):
    """
    Menu para interagir com um item específico
    """
    id_inst_item, id_item, nome, quantidade, tipo_inventario, id_inventario, tipo_item, descricao, preco = item_info
    
    while True:
        limpar_terminal()
        print(logo)
        
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}ITEM SELECIONADO:")
        print(f"{Style.BRIGHT}{Fore.YELLOW}{'═' * 50}")
        print(f"{Style.BRIGHT}{Fore.LIGHTCYAN_EX}Nome: {Fore.YELLOW}{nome}")
        print(f"{Fore.LIGHTCYAN_EX}Quantidade: {Fore.YELLOW}{quantidade}")
        print(f"{Fore.LIGHTCYAN_EX}Tipo: {Fore.YELLOW}{tipo_item or 'N/A'}")
        print(f"{Fore.LIGHTCYAN_EX}Local: {Fore.YELLOW}{tipo_inventario}")
        if descricao:
            print(f"{Fore.LIGHTCYAN_EX}Descrição: {Fore.WHITE}{descricao}")
        
        print(f"\n{Style.BRIGHT}{Fore.YELLOW}AÇÕES DISPONÍVEIS:")
        print(f"{Fore.LIGHTGREEN_EX}1. Dropar item")
        
        if tipo_item in ['Arma', 'Armadura']:
            print(f"{Fore.LIGHTGREEN_EX}2. Equipar item")
        
        print(f"{Fore.LIGHTGREEN_EX}0. Voltar")
        
        escolha = input(f"\n{Style.BRIGHT}{Fore.MAGENTA}>> ").strip()
        
        if escolha == '0':
            return
        elif escolha == '1':
            if dropar_item(nickname, item_info):
                return  # Voltar ao menu principal após dropar
        elif escolha == '2' and tipo_item in ['Arma', 'Armadura']:
            equipar_item(nickname, item_info)
        else:
            print(f"{Fore.RED}Opção inválida!")
            time.sleep(1)

def ver_inventario(nickname):
    """
    Função principal para acessar o inventário
    Esta função será chamada do menu principal
    """
    menu_inventario(nickname)

def listar_armas_disponiveis(nickname):
    """
    Lista todas as armas disponíveis no inventário do jogador
    """
    connection = connect_to_db()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("""
        SELECT ii."idInstItem", i."idItem", i."nome", ii."quantidade", i."precoBase", 
               a."dadoAtaque", a."chanceCritico", a."multiplicador", a."multiplicadorCritico",
               CASE WHEN ii."idInventario" = 4 THEN 'Equipada' ELSE 'Na Mochila' END as status
        FROM "inst_item" ii
        JOIN "item" i ON ii."idItem" = i."idItem"
        JOIN "arma" a ON i."idItem" = a."idItem"
        WHERE ii."nickname" = %s AND i."tipo" = 'Arma'
        ORDER BY ii."idInventario" DESC, i."precoBase" DESC
    """, (nickname,))

    armas = cursor.fetchall()
    cursor.close()
    connection.close()
    return armas

def selecionar_arma_para_equipar(nickname):
    """
    Interface para selecionar qual arma equipar
    """
    limpar_terminal()
    print(logo)
    
    print(f"{Style.BRIGHT}{Fore.YELLOW}{'═' * largura_terminal}")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}SELEÇÃO DE ARMA - {nickname.upper()}".center(largura_terminal))
    print(f"{Style.BRIGHT}{Fore.YELLOW}{'═' * largura_terminal}")
    
    armas = listar_armas_disponiveis(nickname)
    
    if not armas:
        print(f"\n{Fore.RED}Você não possui nenhuma arma no inventário!")
        print(f"{Fore.YELLOW}Volte ao menu principal e compre uma arma primeiro.")
        time.sleep(3)
        return None
    
    print(f"\n{Style.BRIGHT}{Fore.LIGHTCYAN_EX}ARMAS DISPONÍVEIS:")
    print(f"{Fore.LIGHTBLUE_EX}{'Nº':<3} {'Nome':<25} {'Dado':<8} {'Crít':<6} {'Mult':<6} {'Preço':<8} {'Status':<12}")
    print(f"{Fore.LIGHTBLACK_EX}{'─' * 70}")
    
    armas_numeradas = []
    for i, arma in enumerate(armas, 1):
        id_inst, id_item, nome, qtd, preco, dado, crit, mult, mult_crit, status = arma
        status_color = Fore.GREEN if status == 'Equipada' else Fore.WHITE
        print(f"{Fore.WHITE}{i:<3} {nome:<25} {dado:<8} {crit:<6} {mult:<6} {preco:<8} {status_color}{status:<12}")
        armas_numeradas.append(arma)
    
    print(f"\n{Style.BRIGHT}{Fore.YELLOW}INSTRUÇÕES:")
    print(f"{Fore.LIGHTGREEN_EX}• Digite o número da arma que deseja equipar")
    print(f"{Fore.LIGHTGREEN_EX}• Digite '0' para cancelar")
    
    while True:
        try:
            escolha = input(f"\n{Style.BRIGHT}{Fore.MAGENTA}>> ").strip()
            
            if escolha == '0':
                return None
            
            num_arma = int(escolha)
            if 1 <= num_arma <= len(armas_numeradas):
                arma_selecionada = armas_numeradas[num_arma - 1]
                return equipar_arma_especifica(nickname, arma_selecionada)
            else:
                print(f"{Fore.RED}Número inválido! Escolha entre 1 e {len(armas_numeradas)}")
        except ValueError:
            print(f"{Fore.RED}Por favor, digite um número válido!")

def equipar_arma_especifica(nickname, arma_info):
    """
    Equipa uma arma específica escolhida pelo jogador
    """
    id_inst_item, id_item, nome, quantidade, preco, dado, crit, mult, mult_crit, status = arma_info
    
    # Se já está equipada, não precisa fazer nada
    if status == 'Equipada':
        print(f"{Fore.YELLOW}{nome} já está equipada!")
        time.sleep(2)
        return True
    
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Remove todas as outras armas do slot de equipamento primeiro
        cursor.execute("""
            UPDATE "inst_item" 
            SET "idInventario" = 1 
            WHERE "nickname" = %s AND "idInventario" = 4;
        """, (nickname,))
        
        # Equipa a arma selecionada
        cursor.execute("""
            UPDATE "inst_item" 
            SET "idInventario" = 4 
            WHERE "nickname" = %s AND "idItem" = %s;
        """, (nickname, id_item))
        
        # Atualizar slots ocupados
        cursor.execute("""
            UPDATE "inst_inventario"
            SET "slotOcupado" = 1
            WHERE "nickname" = %s AND "idInventario" = 4;
        """, (nickname,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}✓ {nome} foi equipada com sucesso!")
        print(f"{Fore.LIGHTBLUE_EX}  Dado: {dado} | Crítico: {crit}% | Multiplicador: {mult}")
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"{Fore.RED}Erro ao equipar arma: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        time.sleep(2)
        return False

def listar_armaduras_disponiveis(nickname):
    """
    Lista todas as armaduras disponíveis no inventário do jogador
    """
    connection = connect_to_db()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("""
        SELECT ii."idInstItem", i."idItem", i."nome", ii."quantidade", i."precoBase", 
               ar."dadoDefesa", ar."defesaPassiva", ar."criticoDefensivo", ar."bonusDefesa",
               CASE WHEN ii."idInventario" = 3 THEN 'Equipada' ELSE 'Na Mochila' END as status
        FROM "inst_item" ii
        JOIN "item" i ON ii."idItem" = i."idItem"
        JOIN "armadura" ar ON i."idItem" = ar."idItem"
        WHERE ii."nickname" = %s AND i."tipo" = 'Armadura'
        ORDER BY ii."idInventario" DESC, i."precoBase" DESC
    """, (nickname,))

    armaduras = cursor.fetchall()
    cursor.close()
    connection.close()
    return armaduras

def selecionar_armadura_para_equipar(nickname):
    """
    Interface para selecionar qual armadura equipar
    """
    limpar_terminal()
    print(logo)
    
    print(f"{Style.BRIGHT}{Fore.YELLOW}{'═' * largura_terminal}")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}SELEÇÃO DE ARMADURA - {nickname.upper()}".center(largura_terminal))
    print(f"{Style.BRIGHT}{Fore.YELLOW}{'═' * largura_terminal}")
    
    armaduras = listar_armaduras_disponiveis(nickname)
    
    if not armaduras:
        print(f"\n{Fore.RED}Você não possui nenhuma armadura no inventário!")
        print(f"{Fore.YELLOW}Volte ao menu principal e compre uma armadura primeiro.")
        time.sleep(3)
        return None
    
    print(f"\n{Style.BRIGHT}{Fore.LIGHTCYAN_EX}ARMADURAS DISPONÍVEIS:")
    print(f"{Fore.LIGHTBLUE_EX}{'Nº':<3} {'Nome':<25} {'Dado':<8} {'Def':<6} {'Crít':<6} {'Preço':<8} {'Status':<12}")
    print(f"{Fore.LIGHTBLACK_EX}{'─' * 70}")
    
    armaduras_numeradas = []
    for i, armadura in enumerate(armaduras, 1):
        id_inst, id_item, nome, qtd, preco, dado, def_pass, crit_def, bonus, status = armadura
        status_color = Fore.GREEN if status == 'Equipada' else Fore.WHITE
        print(f"{Fore.WHITE}{i:<3} {nome:<25} {dado:<8} {def_pass:<6} {crit_def:<6} {preco:<8} {status_color}{status:<12}")
        armaduras_numeradas.append(armadura)
    
    print(f"\n{Style.BRIGHT}{Fore.YELLOW}INSTRUÇÕES:")
    print(f"{Fore.LIGHTGREEN_EX}• Digite o número da armadura que deseja equipar")
    print(f"{Fore.LIGHTGREEN_EX}• Digite '0' para cancelar")
    
    while True:
        try:
            escolha = input(f"\n{Style.BRIGHT}{Fore.MAGENTA}>> ").strip()
            
            if escolha == '0':
                return None
            
            num_armadura = int(escolha)
            if 1 <= num_armadura <= len(armaduras_numeradas):
                armadura_selecionada = armaduras_numeradas[num_armadura - 1]
                return equipar_armadura_especifica(nickname, armadura_selecionada)
            else:
                print(f"{Fore.RED}Número inválido! Escolha entre 1 e {len(armaduras_numeradas)}")
        except ValueError:
            print(f"{Fore.RED}Por favor, digite um número válido!")

def equipar_armadura_especifica(nickname, armadura_info):
    """
    Equipa uma armadura específica escolhida pelo jogador
    """
    id_inst_item, id_item, nome, quantidade, preco, dado, def_pass, crit_def, bonus, status = armadura_info
    
    # Se já está equipada, não precisa fazer nada
    if status == 'Equipada':
        print(f"{Fore.YELLOW}{nome} já está equipada!")
        time.sleep(2)
        return True
    
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Remove todas as outras armaduras do slot de equipamento primeiro
        cursor.execute("""
            UPDATE "inst_item" 
            SET "idInventario" = 1 
            WHERE "nickname" = %s AND "idInventario" = 3;
        """, (nickname,))
        
        # Equipa a armadura selecionada
        cursor.execute("""
            UPDATE "inst_item" 
            SET "idInventario" = 3 
            WHERE "nickname" = %s AND "idItem" = %s;
        """, (nickname, id_item))
        
        # Atualizar slots ocupados
        cursor.execute("""
            UPDATE "inst_inventario"
            SET "slotOcupado" = 1
            WHERE "nickname" = %s AND "idInventario" = 3;
        """, (nickname,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}✓ {nome} foi equipada com sucesso!")
        print(f"{Fore.LIGHTBLUE_EX}  Dado: {dado} | Defesa Passiva: {def_pass} | Crítico: {crit_def}%")
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"{Fore.RED}Erro ao equipar armadura: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        time.sleep(2)
        return False