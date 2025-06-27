import time
from pages.Estabelecimento.db_estabelecimento import *
from pages.IniciarJogo.db_iniciarJogo import buscar_seed_mundo
from pages.Estabelecimento.db_estabelecimento import (
    verificar_instancia_banco_por_jogador,
    visualizar_saldo_banco_por_jogador,
    aplicar_ouro_banco_por_jogador
)
from utils.limparTerminal import limpar_terminal
from utils.enterContinue import enter_continue
from colorama import Fore, Back, Style, init
import pygame
import shutil

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

def cabecalho_banco():
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}=================== BANCO ===================".center(largura_terminal))
    print(f"{Fore.YELLOW}Banco de Rynoka - Serviços Bancários".center(largura_terminal))
    print(f"{Fore.LIGHTGREEN_EX}========================================================".center(largura_terminal))

def menu_banco(jogador):
    """
    Menu principal do banco
    """
    init(autoreset=True)
    
    # Verificar e criar instância do banco se necessário
    if not verificar_instancia_banco_por_jogador(jogador):
        # Buscar seed_mundo para criar instância
        seed_mundo = buscar_seed_mundo(jogador)
        if seed_mundo:
            # Criar instância do banco
            sucesso = criar_instancia_banco(seed_mundo, "Banco de Rynoka", 1, 0)
            if not sucesso:
                print(f"{Fore.RED}Erro ao inicializar o banco!")
                enter_continue()
                return
        else:
            print(f"{Fore.RED}Erro ao buscar informações do mundo!")
            enter_continue()
            return
    
    while True:
        limpar_terminal()
        cabecalho_banco()
        print("\n")
        print(f"{Style.BRIGHT}{Fore.CYAN}O que você gostaria de fazer?".center(largura_terminal))
        print("\n")
        print(f"{Fore.WHITE}1 - Visualizar saldo disponível no banco")
        print(f"{Fore.WHITE}2 - Aplicar uma nova quantidade de ouro no banco")
        print(f"{Fore.WHITE}0 - Sair do Banco")
        print("\n")
        
        escolha = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip()
        
        if escolha == "1":
            visualizar_saldo(jogador)
        elif escolha == "2":
            aplicar_ouro(jogador)
        elif escolha == "0":
            print(f"\n{Fore.YELLOW}Obrigado pela visita! Volte sempre!")
            enter_continue()
            break
        else:
            print(f"\n{Fore.RED}Opção inválida. Tente novamente.")
            enter_continue()

def visualizar_saldo(jogador):
    """
    Função para visualizar o saldo no banco
    """
    limpar_terminal()
    cabecalho_banco()
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== SALDO BANCÁRIO ===".center(largura_terminal))
    print("\n")
    
    saldo_info = visualizar_saldo_banco_por_jogador(jogador)
    if saldo_info:
        saldo_atual, valor_entrada, nome_local = saldo_info
        print(f"{Fore.WHITE}Local: {nome_local}")
        print(f"{Fore.YELLOW}Saldo Atual: {saldo_atual} ouros")
        print(f"{Fore.CYAN}Valor de Entrada: {valor_entrada} ouros")
        print(f"{Fore.GREEN}Total Aplicado: {saldo_atual - valor_entrada} ouros")
    else:
        print(f"{Fore.RED}Erro ao buscar saldo do banco!")
    
    print("\n")
    enter_continue()

def aplicar_ouro(jogador):
    """
    Função para aplicar ouro no banco
    """
    limpar_terminal()
    cabecalho_banco()
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== APLICAR OURO NO BANCO ===".center(largura_terminal))
    print("\n")
    
    # Mostrar saldo atual
    saldo_info = visualizar_saldo_banco_por_jogador(jogador)
    if saldo_info:
        saldo_atual, _, _ = saldo_info
        print(f"{Fore.YELLOW}Saldo Atual: {saldo_atual} ouros")
    
    print(f"\n{Fore.WHITE}Digite a quantidade de ouro que deseja aplicar:")
    try:
        quantidade = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> "))
        
        if quantidade <= 0:
            print(f"{Fore.RED}Quantidade deve ser maior que zero!")
            enter_continue()
            return
        
        # Aplicar ouro no banco
        sucesso = aplicar_ouro_banco_por_jogador(jogador, quantidade)
        
        if sucesso:
            print(f"\n{Fore.GREEN}✅ {quantidade} ouros aplicados com sucesso!")
            
            # Mostrar novo saldo
            novo_saldo_info = visualizar_saldo_banco_por_jogador(jogador)
            if novo_saldo_info:
                novo_saldo, _, _ = novo_saldo_info
                print(f"{Fore.YELLOW}Novo Saldo: {novo_saldo} ouros")
        else:
            print(f"\n{Fore.RED}❌ Erro ao aplicar ouro no banco!")
            
    except ValueError:
        print(f"{Fore.RED}Por favor, digite um número válido!")
    except Exception as e:
        print(f"{Fore.RED}Erro inesperado: {e}")
    
    print("\n")
    enter_continue() 