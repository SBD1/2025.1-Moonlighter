import time
from pages.Estabelecimento.db_estabelecimento import *
from pages.IniciarJogo.db_iniciarJogo import buscar_seed_mundo
from pages.Estabelecimento.db_estabelecimento import (
    verificar_instancia_varejo_por_jogador,
    visualizar_itens_varejo_por_jogador,
    comprar_item_varejo_por_jogador,
    criar_instancia_varejo_por_jogador,
    exibir_dialogo_saudacao,
    exibir_dialogo_catalogo,
    exibir_dialogo_compra,
    exibir_dialogo_despedida
)
from setup.database import connect_to_db
from utils.limparTerminal import limpar_terminal
from utils.enterContinue import enter_continue
from colorama import Fore, Back, Style, init
import pygame
import shutil

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

def cabecalho_varejo():
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}=================== O CHAPÉU DE MADEIRA ===================".center(largura_terminal))
    print(f"{Fore.YELLOW}Loja de Varejo - Compras e Vendas".center(largura_terminal))
    print(f"{Fore.LIGHTGREEN_EX}========================================================".center(largura_terminal))

def menu_varejo(jogador):
    """
    Menu principal da loja de varejo
    """
    init(autoreset=True)
    
    # Exibir diálogo de saudação da alquimista
    limpar_terminal()
    cabecalho_varejo()
    exibir_dialogo_saudacao("Eris", jogador)
    enter_continue()
    
    # Verificar e criar instância da loja se necessário
    if not verificar_instancia_varejo_por_jogador(jogador):
        seed_mundo = buscar_seed_mundo(jogador)
        if seed_mundo:
            sucesso = criar_instancia_varejo_por_jogador(jogador, "O Chapéu de Madeira", 3, 15)
            if not sucesso:
                print(f"{Fore.RED}Erro ao inicializar a loja!")
                enter_continue()
                return
        else:
            print(f"{Fore.RED}Erro ao buscar informações do mundo!")
            enter_continue()
            return
    
    while True:
        limpar_terminal()
        cabecalho_varejo()
        print("\n")
        print(f"{Style.BRIGHT}{Fore.CYAN}O que você gostaria de fazer?".center(largura_terminal))
        print("\n")
        print(f"{Fore.WHITE}1 - Ver itens disponíveis para compra")
        print(f"{Fore.WHITE}2 - Comprar um item")
        print(f"{Fore.WHITE}0 - Sair da Loja")
        print("\n")
        
        escolha = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip()
        
        if escolha == "1":
            ver_itens_disponiveis(jogador)
        elif escolha == "2":
            comprar_item(jogador)
        elif escolha == "0":
            exibir_dialogo_despedida("Eris", jogador)
            enter_continue()
            break
        else:
            print(f"\n{Fore.RED}Opção inválida. Tente novamente.")
            enter_continue()

def ver_itens_disponiveis(jogador):
    """
    Função para ver itens disponíveis para compra
    """
    limpar_terminal()
    cabecalho_varejo()
    
    # Exibir diálogo de catálogo
    exibir_dialogo_catalogo("Eris", jogador)
    enter_continue()
    
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== ITENS DISPONÍVEIS PARA COMPRA ===".center(largura_terminal))
    print("\n")
    
    itens = visualizar_itens_varejo_por_jogador(jogador)
    if itens:
        print(f"{Fore.WHITE}{'ID':<5} {'Nome':<25} {'Preço':<10}")
        print(f"{Fore.LIGHTBLACK_EX}{'='*45}")
        for item in itens:
            id_item, nome, preco, descricao = item
            print(f"{Fore.WHITE}{id_item:<5} {nome:<25} {preco:<10}")
            print(f"{Fore.LIGHTBLACK_EX}     {descricao}")
            print()
    else:
        print(f"{Fore.RED}Nenhum item disponível para compra!")
    
    print("\n")
    enter_continue()

def comprar_item(jogador):
    """
    Função para comprar um item
    """
    limpar_terminal()
    cabecalho_varejo()
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== COMPRAR ITEM ===".center(largura_terminal))
    print("\n")
    
    # Mostrar itens disponíveis
    itens = visualizar_itens_varejo_por_jogador(jogador)
    if not itens:
        print(f"{Fore.RED}Nenhum item disponível para compra!")
        enter_continue()
        return
    
    print(f"{Fore.WHITE}{'ID':<5} {'Nome':<25} {'Preço':<10}")
    print(f"{Fore.LIGHTBLACK_EX}{'='*45}")
    for item in itens:
        id_item, nome, preco, descricao = item
        print(f"{Fore.WHITE}{id_item:<5} {nome:<25} {preco:<10}")
    
    print(f"\n{Fore.WHITE}Digite o ID do item que deseja comprar:")
    try:
        item_id = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> "))
        
        # Verificar se o item existe
        item_encontrado = None
        for item in itens:
            if item[0] == item_id:
                item_encontrado = item
                break
        
        if not item_encontrado:
            print(f"{Fore.RED}Item não encontrado!")
            enter_continue()
            return
        
        print(f"\n{Fore.WHITE}Digite a quantidade que deseja comprar:")
        quantidade = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> "))
        
        if quantidade <= 0:
            print(f"{Fore.RED}Quantidade deve ser maior que zero!")
            enter_continue()
            return
        
        # Exibir diálogo de compra
        exibir_dialogo_compra("Eris", jogador)
        
        # Comprar o item
        sucesso = comprar_item_varejo_por_jogador(jogador, item_id, quantidade)
        
        if sucesso:
            print(f"\n{Fore.GREEN}✅ {quantidade}x '{item_encontrado[1]}' comprado(s) com sucesso!")
        else:
            print(f"\n{Fore.RED}❌ Erro ao comprar item!")
            
    except ValueError:
        print(f"{Fore.RED}Por favor, digite um número válido!")
    except Exception as e:
        print(f"{Fore.RED}Erro inesperado: {e}")
    
    print("\n")
    enter_continue() 