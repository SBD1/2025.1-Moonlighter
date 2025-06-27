from colorama import Fore, Back, Style, init
from pages.Masmorra.db_masmorra import *
import pygame
import pyfiglet
import os
import shutil
import time
from utils.geracaoProceduralMasmorra import gerarMasmorra

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

# definição da Logo do Jogo centralizada:
ascii = pyfiglet.figlet_format("MOONLIGHTER")
centralizacao = "\n".join([linha.center(largura_terminal) for linha in ascii.splitlines()])
logo = f"{Style.BRIGHT + Fore.LIGHTGREEN_EX}\n\n{centralizacao}\n\n\n"

# definicoes e funcoes iniciais
def musicMasmorraGolem(): #musica da masmorra
    pygame.mixer.init() 
    pygame.mixer.music.load("apps/cli/assets/musics/MoonlighterOST_07_MasmorraGolem.mp3")
    pygame.mixer.music.play(-1, fade_ms=3000)

def musicMasmorraEntrance():
    pygame.mixer.init()
    pygame.mixer.music.load("apps/cli/assets/musics/MoonlighterOST_06_SentientStone.mp3")
    pygame.mixer.music.play(-1, fade_ms=3000)

def musicCity(): #musica da cidade
    pygame.mixer.init() 
    pygame.mixer.music.load("apps/cli/assets/musics/MoonlighterOST_02_Cidade.mp3")
    pygame.mixer.music.play(-1, fade_ms=3000)

def musicGolemKing(): #musica da chefe da masmorra
    pygame.mixer.init() 
    pygame.mixer.music.load("apps/cli/assets/musics/MoonlighterOST_08_GolemKing.mp3")
    pygame.mixer.music.play(-1, fade_ms=3000)

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def enter_continue():
    input(Fore.LIGHTBLACK_EX + "\nPressione Enter para continuar...")

#mapa da masmorra
def mapa_masmorra():

    mapa: list = [
        "###############",
        "#S............#",
        "#.............#",
        "#.............#",
        "#.............#",
        "#.............#",
        "#.............#",
        "###############"
    ]

    print("\n")
    for linha in mapa:
        for char in linha:
            if char == "#":
                print(Fore.LIGHTBLACK_EX + char, end="")
            elif char == ".":
                print(Fore.WHITE + char, end="")
            elif char == "S":
                print(Fore.GREEN + char, end="")
            elif char == "T":
                print(Fore.YELLOW + char, end="")
        print()
    print("\n")

#funcao da area da masmorra
def area_masmorra():
    init(autoreset=True) #terminal colorido
    limpar_terminal()
    musicMasmorraGolem()

    while True:
        print(Fore.RED + f"Vida: XX")
        print(Fore.YELLOW + f"dinheiro: $XX.xx")

        mapa_masmorra()

        print("wasd - movimentar personagem")
        print("i - abrir inventario")
        print("x - sair da masmorra (usar pingente)")

        escolha: str = input("\nDigite: ")

        if (escolha == 'x' or escolha == 'X'): #sair da masmorra
            continue

        if (escolha == 'w' or escolha == 'W'):
            continue

        if (escolha == 'a' or escolha == 'A'):
            continue

        if (escolha == 's' or escolha == 'S'):
            continue

        if (escolha == 'd' or escolha == 'D'):
            continue

        if (escolha == 'i' or escolha == 'I'):
            continue

def mainMasmorra(nickname):
    dadosJogador = ObterDadosJogador(nickname)
    dadosMasmorra = ObterDadosMasmorra(dadosJogador[6])
    dadosMundo = ObterDadosMundo(nickname)

    if dadosMasmorra[1] > dadosMundo[4]:
        limpar_terminal()
        print('\033[?25l', end='', flush=True)
        print(logo)
        print("\n\n\n\n")
        atualizarParaLocalAnterior(dadosJogador)
        print(f"{Style.BRIGHT}{Fore.YELLOW}Você ainda se sente muito inseguro para entrar nesta Masmorra.".center(largura_terminal))
        print(f"{Style.BRIGHT}{Fore.RED}Derrote o chefe da Masmorra Anterior primeiro!".center(largura_terminal))
        time.sleep(3)
        print('\033[?25h', end='', flush=True)
        return
    
    musicMasmorraEntrance()
    confirmacao = ''

    while confirmacao not in ['s', 'S', 'n', 'N']:
        limpar_terminal()
        print(logo)
        print("\n\n\n\n")
        print(f"{Style.BRIGHT}{Fore.YELLOW}Você tem certeza que deseja entrar?".center(largura_terminal))
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}{dadosMasmorra[0]}".center(largura_terminal))
        print("\n")
        print(f"{Fore.WHITE}Digite 's' para confirmar ou 'n' para desistir.".center(largura_terminal))

        print("\n\n\n\n\n")
        confirmacao = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip().lower()

        if confirmacao == 'n' or confirmacao == 'N':
            limpar_terminal()
            print('\033[?25l', end='', flush=True)
            print(logo)
            print("\n\n\n\n")
            atualizarParaLocalAnterior(dadosJogador)
            print(f"{Style.BRIGHT}{Fore.YELLOW}Você decidiu não entrar na Masmorra.".center(largura_terminal))
            time.sleep(2)
            print('\033[?25h', end='', flush=True)
            musicCity()
            return
        elif confirmacao == 's' or confirmacao == 'S':
            limpar_terminal()
            print('\033[?25l', end='', flush=True)
            print(logo)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT}{Fore.LIGHTYELLOW_EX}GERANDO MASMORRA...".center(largura_terminal))
            novaMasmorra, seedMasmorra = gerarMasmorra(dadosMasmorra)
            try:
                seedMasmorra = salvarMasmorra(dadosMundo, dadosMasmorra, seedMasmorra, novaMasmorra)
            except Exception as e:
                print(Fore.RED + "Erro ao salvar a masmorra no banco de dados:", e)
                time.sleep(3)
                return
            time.sleep(6)
            limpar_terminal()
            print(logo)
            print("\n\n")
            print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Você entrou na {dadosMasmorra[0]}!".center(largura_terminal))
            print("\n")
            print(f"{Style.BRIGHT}{Fore.YELLOW}════════════════════════════════════════════════════".center(largura_terminal))
            print(f"{Style.BRIGHT}{Fore.YELLOW}SEED DA MASMORRA".center(largura_terminal))
            print(f"{Style.BRIGHT}{Fore.YELLOW}{seedMasmorra}".center(largura_terminal))
            print(f"{Style.BRIGHT}{Fore.YELLOW}════════════════════════════════════════════════════".center(largura_terminal))
            pygame.mixer.music.fadeout(7000)
            time.sleep(7)
            limpar_terminal()
            print('\033[?25h', end='', flush=True)
        else:
            limpar_terminal()
            print('\033[?25l', end='', flush=True)
            print(logo)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT}{Fore.RED}Opção inválida. Por favor, digite 's' ou 'n'.".center(largura_terminal))
            time.sleep(2)
            print('\033[?25h', end='', flush=True)
            continue