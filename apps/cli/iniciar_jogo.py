from colorama import Fore, Back, Style, init
import pygame
import subprocess
import os

# definicoes e funcoes iniciais
init(autoreset=True) #terminal colorido

def musicCity(): #musica da cidade
    pygame.mixer.init() 
    pygame.mixer.music.load("apps/docs/docs/musics/MoonlighterOST_02_Cidade.mp3")
    pygame.mixer.music.play(-1, fade_ms=3000)

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def enter_continue():
    input(Fore.LIGHTBLACK_EX + "\nPressione Enter para continuar...")

#funcao principal
def iniciar_jogo():
    musicCity()
    local_jogador: str = 'loja' # o jogador sempre comeca o jogo em sua loja 

    # loop dos locais no terminal
    while True:
        limpar_terminal()
        print(Fore.YELLOW + f"dia: XX, turno: XX, local: {local_jogador}")
        print(Style.BRIGHT + Fore.CYAN + "Para onde deseja ir?\n")

        if (local_jogador != 'loja'):                   print("l- ir para minha loja")
        if (local_jogador != 'area das masmorras'):     print("m- ir para a area das masmorras")
        if (local_jogador != 'forjaria'):               print("f- ir para a forjaria")
        if (local_jogador != 'varejo'):                 print("v- ir para o varejo")
        if (local_jogador != 'banco'):                  print("b- ir para o banco")

        print(Fore.LIGHTBLACK_EX + "x- sair do jogo")

        escolha: str = input("\nDigite: ")

        if (escolha == 'x'): #sair do jogo
            pygame.mixer.music.stop()
            print("Salvando seu progresso...")
            print("Jogo salvo!")
            enter_continue()
            break;

        if (escolha == 'l'): #loja do jogador        
            local_jogador = 'loja'
            limpar_terminal()

            print(Fore.YELLOW + f"dia: XX, turno: XX, local: {local_jogador}")
            print("Parece que nao ha nada a o que fazer aqui ainda, volte mais tarde!")
            enter_continue()

        if (escolha == 'm'): #area das masmorras
            local_jogador = 'area das masmorras'

            while True: #loop nterno do lobby das masmorras
                limpar_terminal()
                print(Fore.YELLOW + f"dia: XX, turno: XX, local: {local_jogador}")
                print("Qual masmorra deseja entrar?\n")

                print("1- Masmorra do golem")
                print(Fore.RED + "2- Masmorra da floresta")
                print(Fore.RED + "3- Masmorra do deserto")
                print(Fore.RED + "4- Masmorra tech")
                print(Fore.RED + "5- Masmorra desconhecida")
                print(Fore.LIGHTBLACK_EX + "0- voltar")

                escolha_masmorra: int = int(input("\nDigite: "))

                if(escolha_masmorra == 0): #voltar
                    break

                if(escolha_masmorra == 1):
                    print("Parece que nao ha nada a o que fazer aqui ainda, volte mais tarde!")
                    enter_continue()
                
                if(escolha_masmorra == 2):
                    print("Masmorra nao desbloqueada")
                    enter_continue()

                if(escolha_masmorra == 3):
                    print("Masmorra nao desbloqueada")
                    enter_continue()

                if(escolha_masmorra == 4):
                    print("Masmorra nao desbloqueada")
                    enter_continue()

                if(escolha_masmorra == 5):
                    print("Masmorra nao desbloqueada")
                    enter_continue()

        if (escolha == 'f'): #forjaria        
            local_jogador = 'forjaria'
            limpar_terminal()

            print(Fore.YELLOW + f"dia: XX, turno: XX, local: {local_jogador}")
            print("Parece que nao ha nada a o que fazer aqui ainda, volte mais tarde!")
            enter_continue()

        if (escolha == 'v'): #varejo       
            local_jogador = 'varejo'
            limpar_terminal()

            print(Fore.YELLOW + f"dia: XX, turno: XX, local: {local_jogador}")
            print("Parece que nao ha nada a o que fazer aqui ainda, volte mais tarde!")
            enter_continue()

        if (escolha == 'b'): #banco       
            local_jogador = 'banco'
            limpar_terminal()

            print(Fore.YELLOW + f"dia: XX, turno: XX, local: {local_jogador}")
            print("Parece que nao ha nada a o que fazer aqui ainda, volte mais tarde!")
            enter_continue()