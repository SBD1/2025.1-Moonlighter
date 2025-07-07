import time
import traceback
import pyfiglet
from pages.IniciarJogo.db_iniciarJogo import *
from pages.IniciarJogo.inventario_interface import ver_inventario
from pages.Estabelecimento import menu_chapeu_de_madeira, menu_forja, menu_banco
from utils.limparTerminal import limpar_terminal
from pages.Masmorra.masmorra import mainMasmorra
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


def musicCity():  # musica da cidade
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
    dadosMundo = buscarInfoMundo(nickname)

    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╔════════════════════[ MOONLIGHTER GAME ]════════════════════╗".center(largura_terminal))
    print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}{dadosJogador[0]}".center(largura_terminal))
    print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}HP: {dadosJogador[2]} / {dadosJogador[1]} | OURO: {dadosJogador[3]}".center(largura_terminal))
    print("\n")
    if dadosJogador[4] == -1 or (dadosJogador[4] == 0 and dadosJogador[5] == 0):
        print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}{dadosJogador[6]}".center(largura_terminal))
        print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}DIA: {dadosMundo[3]} | PERÍODO: {dadosMundo[2]}".center(largura_terminal))
    else:
        print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}MASMORRA: {dadosJogador[6]}".center(largura_terminal))
        print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}SALA [X][Y]: [{dadosJogador[4]}][{dadosJogador[5]}]".center(largura_terminal))
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
        if (dadosJogador[6] != 'Vila Rynoka'):
            locais.append(('Voltar ao Local Anterior',))
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
                
                try:
                    if locais[escolha - 1][0].startswith('Masmorra'):
                        mainMasmorra(nickname)
                except Exception as e:
                    print(Fore.RED + "Erro ao executar a masmorra:", e)
                    traceback.print_exc()
                    input("Pressione Enter para continuar...")
                if locais[escolha - 1][0] == 'Forja Vulcânica':
                    menu_forja(nickname, buscarSeedMapa(nickname))
                if locais[escolha - 1][0] == 'Banco de Rynoka':
                    menu_banco(nickname)
                if locais[escolha - 1][0] == 'O Chapéu de Madeira':
                    menu_chapeu_de_madeira(nickname, buscarSeedMapa(nickname))
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
    print(f"{Style.BRIGHT}{Fore.YELLOW}5 - Ver Itens no Chão")
    print(f"{Style.BRIGHT}{Fore.RED}6 - Voltar ao Menu Principal")

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


def ver_status_jogador(nickname):
    """
    Exibe informações detalhadas do status do jogador
    """
    limpar_terminal()
    print(logo)

    dadosJogador = buscar_dadosJogador(nickname)
    if not dadosJogador:
        print(f"{Fore.RED}Erro ao buscar dados do jogador.")
        input(f"{Fore.LIGHTBLACK_EX}\nPressione Enter para continuar...")
        return

    # Buscar equipamentos
    equipamentos = obter_equipamentos_jogador(nickname)

    # Buscar informações do mundo
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT "seedMundo", "periodo", "dia", "nivelMundo"
            FROM "mundo" 
            WHERE "nickname" = %s
        """, (nickname,))
        mundo_info = cursor.fetchone()
        cursor.close()
        connection.close()
    else:
        mundo_info = None

    print(f"{Style.BRIGHT}{Fore.YELLOW}{'═' * largura_terminal}")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}STATUS DO JOGADOR: {nickname.upper()}".center(largura_terminal))
    print(f"{Style.BRIGHT}{Fore.YELLOW}{'═' * largura_terminal}")

    print(f"\n{Style.BRIGHT}{Fore.LIGHTCYAN_EX}INFORMAÇÕES BÁSICAS:")
    print(f"{Fore.LIGHTBLUE_EX}  Nome: {Fore.YELLOW}{dadosJogador[0]}")
    print(f"{Fore.LIGHTBLUE_EX}  HP Atual: {Fore.YELLOW}{dadosJogador[2]}")
    print(f"{Fore.LIGHTBLUE_EX}  HP Máximo: {Fore.YELLOW}{dadosJogador[1]}")
    print(f"{Fore.LIGHTBLUE_EX}  Ouro: {Fore.YELLOW}{dadosJogador[3]}")
    print(f"{Fore.LIGHTBLUE_EX}  Localização: {Fore.YELLOW}{dadosJogador[6]}")

    if mundo_info:
        print(f"\n{Style.BRIGHT}{Fore.LIGHTCYAN_EX}INFORMAÇÕES DO MUNDO:")
        print(f"{Fore.LIGHTBLUE_EX}  Seed do Mundo: {Fore.YELLOW}{mundo_info[0]}")
        print(f"{Fore.LIGHTBLUE_EX}  Período: {Fore.YELLOW}{mundo_info[1]}")
        print(f"{Fore.LIGHTBLUE_EX}  Dia: {Fore.YELLOW}{mundo_info[2]}")
        print(f"{Fore.LIGHTBLUE_EX}  Nível do Mundo: {Fore.YELLOW}{mundo_info[3]}")

    if equipamentos:
        print(f"\n{Style.BRIGHT}{Fore.LIGHTCYAN_EX}EQUIPAMENTOS:")
        print(f"{Fore.LIGHTBLUE_EX}  Arma Equipada: {Fore.YELLOW}{equipamentos['arma_nome']}")
        print(f"{Fore.LIGHTBLUE_EX}  Armadura Equipada: {Fore.YELLOW}{equipamentos['armadura_nome']}")

    print(f"{Fore.LIGHTBLACK_EX}\nPressione Enter para voltar...")
    input()


def obter_equipamentos_jogador(nickname):
    """
    Função helper para obter equipamentos do jogador
    """
    connection = connect_to_db()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("""
        SELECT I_arma."idItem", I_arma."nome", I_arma."tipo"
        FROM "jogador" J
            JOIN "inst_item" II_arma ON J."nickname" = II_arma."nickname"
            JOIN "item" I_arma ON II_arma."idItem" = I_arma."idItem"
        WHERE J."nickname" = %s AND II_arma."idInventario" = 4
        UNION
        SELECT I_armadura."idItem", I_armadura."nome", I_armadura."tipo"
        FROM "jogador" J
            JOIN "inst_item" II_armadura ON J."nickname" = II_armadura."nickname"
            JOIN "item" I_armadura ON II_armadura."idItem" = I_armadura."idItem"
        WHERE J."nickname" = %s AND II_armadura."idInventario" = 3;
    """, (nickname, nickname,))

    resultado = cursor.fetchall()
    cursor.close()
    connection.close()

    equipamento = {
        'id_arma': None,
        'id_armadura': None,
        'arma_nome': "Nenhum",
        'armadura_nome': "Nenhum"
    }

    if resultado:
        for linha in resultado:
            if linha[2] == 'Arma':
                equipamento['id_arma'] = linha[0]
                equipamento['arma_nome'] = linha[1]
            elif linha[2] == 'Armadura':
                equipamento['id_armadura'] = linha[0]
                equipamento['armadura_nome'] = linha[1]

        return equipamento
    return None


def ver_itens_no_chao(nickname):
    """
    Exibe itens no chão e permite coletar
    """
    while True:
        limpar_terminal()
        print(logo)

        print(f"{Style.BRIGHT}{Fore.YELLOW}{'═' * largura_terminal}")
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}ITENS NO CHÃO".center(largura_terminal))
        print(f"{Style.BRIGHT}{Fore.YELLOW}{'═' * largura_terminal}")

        itens_chao = listar_itens_no_chao(nickname)

        if not itens_chao:
            print(f"\n{Fore.YELLOW}Não há itens no chão neste local.")
            print(f"{Fore.LIGHTBLACK_EX}\nPressione Enter para voltar...")
            input()
            return

        print(f"\n{Style.BRIGHT}{Fore.LIGHTCYAN_EX}ITENS DISPONÍVEIS:")
        print(f"{Style.BRIGHT}{Fore.YELLOW}{'─' * 60}")

        for i, item in enumerate(itens_chao, start=1):
            id_item_chao, id_item, nome, quantidade, pos_x, pos_y, descricao = item
            print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}{i:2d}. {Fore.YELLOW}{nome}")
            print(f"     {Fore.LIGHTBLUE_EX}Quantidade: {Fore.WHITE}{quantidade}")
            print(f"     {Fore.LIGHTBLUE_EX}Posição: {Fore.WHITE}({pos_x}, {pos_y})")
            if descricao:
                desc_limitada = descricao[:50] + "..." if len(descricao) > 50 else descricao
                print(f"     {Fore.LIGHTBLACK_EX}{desc_limitada}")
            print()

        print(f"\n{Style.BRIGHT}{Fore.YELLOW}OPÇÕES:")
        print(f"{Fore.LIGHTGREEN_EX}• Digite o número do item para coletar")
        print(f"{Fore.LIGHTGREEN_EX}• Digite '0' para voltar")

        escolha = input(f"\n{Style.BRIGHT}{Fore.MAGENTA}>> ").strip()

        if escolha == '0':
            return

        try:
            num_item = int(escolha)
            if 1 <= num_item <= len(itens_chao):
                item_selecionado = itens_chao[num_item - 1]
                id_item_chao, id_item, nome, quantidade, pos_x, pos_y, descricao = item_selecionado

                print(f"\n{Style.BRIGHT}{Fore.YELLOW}Coletar: {Fore.LIGHTGREEN_EX}{quantidade}x {nome}?")
                print(f"{Fore.WHITE}Digite 's' para confirmar ou 'n' para cancelar.")
                confirmacao = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip().lower()

                if confirmacao == 's':
                    if coletar_item_do_chao(nickname, id_item_chao):
                        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}✓ {quantidade}x {nome} coletado com sucesso!")
                        time.sleep(2)
                    else:
                        print(f"{Fore.RED}Erro ao coletar item! Verifique se há espaço no inventário.")
                        time.sleep(2)
                else:
                    print(f"{Fore.YELLOW}Ação cancelada.")
                    time.sleep(1)
            else:
                print(f"{Fore.RED}Número de item inválido!")
                time.sleep(1)
        except ValueError:
            print(f"{Fore.RED}Por favor, digite um número válido!")
            time.sleep(1)


def listar_itens_no_chao(nickname):
    """
    Lista os itens disponíveis no chão para o jogador
    """
    connection = connect_to_db()
    if connection is None:
        return []

    cursor = connection.cursor()

    # Buscar informações do jogador para obter seedMundo e nomeLocal
    cursor.execute("""
        SELECT j."nomeLocal", m."seedMundo"
        FROM "jogador" j
        JOIN "mundo" m ON j."nickname" = m."nickname"
        WHERE j."nickname" = %s
    """, (nickname,))

    jogador_info = cursor.fetchone()
    if not jogador_info:
        cursor.close()
        connection.close()
        return []

    nome_local, seed_mundo = jogador_info

    # Buscar itens no chão na localização atual
    cursor.execute("""
        SELECT 
            ic."idItemChao",
            ic."idItem",
            i."nome",
            ic."quantidade",
            ic."posicaoX",
            ic."posicaoY",
            i."descricao"
        FROM "item_chao" ic
        JOIN "item" i ON ic."idItem" = i."idItem"
        WHERE ic."seedMundo" = %s AND ic."nomeLocal" = %s
        ORDER BY ic."tempoDropado" DESC
    """, (seed_mundo, nome_local))

    resultados = cursor.fetchall()
    cursor.close()
    connection.close()

    return resultados


def coletar_item_do_chao(nickname, id_item_chao):
    """
    Coleta um item do chão e adiciona ao inventário do jogador
    """
    from pages.IniciarJogo.db_iniciarJogo import coletar_item_do_chao as coletar_item_db
    return coletar_item_db(nickname, id_item_chao)

# funcao principal


def iniciar_jogo(nickname):
    init(autoreset=True)  # terminal colorido

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
            elif int(escolha) == 3:
                ver_inventario(nickname)
            elif int(escolha) == 4:
                ver_status_jogador(nickname)
            elif int(escolha) == 5:
                ver_itens_no_chao(nickname)
            elif int(escolha) == 6:
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
