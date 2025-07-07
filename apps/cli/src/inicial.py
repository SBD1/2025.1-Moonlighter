from setup.database import connect_to_db
from pages.IniciarJogo.iniciarJogo import iniciar_jogo
from pages.IniciarJogo.inventario_funcoes import inicializar_dados_inventario, criar_inventarios_jogador
from utils.limparTerminal import limpar_terminal
from utils.enterContinue import enter_continue
from utils.geradorSeed import gerarSeed
from pages.Tutorial.tutorial import exibirHistoria
from colorama import Fore, Style, init
import time
import shutil
import pygame
import pyfiglet
import os
from zoneinfo import ZoneInfo
from pages.Estabelecimento.db_estabelecimento import (
    criar_instancia_banco_por_jogador,
    criar_instancia_chapeu_de_madeira_por_jogador,
    criar_instancia_forja_por_jogador
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
    print("\n\n\n\n\n\n\n\n\n\n")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Desenvolvido durante o curso de".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}Sistema de Banco de Dados 1 - UnB".center(largura_terminal))
    time.sleep(2)
    limpar_terminal()
    print("\n\n\n\n\n\n\n")
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}Desenvolvedores:".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}Arthur Evangelista".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}Daniel Rodrigues".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}Igor de Sousa".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}João Paulo".center(largura_terminal))
    print(f"{Fore.YELLOW}{Style.BRIGHT}Yan Matheus".center(largura_terminal))
    time.sleep(2)
    limpar_terminal()
    print("\n\n\n\n\n\n\n\n\n\n")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Jogo inspirado em Moonlighter, por Digital Sun Games".center(largura_terminal))
    time.sleep(3)
    limpar_terminal()
    print("\n\n\n\n\n\n")
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
    jogadores = cursor.fetchall()
    cursor.close()
    connection.close()

    return jogadores

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
    print(logo)

    print(f"{Style.BRIGHT}{Fore.YELLOW}Criação de Jogador".center(largura_terminal))
    print(f"{Style.BRIGHT}{Fore.RED}>> DIGITE '0' PARA VOLTAR <<".center(largura_terminal))


    print("\n\n\n\n\n\n\n")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Insira o nome do novo jogador:")
    nickname = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ")

    if nickname == '0':
        return

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
        print(logo)

        print(f"{Style.BRIGHT}{Fore.YELLOW}Este será o seu nome?".center(largura_terminal))
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}{nickname}".center(largura_terminal))
        print("\n")
        print(f"{Fore.WHITE}Digite 's' para confirmar ou 'n' para escolher outro nome.".center(largura_terminal))

        print("\n\n\n\n\n")
        confirmacao = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip().lower()

        if confirmacao == 's' or confirmacao == 'S':
            limpar_terminal()
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
                    print('\033[?25h', end='', flush=True)
                    time.sleep(3)
                    return
                
                limpar_terminal()
                print(logo)
                print("\n\n\n")
                print(f"{Style.BRIGHT}{Fore.YELLOW}CRIANDO MUNDO...".center(largura_terminal))
                time.sleep(2)
                seed = gerarSeed()
                cursor = connection.cursor()
                
                # Criar jogador
                cursor.execute("INSERT INTO jogador VALUES (%s, 100, 100, 100, -1, -1, 'Vila Rynoka', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);", (nickname,))
                # Criar mundo e loja
                cursor.execute("INSERT INTO mundo VALUES (%s, %s, 'Manhã', 1, 1);", (seed, nickname,))
                cursor.execute("INSERT INTO loja_jogador VALUES (%s, 'Moonlighter', 1, 10, 0)", (seed,))
                
                # Fazer commit das inserções principais
                connection.commit()
                
                # Criar instâncias dos estabelecimentos para o novo jogador
                sucesso_banco = criar_instancia_banco_por_jogador(nickname, "Banco de Rynoka", 1, 0)
                if not sucesso_banco:
                    print(f"{Fore.YELLOW}Aviso: Não foi possível criar instância do banco para {nickname}".center(largura_terminal))
                    time.sleep(2)
                
                sucesso_varejo = criar_instancia_chapeu_de_madeira_por_jogador(nickname, "O Chapéu de Madeira", 2, 15)
                if not sucesso_varejo:
                    print(f"{Fore.YELLOW}Aviso: Não foi possível criar instância do Chapéu de Madeira para {nickname}".center(largura_terminal))
                    time.sleep(2)

                sucesso_forja = criar_instancia_forja_por_jogador(nickname, "Forja de Vulcan", 3)
                if not sucesso_forja:
                    print(f"{Fore.YELLOW}Aviso: Não foi possível criar instância da forja para {nickname}".center(largura_terminal))
                    time.sleep(2)

                cursor.close()
                connection.close()
                
                limpar_terminal()
                print(logo)
                print("\n\n\n")
                # Criar inventários do jogador
                print(f"{Style.BRIGHT}{Fore.YELLOW}CRIANDO INVENTÁRIOS...".center(largura_terminal))
                time.sleep(2)
                if not criar_inventarios_jogador(nickname):
                    print(f"{Fore.RED}Erro ao criar inventários do jogador.".center(largura_terminal))
                    print('\033[?25h', end='', flush=True)
                    time.sleep(3)
                    return
                
                limpar_terminal()
                print(logo)
                print("\n\n\n")
                # Adicionar itens iniciais
                print(f"{Style.BRIGHT}{Fore.YELLOW}ADICIONANDO ITENS INICIAIS...".center(largura_terminal))
                time.sleep(2)
                connection = connect_to_db()
                cursor = connection.cursor()
                
                # Buscar ID do inventário principal (Mochila Principal)
                cursor.execute("""
                    SELECT "idInventario" 
                    FROM "inventario" 
                    WHERE "nome" = 'Mochila'
                """)

                id_inventario_principal = cursor.fetchone()
                    
                # Buscar IDs dos itens iniciais
                cursor.execute("""
                    SELECT "idItem", "nome" FROM "item" 
                    WHERE "nome" IN ('Espada Curta de Treinamento', 'Armadura de Tecido I', 'Poção de Cura I')
                """)
                itens_iniciais = cursor.fetchall()
                
                # Adicionar cada item inicial
                for id_item, nome_item in itens_iniciais:
                    quantidade = 3 if nome_item == 'Poção de Cura I' else 1

                    cursor.execute("""
                        INSERT INTO "inst_item" ("idItem", "quantidade", "nickname", "idInventario")
                        VALUES (%s, %s, %s, %s)
                    """, (id_item, quantidade, nickname, id_inventario_principal))
                    cursor.execute("""
                        UPDATE "inst_inventario"
                        SET "slotOcupado" = "slotOcupado" + 1
                        WHERE "nickname" = %s AND "idInventario" = 1
                    """, (nickname,))

                connection.commit()
                cursor.close()
                connection.close()
                
            except Exception as e:
                connection.rollback()
                limpar_terminal()
                print("\n\n\n\n")
                print(logo)
                print("\n\n\n")
                print(f"Erro ao criar jogador: {e}\n")
                print('\033[?25h', end='', flush=True)
                time.sleep(70)
                return
            
            limpar_terminal()
            print(logo)
            print("\n\n\n")
            print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}JOGADOR CRIADO COM SUCESSO!".center(largura_terminal))
            pygame.mixer.music.fadeout(7000)
            time.sleep(2)
            limpar_terminal()
            print("\n\n\n\n\n\n\n\n\n\n")
            print(logo)
            time.sleep(5)
            print('\033[?25h', end='', flush=True)
            return exibirHistoria(buscarJogador(nickname))
        elif confirmacao == 'n' or confirmacao == 'N':
            return novoJogador()
        else:
            limpar_terminal()
            print(logo)
            print("\n\n\n")
            print(f"{Style.BRIGHT}{Fore.RED}Opção inválida. Tente novamente.".center(largura_terminal))
            time.sleep(2)
            limpar_terminal()

def continuar_jogo():
    limpar_terminal()
    print(logo)

    print(f"{Style.BRIGHT}{Fore.YELLOW}Jogos Existentes".center(largura_terminal))
    print(f"{Style.BRIGHT}{Fore.RED}>> DIGITE '0' PARA VOLTAR <<".center(largura_terminal))
    print("\n")

    jogadores = buscaTodosJogadores()
    print(f"{Style.BRIGHT}{Fore.YELLOW}═════════════════════════════════════════════════════".center(largura_terminal + 2))
    for i, jogador in enumerate(jogadores):
        nome_jogador = jogador[0]
        ultimoUpdate = jogador[9]
        ourosJogador = jogador[3]
        localizacaoJogador = jogador[6]
        ultimoUpdate = ultimoUpdate.replace(tzinfo=ZoneInfo("UTC"))
        ultimoUpdate_br = ultimoUpdate.astimezone(ZoneInfo("America/Sao_Paulo"))
        data_formatada = ultimoUpdate_br.strftime('%d/%m/%Y às %H:%M:%S')
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}{nome_jogador}".center(largura_terminal))
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Ouros: {Fore.MAGENTA}{ourosJogador}".center(largura_terminal + 3))
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Localização: {Fore.MAGENTA}{localizacaoJogador}".center(largura_terminal + 5))
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Último Salvamento: {Fore.MAGENTA}{data_formatada}".center(largura_terminal + 5))
        print(f"{Style.BRIGHT}{Fore.YELLOW}═════════════════════════[{Fore.LIGHTGREEN_EX}{i+1}{Fore.YELLOW}]═════════════════════════".center(largura_terminal + 12))

    print("\n\n")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Digite o número do jogador que deseja continuar: ")
    escolha = input(f"{Style.BRIGHT}{Fore.MAGENTA}>> ")

    if not escolha.isdigit():
        limpar_terminal()
        print(logo)
        print("\n\n\n")
        print(f"{Style.BRIGHT}{Fore.RED}Por favor, digite um número válido.".center(largura_terminal))
        time.sleep(2)
        return continuar_jogo()
    elif int(escolha) == 0:
        return tela_inicial(False)
    elif 1 <= int(escolha) <= len(jogadores):
        jogador_selecionado = jogadores[int(escolha) - 1]
        
        confirmacao = ""
        while confirmacao != "s" and confirmacao != "S" and confirmacao != "n" and confirmacao != "N":
            limpar_terminal()
            print(logo)
            
            print(f"{Style.BRIGHT}{Fore.YELLOW}Você deseja continuar com o jogador abaixo?".center(largura_terminal))
            print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}{jogador_selecionado[0]}".center(largura_terminal))
            print("\n")
            print(f"{Fore.WHITE}Digite 's' para confirmar ou 'n' para escolher outro nome.".center(largura_terminal))

            print("\n\n\n\n\n")
            confirmacao = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip().lower()

            if confirmacao == 's' or confirmacao == 'S':
                limpar_terminal()
                print(logo)
                print("\n\n\n")

                # COMANDO PARA ESCONDER O CURSOR:
                print('\033[?25l', end='', flush=True)

                print(f"{Style.BRIGHT}{Fore.YELLOW}CARREGANDO JOGO...".center(largura_terminal))
                time.sleep(2)
                pygame.mixer.music.fadeout(7000)
                time.sleep(2)
                limpar_terminal()
                print("\n\n\n\n\n\n\n\n\n\n")
                print(logo)
                time.sleep(5)
                print('\033[?25h', end='', flush=True)
                iniciar_jogo(jogador_selecionado[0])
            elif confirmacao == 'n' or confirmacao == 'N':
                limpar_terminal()
                print(logo)
                return continuar_jogo()
            else:
                limpar_terminal()
                print(logo)
                print("\n\n\n")
                print(f"{Style.BRIGHT}{Fore.RED}Opção inválida. Tente novamente.".center(largura_terminal))
                time.sleep(2)
                limpar_terminal()
    else:
        limpar_terminal()
        print(logo)
        print("\n\n\n")
        print(f"{Style.BRIGHT}{Fore.RED}Opção inválida. Tente novamente.".center(largura_terminal))
        time.sleep(2)
        return continuar_jogo()


def musicTheme():
    pygame.mixer.init() #musica
    pygame.mixer.music.load("apps/cli/assets/musics/MoonlighterOST_01_TitleScreen.mp3")
    pygame.mixer.music.play(-1, fade_ms=7000)

#funcao principal
def tela_inicial(introduction = False):
    while True:
        jogadores = buscaTodosJogadores()
        opcoes = ["Continuar", "Novo Jogo", "Sair"] if len(jogadores) > 0 else ["Novo Jogo", "Sair"]

        musicTheme()

        if introduction:
            print('\033[?25l', end='', flush=True)
            introducao()
        
        limpar_terminal()
        print('\033[?25h', end='', flush=True)

        print(logo)

        for i, opcao in enumerate(opcoes):
            construcaoString = f"{Fore.YELLOW}{Style.BRIGHT}{i + 1}. {opcao}"
            opcao_centralizada = construcaoString.center(largura_terminal)
            print(opcao_centralizada)

        try:
            print("\n\n\n\n\n\n\n" + f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Digite o número da opção desejada:")
            escolha:int = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>> "))
        except ValueError:
            limpar_terminal()
            print(logo)
            print("\n\n\n")
            print(f"{Style.BRIGHT}{Fore.RED}Por favor, digite um número válido.".center(largura_terminal))
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
                    continuar_jogo()
                case 2:
                    novoJogador()
                case 3:
                    sairDoJogo()
                case _:
                    print(Fore.RED + "Opção inválida. Tente novamente.")
                    enter_continue()

# Executa a tela inicial
if __name__ == '__main__':
    tela_inicial(True)