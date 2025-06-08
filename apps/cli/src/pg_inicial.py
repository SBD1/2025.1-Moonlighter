from setup.database import connect_to_db
from iniciar_jogo import iniciar_jogo
from colorama import Fore, Style, init
import time
import shutil
import pygame
import pyfiglet
import os

# definicoes e funcoes iniciais
init(autoreset=True) #terminal colorido

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

# definição da Logo do Jogo centralizada:
ascii = pyfiglet.figlet_format("MOONLIGHTER")
centralizacao = "\n".join([linha.center(largura_terminal) for linha in ascii.splitlines()])
logo = f"{Style.BRIGHT + Fore.LIGHTGREEN_EX}\n\n{centralizacao}\n\n\n"

def buscarJogador():
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM jogador;")
    jogador = cursor.fetchall()
    cursor.close()
    connection.close()

    return jogador

def sairDoJogo():
    limpar_terminal()
    print(logo)

    # COMANDO PARA ESCONDER O CURSOR:
    print('\033[?25l', end='', flush=True)

    print("\n\n\n\n\n")
    print(Fore.RED + Style.BRIGHT + "Saindo do jogo...".center(largura_terminal))
    time.sleep(2)
    exit()

def novoJogador():
    limpar_terminal()
    print(logo)

    print(f"{Style.BRIGHT}{Fore.YELLOW}Criação de Jogador".center(largura_terminal))

    print("\n\n\n\n\n")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Insira o nome do novo jogador:")
    nickname = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ")

    limpar_terminal()
    print(logo)
    print("\n\n\n\n\n")
    print(f"{Style.BRIGHT}{Fore.YELLOW}CRIANDO SEU JOGADOR...".center(largura_terminal))
    time.sleep(2)

    try:
        connection = connect_to_db()
        if connection is None:
            print(Fore.RED + "Erro ao conectar ao banco de dados.")
            return
        cursor = connection.cursor()
        cursor.execute("INSERT INTO jogador VALUES (%s, 100, 100, 0, NULL);", (nickname,))
        cursor.execute("INSERT INTO inst_inventario VALUES (1, %s, 0), (2, %s, 0), (3, %s, 0), (4, %s, 0), (5, %s, 0), (6, %s, 0), (7, %s, 0);", tuple([nickname]*7))
        cursor.execute("INSERT INTO \"lojaJogador\" VALUES (%s, 1, 10, 0, 1)", (nickname,))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception:
        limpar_terminal()
        print(logo)
        print("\n\n\n\n\n")
        print(f"{Style.BRIGHT}{Fore.RED}Este jogador já existe!".center(largura_terminal))
        time.sleep(2)
        return novoJogador()
    
    limpar_terminal()
    print(logo)
    print("\n\n\n\n\n\n")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}JOGADOR CRIADO COM SUCESSO!".center(largura_terminal))
    time.sleep(2)
    iniciar_jogo()

def musicTheme():
    pygame.mixer.init() #musica
    pygame.mixer.music.load("apps/docs/docs/musics/MoonlighterOST_01_TitleScreen.mp3")
    pygame.mixer.music.play(-1, fade_ms=3000)

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def enter_continue():
    input(Fore.LIGHTBLACK_EX + "\nPressione Enter para continuar...")

#funcao principal
def tela_inicial(opcoes):
    while True:
        musicTheme()
        limpar_terminal()

        print(logo)

        for i, opcao in enumerate(opcoes):
            construcaoString = f"{Fore.YELLOW}{Style.BRIGHT}{i + 1}. {opcao}"
            opcao_centralizada = construcaoString.center(largura_terminal)
            print(opcao_centralizada)

        try:
            print("\n\n\n\n\n\n\n\n\n" + f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Digite o número da opção desejada:")
            escolha:int = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>> "))
        except ValueError:
            print("Por favor, digite um número válido.")
            enter_continue()
            continue

        if len(jogador) == 0:
            match escolha:
                case 1:
                    novoJogador()
                case 2:
                    sairDoJogo()
                case _:
                    print(Fore.RED + "Opção inválida. Tente novamente.")
                    enter_continue()
        else:
            match escolha:
                case 1:
                    iniciar_jogo()
                case 2:
                    novoJogador()
                case 3:
                    sairDoJogo()
                case _:
                    print(Fore.RED + "Opção inválida. Tente novamente.")
                    enter_continue()

# Executa a tela inicial
if __name__ == '__main__':
    jogador = buscarJogador()

    if len(jogador) == 0:
        tela_inicial(["Novo Jogo", "Sair"])
    else:
        tela_inicial(["Continuar", "Novo Jogo", "Sair"])