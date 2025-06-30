import time
from pages.Estabelecimento.db_estabelecimento import *
from pages.IniciarJogo.db_iniciarJogo import buscar_seed_mundo
from pages.Estabelecimento.db_estabelecimento import (
    verificar_instancia_forja_por_jogador,
    visualizar_itens_forja_por_jogador,
    forjar_item_por_jogador,
    criar_instancia_forja_por_jogador,
    criar_instancia_forja_por_jogador,
    exibir_dialogo_saudacao,
    exibir_dialogo_catalogo,
    exibir_dialogo_fabricacao,
    exibir_dialogo_despedida
)
from utils.limparTerminal import limpar_terminal
from utils.enterContinue import enter_continue
from colorama import Fore, Back, Style, init
import pygame
import shutil

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

def cabecalho_forja():
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}=================== FORJA VULCÂNICA ===================".center(largura_terminal))
    print(f"{Fore.YELLOW}Forja Vulcânica - Fabricação de Itens".center(largura_terminal))
    print(f"{Fore.LIGHTGREEN_EX}========================================================".center(largura_terminal))

def menu_forja(jogador):
    """
    Menu principal da forja
    """
    init(autoreset=True)
    
    # Exibir diálogo de saudação do ferreiro
    limpar_terminal()
    cabecalho_forja()
    exibir_dialogo_saudacao("Andrei", jogador)
    enter_continue()
    
    # Verificar e criar instância da forja se necessário
    if not verificar_instancia_forja_por_jogador(jogador):
        # Buscar seed_mundo para criar instância
        seed_mundo = buscar_seed_mundo(jogador)
        if seed_mundo:
            # Criar instância da forja
            sucesso = criar_instancia_forja_por_jogador_por_jogador(jogador, "Forja Vulcânica", 2)
            if not sucesso:
                print(f"{Fore.RED}Erro ao inicializar a forja!")
                enter_continue()
                return
        else:
            print(f"{Fore.RED}Erro ao buscar informações do mundo!")
            enter_continue()
            return
    
    while True:
        limpar_terminal()
        cabecalho_forja()
        print("\n")
        print(f"{Style.BRIGHT}{Fore.CYAN}Qual ação você gostaria de realizar?".center(largura_terminal))
        print("\n")
        print(f"{Fore.WHITE}1 - Ver itens disponíveis para fabricar")
        print(f"{Fore.WHITE}2 - Fabricar um item")
        print(f"{Fore.WHITE}0 - Sair da Forja")
        print("\n")
        
        escolha = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip()
        
        if escolha == "1":
            menu_categoria_itens(jogador, modo="ver")
        elif escolha == "2":
            menu_categoria_itens(jogador, modo="fabricar")
        elif escolha == "0":
            exibir_dialogo_despedida("Andrei", jogador)
            enter_continue()
            break
        else:
            print(f"\n{Fore.RED}Opção inválida. Tente novamente.")
            enter_continue()

def menu_categoria_itens(jogador, modo):
    """
    Menu de escolha por categoria de item
    """
    categorias = ["Arco", "Bandana", "Botas", "Capacete", "Espada", "Peitoral"]
    
    while True:
        limpar_terminal()
        print(f"{Style.BRIGHT}{Fore.CYAN}Escolha uma categoria de item:".center(largura_terminal))
        print("\n")
        for idx, cat in enumerate(categorias, start=1):
            print(f"{Fore.WHITE}{idx} - {cat}")
        print(f"{Fore.WHITE}0 - Voltar")
        print("\n")
        
        escolha = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip()
        
        if escolha == "0":
            break
        elif escolha.isdigit() and 1 <= int(escolha) <= len(categorias):
            categoria = categorias[int(escolha) - 1]
            if modo == "ver":
                ver_itens_disponiveis(jogador, categoria)
            elif modo == "fabricar":
                fabricar_item(jogador, categoria)
            enter_continue()
        else:
            print(f"\n{Fore.RED}Opção inválida. Tente novamente.")
            enter_continue()
           

def ver_itens_disponiveis(jogador, categoria):
    """
    Função para ver itens disponíveis para fabricar por categoria
    """
    limpar_terminal()
    cabecalho_forja()
    
    # Exibir diálogo de catálogo
    exibir_dialogo_catalogo("Andrei", jogador)
    enter_continue()
    
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== ITENS DISPONÍVEIS PARA FABRICAR ({categoria}) ===".center(largura_terminal))
    print("\n")
    
    # Buscar itens filtrados pela categoria
    itens = visualizar_itens_forja_por_jogador(jogador, categoria)
    
    if itens:
        print(f"{Fore.WHITE}{'ID':<5} {'Nome':<25} {'Preço':<10}")
        print(f"{Fore.LIGHTBLACK_EX}{'='*45}")
        for item in itens:
            id_item, nome, preco_base, descricao = item
            print(f"{Fore.WHITE}{id_item:<5} {nome:<25} {preco_base:<10}")
            print(f"{Fore.LIGHTBLACK_EX}     {descricao}")
            print()  # Linha em branco entre itens
    else:
        print(f"{Fore.RED}Nenhum item disponível para fabricar!")
    
    print("\n")
    enter_continue()

def fabricar_item(jogador, categoria):
    """
    Função para fabricar um item de uma categoria específica
    """
    limpar_terminal()
    cabecalho_forja()
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== FABRICAR ITEM ({categoria}) ===".center(largura_terminal))
    print("\n")
    
    # Mostrar itens disponíveis da categoria escolhida
    itens = visualizar_itens_forja_por_jogador(jogador, categoria)
    if not itens:
        print(f"{Fore.RED}Nenhum item disponível para fabricar na categoria {categoria.lower()}!")
        enter_continue()
        return
    
    print(f"{Fore.WHITE}{'ID':<5} {'Nome':<25} {'Preço':<10}")
    print(f"{Fore.LIGHTBLACK_EX}{'='*45}")
    for item in itens:
        id_item, nome, preco_base, descricao = item
        print(f"{Fore.WHITE}{id_item:<5} {nome:<25} {preco_base:<10}")
    
    print(f"\n{Fore.WHITE}Digite o ID do item que deseja fabricar:")
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
        
        # Exibir diálogo de fabricação
        exibir_dialogo_fabricacao("Andrei", jogador)
        
        # Fabricar o item
        sucesso = forjar_item_por_jogador(jogador, item_id)
        
        if sucesso:
            print(f"\n{Fore.GREEN}✅ Item fabricado com sucesso!")
        else:
            print(f"\n{Fore.RED}❌ Erro ao fabricar item!")
            
    except ValueError:
        print(f"{Fore.RED}Por favor, digite um número válido!")
    except Exception as e:
        print(f"{Fore.RED}Erro inesperado: {e}")
    
    print("\n")
    enter_continue()
