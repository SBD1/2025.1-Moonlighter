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
        SELECT 
            J."armaEquipada",
            J."armaduraEquipada",
            IA."nome" AS "nome_arma",
            IAR."nome" AS "nome_armadura"
        FROM "jogador" J
        LEFT JOIN "item" IA ON J."armaEquipada" = IA."idItem"
        LEFT JOIN "item" IAR ON J."armaduraEquipada" = IAR."idItem"
        WHERE J."nickname" = %s;
    """, (nickname,))

    resultado = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if resultado:
        return {
            'arma_id': resultado[0],
            'armadura_id': resultado[1],
            'arma_nome': resultado[2] or "Nenhuma",
            'armadura_nome': resultado[3] or "Nenhuma"
        }
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
            print(f"     {Fore.LIGHTBLUE_EX}Valor Base: {Fore.WHITE}{preco} ouros")
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
            cursor.execute("""
                UPDATE "jogador" 
                SET "armaEquipada" = %s 
                WHERE "nickname" = %s;
            """, (id_item, nickname))
            tipo_equipamento = "arma"
        else:  # Armadura
            cursor.execute("""
                UPDATE "jogador" 
                SET "armaduraEquipada" = %s 
                WHERE "nickname" = %s;
            """, (id_item, nickname))
            tipo_equipamento = "armadura"
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}✓ {nome} foi equipado como {tipo_equipamento}!")
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
        print(f"{Fore.LIGHTGREEN_EX}• Digite '0' para voltar ao menu principal")
        
        escolha = input(f"\n{Style.BRIGHT}{Fore.MAGENTA}>> ").strip()
        
        if escolha == '0':
            return
        
        try:
            num_item = int(escolha)
            if 1 <= num_item <= len(itens_numerados):
                item_selecionado = itens_numerados[num_item - 1]
                menu_item_individual(nickname, item_selecionado)
            else:
                print(f"{Fore.RED}Número de item inválido!")
                time.sleep(1)
        except ValueError:
            print(f"{Fore.RED}Por favor, digite um número válido!")
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
        print(f"{Fore.LIGHTCYAN_EX}Valor Base: {Fore.YELLOW}{preco} ouros")
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