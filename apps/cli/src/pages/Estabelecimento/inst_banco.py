import time
from pages.Estabelecimento.db_estabelecimento import *
from pages.Estabelecimento.db_estabelecimento import (
    verificar_instancia_banco_por_jogador,
    visualizar_saldo_banco_por_jogador,
    aplicar_ouro_banco_por_jogador,
    criar_instancia_banco_por_jogador,
    sacar_ouro_banco_por_jogador,
    sacar_tudo_banco_por_jogador,
    exibir_dialogo_saudacao,
    exibir_dialogo_aplicar,
    exibir_dialogo_sacar,
    exibir_dialogo_despedida,
    exibir_dialogo_apos_aplicar
)
from utils.limparTerminal import limpar_terminal
from utils.enterContinue import enter_continue
from colorama import Fore, Back, Style, init
import pygame
import shutil
from setup.database import connect_to_db
from pages.IniciarJogo.db_iniciarJogo import *

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

def print_in_centered(text):
    largura_terminal = shutil.get_terminal_size().columns
    # Quebra o texto em linhas que caibam no terminal
    linhas = textwrap.wrap(text, width=largura_terminal - 4)  # margem para centralizar
    for linha in linhas:
        linha_centralizada = linha.center(largura_terminal)
        print(Style.BRIGHT + Fore.WHITE + linha_centralizada)


def cabecalho_banco(nickname):
    dadosJogador = buscar_dadosJogador(nickname)
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╔═════════════════════════════════════       BANCO       ═════════════════════════════════════╗".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}Banco de Rynoka - Serviços Bancários".center(largura_terminal))
    print(f"{Fore.LIGHTGREEN_EX}════════════════════════════════════════════════════════════════════════════".center(largura_terminal))
    print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}{dadosJogador[0]}".center(largura_terminal))
    print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}OURO: {dadosJogador[3]}".center(largura_terminal))
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╚═══════════════════════════════════════════════════════════════════════════════════════════╝".center(largura_terminal))

    print("\n")
    print_in_centered(buscarDescricaoLocal(dadosJogador[6]))
    print("\n")

def menu_banco(jogador):
    """
    Menu principal do banco
    """
    init(autoreset=True)
    
    # Exibir diálogo de saudação do banqueiro
    limpar_terminal()
    cabecalho_banco(jogador)
    exibir_dialogo_saudacao("Edward", jogador)
    enter_continue()
    
    #verifica e cria instancia do banco por precaucao
    if not verificar_instancia_banco_por_jogador(jogador):
        sucesso = criar_instancia_banco_por_jogador(jogador, "Banco de Rynoka", 1, 0)
        if not sucesso:
            print(f"{Fore.RED}Erro ao inicializar o banco!")
            enter_continue()
            return
    
    while True:
        limpar_terminal()
        cabecalho_banco(jogador)
        print("\n")
        print(f"{Style.BRIGHT}{Fore.CYAN}O que você gostaria de fazer?".center(largura_terminal))
        print("\n")
        print(f"{Fore.YELLOW}{Style.BRIGHT}1 - Visualizar saldo disponível no banco")
        print(f"{Fore.YELLOW}{Style.BRIGHT}2 - Aplicar uma nova quantidade de ouro no banco")
        print(f"{Fore.YELLOW}{Style.BRIGHT}3 - Sacar uma quantidade de ouro do banco")
        print(f"{Fore.YELLOW}{Style.BRIGHT}4 - Sacar TODO o saldo do banco")
        print(f"{Fore.RED}{Style.BRIGHT}5 - Sair do Banco")
        print("\n")
        
        escolha = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip()
        
        if escolha == "1":
            visualizar_saldo(jogador)
        elif escolha == "2":
            aplicar_ouro(jogador)
        elif escolha == "3":
            sacar_ouro(jogador)
        elif escolha == "4":
            sacar_tudo(jogador)
        elif escolha == "5":
            limpar_terminal()
            cabecalho_banco(jogador)
            print("\n\n\n\n")
            exibir_dialogo_despedida("Edward", jogador)
            atualizarParaLocalAnterior(buscar_dadosJogador(jogador))
            enter_continue()
            break
        else:
            limpar_terminal()
            cabecalho_banco(jogador)
            print("\n\n\n\n")
            print(f"{Fore.RED}{Style.BRIGHT}Opção inválida. Tente novamente.".center(largura_terminal))
            enter_continue()

def visualizar_saldo(jogador):
    """
    Função para visualizar o saldo no banco
    """
    limpar_terminal()
    cabecalho_banco(jogador)

    print("\n")
    print(f"{Style.BRIGHT}{Fore.CYAN}╔════════════   SALDO BANCÁRIO   ════════════╗".center(largura_terminal + 4))
    print("\n")
    
    saldo_info = visualizar_saldo_banco_por_jogador(jogador)
    if saldo_info:
        saldo_atual, valor_entrada, nome_local = saldo_info
        print(f"{Fore.WHITE}Local: {nome_local}".center(largura_terminal))
        print(f"{Fore.LIGHTBLACK_EX}═════════════════════════════════════════════".center(largura_terminal))
        print(f"{Fore.YELLOW}Saldo Atual: {saldo_atual} ouros".center(largura_terminal))
        print(f"{Fore.LIGHTBLACK_EX}═════════════════════════════════════════════".center(largura_terminal))
        print(f"{Fore.CYAN}Valor de Entrada: {valor_entrada} ouros".center(largura_terminal))
        print(f"{Fore.LIGHTBLACK_EX}═════════════════════════════════════════════".center(largura_terminal))
        print(f"{Fore.GREEN}Total Aplicado: {saldo_atual - valor_entrada} ouros".center(largura_terminal))
        print(f"{Fore.CYAN}╚═════════════════════════════════════════════╝".center(largura_terminal))
    else:
        print(f"{Fore.RED}Erro ao buscar saldo do banco!")
    
    print("\n")
    enter_continue()

def aplicar_ouro(jogador):
    """
    Função para aplicar ouro no banco
    """
    limpar_terminal()
    cabecalho_banco(jogador)
    
    # Exibir diálogo de aplicar
    exibir_dialogo_aplicar("Edward", jogador)
    enter_continue()
    limpar_terminal()
    cabecalho_banco(jogador)
    print(f"{Style.BRIGHT}{Fore.CYAN}══════════ APLICAR OURO NO BANCO ══════════".center(largura_terminal))
    print("\n")
    
    # Mostrar ouro atual do jogador
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT ouro FROM jogador WHERE nickname = %s", (jogador,))
            resultado = cursor.fetchone()
            if resultado:
                ouro_atual = resultado[0]
                print(f"{Fore.YELLOW}{Style.BRIGHT}Ouro disponível: {ouro_atual} ouros".center(largura_terminal))
            cursor.close()
            connection.close()
        except:
            if connection:
                connection.close()
    
    # Mostrar saldo atual do banco
    saldo_info = visualizar_saldo_banco_por_jogador(jogador)
    if saldo_info:
        saldo_atual, _, _ = saldo_info
        print(f"{Fore.CYAN}{Style.BRIGHT}Saldo no banco: {saldo_atual} ouros".center(largura_terminal))
    
    print(f"{Fore.WHITE}{Style.BRIGHT}Digite a quantidade de ouro que deseja aplicar:")
    try:
        quantidade = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> "))
        
        if quantidade <= 0:
            limpar_terminal()
            cabecalho_banco(jogador)
            print("\n\n\n\n")
            print(f"{Fore.RED}{Style.BRIGHT}Quantidade deve ser maior que zero!".center(largura_terminal))
            enter_continue()
            return
        
        # Aplicar ouro no banco
        sucesso = aplicar_ouro_banco_por_jogador(jogador, quantidade)
        
        if sucesso:
            limpar_terminal()
            cabecalho_banco(jogador)
            print("\n\n\n\n")
            print(f"{Fore.GREEN}✅ {quantidade} ouros aplicados com sucesso!".center(largura_terminal))
            
            # Mostrar novo saldo
            novo_saldo_info = visualizar_saldo_banco_por_jogador(jogador)
            if novo_saldo_info:
                novo_saldo, _, _ = novo_saldo_info
                print(f"{Fore.YELLOW}Novo Saldo no Banco: {novo_saldo} ouros".center(largura_terminal))
        else:
            limpar_terminal()
            cabecalho_banco(jogador)
            print("\n\n\n\n")
            print(f"\n{Fore.RED}{Style.BRIGHT}❌ Erro ao aplicar ouro no banco!".center(largura_terminal))

    except ValueError:
        limpar_terminal()
        cabecalho_banco(jogador)
        print("\n\n\n\n")
        print(f"{Fore.RED}{Style.BRIGHT}Por favor, digite um número válido!".center(largura_terminal))
    except Exception as e:
        limpar_terminal()
        cabecalho_banco(jogador)
        print("\n\n\n\n")
        print(f"{Fore.RED}{Style.BRIGHT}Erro inesperado: {e}".center(largura_terminal))

    print("\n")
    enter_continue()
    limpar_terminal()
    exibir_dialogo_apos_aplicar("Edward", jogador)
    enter_continue()
    limpar_terminal()

def sacar_ouro(jogador):
    """
    Função para sacar uma quantidade de ouro do banco
    """
    limpar_terminal()
    cabecalho_banco(jogador)

    enter_continue()

    print(f"{Style.BRIGHT}{Fore.CYAN}══════════ SACAR OURO DO BANCO ══════════".center(largura_terminal))
    print("\n")
    saldo_info = visualizar_saldo_banco_por_jogador(jogador)
    if saldo_info:
        saldo_atual, _, _ = saldo_info
        print(f"{Fore.CYAN}Saldo disponível no banco: {saldo_atual} ouros".center(largura_terminal))
    else:
        limpar_terminal()
        cabecalho_banco(jogador)
        print("\n\n\n\n")
        print(f"{Fore.RED}{Style.BRIGHT}Erro ao buscar saldo do banco!".center(largura_terminal))
        enter_continue()
        return
    print(f"\n{Fore.WHITE}Digite a quantidade de ouro que deseja sacar:")
    try:
        quantidade = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> "))
        if quantidade <= 0:
            limpar_terminal()
            cabecalho_banco(jogador)
            print("\n\n\n\n")
            print(f"{Fore.RED}{Style.BRIGHT}Quantidade deve ser maior que zero!".center(largura_terminal))
            enter_continue()
            return
        sucesso = sacar_ouro_banco_por_jogador(jogador, quantidade)
        if sucesso:
            print(f"\n{Fore.GREEN}✅ {quantidade} ouros sacados com sucesso!".center(largura_terminal))
            novo_saldo_info = visualizar_saldo_banco_por_jogador(jogador)
            if novo_saldo_info:
                novo_saldo, _, _ = novo_saldo_info
                print(f"{Fore.YELLOW}Novo Saldo no Banco: {novo_saldo} ouros".center(largura_terminal))
    except ValueError:
        limpar_terminal()
        cabecalho_banco(jogador)
        print("\n\n\n\n")
        print(f"{Fore.RED}{Style.BRIGHT}Por favor, digite um número válido!".center(largura_terminal))
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}Erro inesperado: {e}".center(largura_terminal))
    print("\n")
    enter_continue()
    limpar_terminal()
    # Exibir diálogo de sacar
    exibir_dialogo_sacar("Edward", jogador)
    enter_continue()
    limpar_terminal()

def sacar_tudo(jogador):
    """
    Função para sacar todo o saldo do banco
    """
    limpar_terminal()
    cabecalho_banco(jogador)
    print(f"\n{Style.BRIGHT}{Fore.CYAN}══════════ SACAR TODO O SALDO DO BANCO ══════════".center(largura_terminal))
    print("\n")
    sucesso = sacar_tudo_banco_por_jogador(jogador)
    if sucesso:
        novo_saldo_info = visualizar_saldo_banco_por_jogador(jogador)
        if novo_saldo_info:
            novo_saldo, _, _ = novo_saldo_info
            print(f"{Fore.YELLOW}Novo Saldo no Banco: {novo_saldo} ouros".center(largura_terminal))
    print("\n")
    enter_continue()
    limpar_terminal()
    exibir_dialogo_sacar("Edward", jogador)
    enter_continue()
    limpar_terminal()