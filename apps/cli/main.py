from iniciar_jogo import iniciar_jogo
from colorama import Fore, Style, init
import os

# definicoes e funcoes iniciais
init(autoreset=True)

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def enter_continue():
    input(Fore.LIGHTBLACK_EX + "\nPressione Enter para continuar...")

#funcao principal
def tela_inicial():
    while True:
        limpar_terminal()

        print(Style.BRIGHT + Fore.CYAN + "== MOONLIGHT ==\n")

        print("1- continuar")
        print(Fore.LIGHTBLACK_EX +  "2 - novo Jogo")
        print(Fore.LIGHTBLACK_EX +  "0 - sair")

        escolha: int = int(input("\nDigite: "))

        if (escolha == 0):
            print("Saindo...")
            exit()

        if (escolha == 1): #continuar
            iniciar_jogo() 

# Executa a tela inicial
if __name__ == '__main__':
    tela_inicial()