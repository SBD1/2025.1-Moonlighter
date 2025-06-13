from colorama import Fore, Back, Style, init
import pygame
import os

# definicoes e funcoes iniciais
def musicMasmorraGolem(): #musica da masmorra
    pygame.mixer.init() 
    pygame.mixer.music.load("apps/docs/docs/musics/MoonlighterOST_07_MasmorraGolem.mp3")
    pygame.mixer.music.play(-1, fade_ms=3000)

def musicGolemKing(): #musica da chefe da masmorra
    pygame.mixer.init() 
    pygame.mixer.music.load("apps/docs/docs/musics/MoonlighterOST_08_GolemKing.mp3")
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