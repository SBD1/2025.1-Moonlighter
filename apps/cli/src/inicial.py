from setup.database import connect_to_db
from pages.IniciarJogo.iniciarJogo import iniciar_jogo
from utils.limparTerminal import limpar_terminal
from utils.geradorSeed import gerarSeed
from pages.Tutorial.tutorial import exibirHistoria
from colorama import Fore, Style, init
import time
import shutil
import pygame
import pyfiglet
import os
from pages.Estabelecimento.db_estabelecimento import (
    criar_instancia_banco_por_jogador,
    criar_instancia_chapeu_de_madeira_por_jogador,
    criar_instancia_forja_por_jogador
)
from pages.IniciarJogo.db_iniciarJogo import (
    buscar_nome_jogador,
    selecionar_jogador
)

# definicoes e funcoes iniciais
init(autoreset=True) #terminal colorido

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

# definição da Logo do Jogo centralizada:
ascii = pyfiglet.figlet_format("MOONLIGHTER")
centralizacao = "\n".join([linha.center(largura_terminal) for linha in ascii.splitlines()])
logo = f"{Style.BRIGHT + Fore.LIGHTGREEN_EX}\n\n{centralizacao}\n\n\n"

def introducao():
    limpar_terminal()
    time.sleep(2)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Desenvolvido durante o curso de".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}Sistema de Banco de Dados 1 - UnB".center(largura_terminal))
    time.sleep(2)
    limpar_terminal()
    print("\n\n\n\n\n\n\n\n\n\n\n")
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}Desenvolvedores:".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}Arthur Evangelista".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}Daniel Rodrigues".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}Igor de Sousa".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}João Paulo".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}Yan Matheus".center(largura_terminal))
    time.sleep(2)
    limpar_terminal()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Jogo inspirado em Moonlighter, por Digital Sun Games".center(largura_terminal))
    time.sleep(3)
    limpar_terminal()
    print("\n\n\n\n\n\n\n\n\n")
    print(logo)
    time.sleep(3)
    return

def buscaTodosJogadores():
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

def buscarJogador(nomeJogador):
    connection = connect_to_db()
    if connection is None:
        print(Fore.RED + "Erro ao conectar ao banco de dados.")
        return None

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM jogador WHERE \"nickname\" = %s;", (nomeJogador,))
    jogador = cursor.fetchone()
    cursor.close()
    connection.close()

    return jogador

def sairDoJogo():
    limpar_terminal()
    print("\n\n\n\n")
    print(logo)

    # COMANDO PARA ESCONDER O CURSOR:
    print('\033[?25l', end='', flush=True)

    print("\n\n\n\n\n")
    print(Fore.RED + Style.BRIGHT + "Saindo do jogo...".center(largura_terminal))
    time.sleep(2)
    exit()

def novoJogador():
    limpar_terminal()
    print("\n\n\n\n")
    print(logo)

    print(f"{Style.BRIGHT}{Fore.YELLOW}Criação de Jogador".center(largura_terminal))

    print("\n\n\n\n\n\n\n\n\n")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Insira o nome do novo jogador:")
    nickname = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ")

    if len(nickname) >= 60:
        limpar_terminal()
        print("\n\n\n\n")
        print(logo)
        print("\n\n\n\n\n")
        print(f"{Style.BRIGHT}{Fore.RED}O NOME DEVE TER MENOS DE 60 CARACTERES.".center(largura_terminal))
        time.sleep(2)
        return novoJogador()

    if len(nickname) == 0:
        limpar_terminal()
        print("\n\n\n\n")
        print(logo)
        print("\n\n\n\n\n")
        print(f"{Style.BRIGHT}{Fore.RED}O NOME NÃO PODE SER VAZIO.".center(largura_terminal))
        time.sleep(2)
        return novoJogador()

    confirmacao = ""

    while confirmacao != "s" and confirmacao != "S" and confirmacao != "n" and confirmacao != "N":
        limpar_terminal()
        print("\n\n\n\n")
        print(logo)

        print(f"{Style.BRIGHT}{Fore.YELLOW}Este será o seu nome?".center(largura_terminal))
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}{nickname}".center(largura_terminal))
        print("\n")
        print(f"{Fore.WHITE}Digite 's' para confirmar ou 'n' para escolher outro nome.".center(largura_terminal))

        print("\n\n\n\n\n\n")
        confirmacao = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip().lower()

        if confirmacao == 's' or confirmacao == 'S':
            limpar_terminal()
            print("\n\n\n\n")
            print(logo)
            print("\n\n\n")

            # COMANDO PARA ESCONDER O CURSOR:
            print('\033[?25l', end='', flush=True)

            print(f"{Style.BRIGHT}{Fore.YELLOW}CRIANDO SEU JOGADOR...".center(largura_terminal))
            time.sleep(2)

            try:
                connection = connect_to_db()
                if connection is None:
                    print(Fore.RED + "Erro ao conectar ao banco de dados.")
                    return
                
                seed = gerarSeed()
                cursor = connection.cursor()
                
                # Criar jogador e mundo
                cursor.execute("INSERT INTO jogador VALUES (%s, 100, 100, 0, 0, 0, 'Vila Rynoka', NULL);", (nickname,))
                cursor.execute("INSERT INTO inst_inventario VALUES (1, %s, 0), (2, %s, 0), (3, %s, 0), (4, %s, 0), (5, %s, 0), (6, %s, 0), (7, %s, 0);", tuple([nickname]*7))
                cursor.execute("INSERT INTO mundo VALUES (%s, %s, 'Manhã', 1, 1);", (seed, nickname,))
                cursor.execute("INSERT INTO \"loja_jogador\" VALUES (%s, 'Moonlighter', 1, 10, 0)", (seed,))
                
                # Fazer commit das inserções principais
                connection.commit()
                
                # Criar instâncias dos estabelecimentos para o novo jogador
                sucesso_banco = criar_instancia_banco_por_jogador(nickname, "Banco de Rynoka", 1, 0)
                if not sucesso_banco:
                    print(f"{Fore.YELLOW}Aviso: Não foi possível criar instância do banco para {nickname}")
                
                sucesso_varejo = criar_instancia_chapeu_de_madeira_por_jogador(nickname, "O Chapéu de Madeira", 2, 15)
                if not sucesso_varejo:
                    print(f"{Fore.YELLOW}Aviso: Não foi possível criar instância do Chapéu de Madeira para {nickname}")
                
                sucesso_forja = criar_instancia_forja_por_jogador(nickname, "Forja de Vulcan", 3)
                if not sucesso_forja:
                    print(f"{Fore.YELLOW}Aviso: Não foi possível criar instância da forja para {nickname}")
                
                cursor.close()
                connection.close()
                
                limpar_terminal()
                print("\n\n\n\n")
                print(logo)
                print("\n\n\n")
                print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}JOGADOR CRIADO COM SUCESSO!".center(largura_terminal))
                pygame.mixer.music.fadeout(7000)
                time.sleep(2)
                limpar_terminal()
                print("\n\n\n\n\n\n\n\n\n")
                print(logo)
                time.sleep(5)
                print('\033[?25h', end='', flush=True)
                return exibirHistoria(buscarJogador(nickname))
            except:
                limpar_terminal()
                print("\n\n\n\n")
                print(logo)
                print("\n\n\n")
                print("Erro ao se conectar com o banco de dados\n")
                time.sleep(2)
                print('\033[?25h', end='', flush=True)
                return novoJogador()
        elif confirmacao == 'n' or confirmacao == 'N':
            return novoJogador()
        else:
            limpar_terminal()
            print("\n\n\n\n")
            print(logo)
            print("\n\n\n")
            print(f"{Style.BRIGHT}{Fore.RED}Opção inválida. Tente novamente.".center(largura_terminal))
            time.sleep(2)
            limpar_terminal()

def musicTheme():
    pygame.mixer.init() #musica
    pygame.mixer.music.load("apps/cli/assets/musics/MoonlighterOST_01_TitleScreen.mp3")
    pygame.mixer.music.play(-1, fade_ms=7000)

def enter_continue():
    input(Fore.LIGHTBLACK_EX + "\nPressione Enter para continuar...")

#funcao principal
def tela_inicial(opcoes):
    while True:
        print('\033[?25l', end='', flush=True)
        musicTheme()
        limpar_terminal()
        introducao()
        limpar_terminal()
        print('\033[?25h', end='', flush=True)

        print("\n\n\n\n")
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

        if len(jogadores) == 0:
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
    jogadores = buscaTodosJogadores()

    if len(jogadores) == 0:
        tela_inicial(["Novo Jogo", "Sair"])
    else:
        tela_inicial(["Continuar", "Novo Jogo", "Sair"])