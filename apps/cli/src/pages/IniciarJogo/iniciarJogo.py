import time
import pyfiglet
from pages.IniciarJogo.db_iniciarJogo import *
from utils.limparTerminal import limpar_terminal
from utils.enterContinue import enter_continue
from colorama import Fore, Back, Style, init
import pygame
import subprocess
import platform
import os
import shutil
import textwrap

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

# definição da Logo do Jogo centralizada:
ascii = pyfiglet.figlet_format("MOONLIGHTER")
centralizacao = "\n".join([linha.center(largura_terminal) for linha in ascii.splitlines()])
logo = f"{Style.BRIGHT + Fore.LIGHTGREEN_EX}\n\n{centralizacao}\n\n\n"

def musicCity(): #musica da cidade
    pygame.mixer.init() 
    pygame.mixer.music.load("apps/cli/assets/musics/MoonlighterOST_02_Cidade.mp3")
    pygame.mixer.music.play(-1, fade_ms=3000)

def print_in_centered(text):
    largura_terminal = shutil.get_terminal_size().columns
    # Quebra o texto em linhas que caibam no terminal
    linhas = textwrap.wrap(text, width=largura_terminal - 4)  # margem para centralizar
    for linha in linhas:
        linha_centralizada = linha.center(largura_terminal)
        print(Style.BRIGHT + Fore.WHITE + linha_centralizada)

def cabecalho(nickname):
        
    dadosJogador = buscar_dadosJogador(nickname)

    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╔════════════════════[ MOONLIGHTER GAME ]════════════════════╗".center(largura_terminal))
    print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}{dadosJogador[0]}".center(largura_terminal))
    print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}HP: {dadosJogador[1]} / {dadosJogador[2]} | OURO: {dadosJogador[3]}".center(largura_terminal))
    print("\n")
    if dadosJogador[4] == -1:
        print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}{dadosJogador[6]}".center(largura_terminal))
        print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}DIA: XX | PERÍODO: XX".center(largura_terminal))
    else:
        print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}MASMORRA: {dadosJogador[6]} | SEED: XXX".center(largura_terminal))
        print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}SALA [Posição Horizontal][Posição Vertical]: [{dadosJogador[3]}][{dadosJogador[4]}]".center(largura_terminal))
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╚════════════════════════════════════════════════════════════╝".center(largura_terminal))
    
    print("\n")

    print_in_centered(buscarDescricaoLocal(dadosJogador[6]))
    print("\n")

def locomocao(nickname):
    while True:
        dadosJogador = buscar_dadosJogador(nickname)
        limpar_terminal()
        cabecalho(nickname)
        print(f"{Style.BRIGHT}{Fore.YELLOW}Escolha um local para se mover:".center(largura_terminal))
        print("\n")

        locais = exibir_locais(dadosJogador[6])
        if (dadosJogador[6] != 'Vila Rynoka'): locais.append(('Voltar ao Local Anterior',))
        locais.append(('Encerrar Locomoção',))

        for i, local in enumerate(locais, start=1):
            if local[0] == "Encerrar Locomoção":
                print(f"{Fore.RED}{Style.BRIGHT}{i} - {local[0]}")
            elif local[0] == "Voltar ao Local Anterior":
                print(f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{i} - {local[0]}")
            else:
                print(f"{Fore.YELLOW}{Style.BRIGHT}{i} - {local[0]}")

        print("\n\n\n\n" + f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Digite o número da opção desejada:")
        entrada = input(f"{Style.BRIGHT}{Fore.MAGENTA}>> ")
        
        if entrada == '':
            limpar_terminal()
            print('\033[?25l', end='', flush=True)
            print("\n\n\n\n\n\n\n\n")
            print(f"{Style.BRIGHT}{Fore.RED}Por favor, digite um número.".center(largura_terminal))
            time.sleep(2)
            print('\033[?25h', end='', flush=True)
            continue

        if entrada < '1' or entrada > str(len(locais)):
            limpar_terminal()
            print('\033[?25l', end='', flush=True)
            print("\n\n\n\n\n\n\n\n")
            print(f"{Style.BRIGHT}{Fore.RED}Opção inválida. Por favor, escolha um número válido.".center(largura_terminal))
            time.sleep(2)
            print('\033[?25h', end='', flush=True)
            continue

        try:
            escolha = int(entrada)
            
            if locais[escolha - 1][0] == 'Encerrar Locomoção':
                return
            elif locais[escolha - 1][0] == 'Voltar ao Local Anterior':
                atualizarParaLocalAnterior(dadosJogador)
                continue
            else:
                atualizar_local_jogador(locais[escolha - 1][0], nickname)

        except ValueError:
            limpar_terminal()
            print('\033[?25l', end='', flush=True)
            print("\n\n\n\n\n\n\n\n")
            print(f"{Style.BRIGHT}{Fore.RED}Por favor, digite um número válido.".center(largura_terminal))
            time.sleep(2)
            print('\033[?25h', end='', flush=True)
            continue

def exibirOpcoes():

    print(f"{Style.BRIGHT}{Fore.YELLOW}Ações disponíveis:".center(largura_terminal))
    print("\n")
    print(f"{Style.BRIGHT}{Fore.YELLOW}1 - Visualizar mapa de Rynoka")
    print(f"{Style.BRIGHT}{Fore.YELLOW}2 - Mover-se para outro local")
    print(f"{Style.BRIGHT}{Fore.YELLOW}3 - Ver Inventário")
    print(f"{Style.BRIGHT}{Fore.YELLOW}4 - Ver Status do Jogador")
    print(f"{Style.BRIGHT}{Fore.RED}5 - Voltar ao Menu Principal")

    print("\n\n\n\n" + f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Digite o número da opção desejada:")
    escolha = input(f"{Style.BRIGHT}{Fore.MAGENTA}>> ")
    
    return escolha

def sairDoJogo():
    limpar_terminal()
    print(logo)

    print(f"{Style.BRIGHT}{Fore.YELLOW}Você tem certeza que deseja voltar ao Menu Principal?".center(largura_terminal))
    print("\n")
    print(f"{Fore.WHITE}Digite 's' para sair ou 'n' para cancelar.".center(largura_terminal))

    print("\n\n\n\n\n")
    confirmacao = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip().lower()

    if confirmacao == 's' or confirmacao == 'S':
        print('\033[?25l', end='', flush=True)
        limpar_terminal()
        print(logo)
        print("\n\n\n")
        print(f"{Style.BRIGHT}{Fore.RED}Voltando ao Menu Principal...".center(largura_terminal))
        pygame.mixer.music.fadeout(7000)
        time.sleep(2)
        limpar_terminal()
        print("\n\n\n\n\n\n\n\n\n\n")
        print(logo)
        time.sleep(7)
        return True
    elif confirmacao == 'n' or confirmacao == 'N':
        return False

def exibirMapa():
    script_path = os.path.abspath("apps/cli/src/actions/mapa.py")
    sistema = platform.system()

    if sistema == "Windows":
        subprocess.Popen(f'start cmd /k python "{script_path}"', shell=True)
    elif sistema == "Linux":
        subprocess.Popen(['gnome-terminal', '--', 'python3', script_path])
    else:
        print("Sistema operacional não suportado para abrir nova janela de terminal.")

#funcao principal
def iniciar_jogo(nickname):
    init(autoreset=True) #terminal colorido
    musicCity()
    # loop dos locais no terminal
    while True:

        limpar_terminal()
        cabecalho(nickname)
        escolha = exibirOpcoes()

        try:
            if int(escolha) == 1:
                exibirMapa()
            elif int(escolha) == 2:
                locomocao(nickname)
            elif int(escolha) == 5:
                if sairDoJogo():
                    break
            else:
                limpar_terminal()
                print('\033[?25l', end='', flush=True)
                print("\n\n\n\n\n\n\n\n")
                print(f"{Style.BRIGHT}{Fore.RED}Opção inválida!".center(largura_terminal))
                time.sleep(2)
                print('\033[?25h', end='', flush=True)
        except ValueError:
            limpar_terminal()
            print('\033[?25l', end='', flush=True)
            print("\n\n\n\n\n\n\n\n")
            print(f"{Style.BRIGHT}{Fore.RED}Opção inválida!".center(largura_terminal))
            time.sleep(2)
            print('\033[?25h', end='', flush=True)