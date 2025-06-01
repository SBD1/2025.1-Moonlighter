from iniciar_jogo import iniciar_jogo
from colorama import Fore, Style, init
import pygame
import os

# definicoes e funcoes iniciais
init(autoreset=True) #terminal colorido

def musicTheme():
    pygame.mixer.init() #musica
    pygame.mixer.music.load("apps/docs/docs/musics/MoonlighterOST_01_TitleScreen.mp3")
    pygame.mixer.music.play(-1, fade_ms=3000)

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def enter_continue():
    input(Fore.LIGHTBLACK_EX + "\nPressione Enter para continuar...")

#funcao principal
def tela_inicial():
    while True:
        musicTheme()
        limpar_terminal()

        print(Style.BRIGHT + Fore.CYAN + "== MOONLIGHT ==\n")

        print("1- continuar")
        print(Fore.LIGHTBLACK_EX +  "2 - novo Jogo")
        print(Fore.LIGHTBLACK_EX +  "0 - sair")

        try:
            escolha:int = int(input("\nDigite: "))
        except ValueError:
            print("Por favor, digite um número válido.")
            enter_continue()
            continue

        if (escolha == 0):
            exit()

        if (escolha == 1): #continuar
            pygame.mixer.music.stop()
            iniciar_jogo() 

# Executa a tela inicial
if __name__ == '__main__':
    tela_inicial()