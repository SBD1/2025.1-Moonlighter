import random
from colorama import Fore, Back, Style, init
from pages.Masmorra.db_masmorra import *
import pygame
import pyfiglet
import os
import sys
import shutil
import time
from utils.geracaoProceduralMasmorra import gerarMasmorra
import traceback

if sys.platform.startswith('win'):
    import msvcrt
else:
    try:
        import getch
    except ImportError:
        getch = None

# definição da largura da janela do terminal:
musica_atual = None
largura_terminal = shutil.get_terminal_size().columns

# definição da Logo do Jogo centralizada:
ascii = pyfiglet.figlet_format("MOONLIGHTER")
centralizacao = "\n".join([linha.center(largura_terminal) for linha in ascii.splitlines()])
logo = f"{Style.BRIGHT + Fore.LIGHTGREEN_EX}\n\n{centralizacao}\n\n\n"

# definicoes e funcoes iniciais
def trocar_musica(caminho_musica, fadeout_ms=1000, fadein_ms=3000):
    global musica_atual
    pygame.mixer.init()
    pygame.mixer.music.fadeout(fadeout_ms)
    time.sleep(fadeout_ms / 1000)  
    pygame.mixer.music.load(caminho_musica)
    pygame.mixer.music.play(-1, fade_ms=fadein_ms)

    musica_atual = caminho_musica

def musicCity(): #musica da cidade
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_02_Cidade.mp3")

def musicMasmorraEntrance():
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_06_SentientStone.mp3")

def musicbattle():
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_22_Battle.mp3")

def musicMasmorraGolem(): #musica da masmorra do golem
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_07_MasmorraGolem.mp3")

def musicGolemKing(): #musica da chefe da masmorra do golem
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_08_GolemKing.mp3")

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def enter_continue():
    input(Fore.LIGHTBLACK_EX + "\nPressione Enter para continuar...")

def construir_matriz_masmorra(salas):
    matriz = {}

    for x, y, conexoes, tipoSala, seedSala in salas:
        matriz[(x, y)] = {
            "conexoes": conexoes,
            "tipo": tipoSala,
            "visitado": False,
            "descoberto": False,
            "seedSala": seedSala
        }

    return matriz

def mostrar_minimapa(matriz, pos_jogador=(7, 7)):
    if not matriz:
        print("Nenhuma sala para mostrar.")
        return

    try:
        xs = [coord[0] for coord in matriz.keys()]
        ys = [coord[1] for coord in matriz.keys()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
    except ValueError as e:
        print(Fore.RED + "Não foi possível determinar os limites:", e)
        return
    
    print(f"{Style.BRIGHT}{Fore.YELLOW}════════════════════════════════════════════════════".center(largura_terminal))
    print(f"{Style.BRIGHT}{Fore.YELLOW}{dadosMasmorra[0]}".center(largura_terminal))
    print(f"{Style.BRIGHT}{Fore.YELLOW}════════════════════════════════════════════════════".center(largura_terminal))
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Seed: {seedMasmorra}".center(largura_terminal))
    print("\n")

    for x in range(min_x, max_x + 1):
        linha = ""
        for y in range(min_y, max_y + 1):
            pos = (x, y)
            sala = matriz.get(pos)

            if not sala or not sala.get("descoberto"):
                linha += "   "
                continue

            if pos == pos_jogador:
                linha += f"{Fore.YELLOW}{Style.BRIGHT} P {Style.RESET_ALL}"
            elif sala["visitado"] and sala["tipo"] != "Boss":
                linha += f"{Fore.WHITE} ■ {Style.RESET_ALL}"
            elif sala["tipo"] == "Boss":
                linha += f"{Fore.RED} B {Style.RESET_ALL}"

            else:
                linha += f"{Fore.LIGHTBLACK_EX} ■ {Style.RESET_ALL}"
        print(linha)

def sortear_monstro(seed_sala, lista_monstros):
    digitos = ''.join(filter(str.isdigit, seed_sala))
    if not digitos:
        digitos = '1'

    seed = int(digitos)
    random.seed(seed)

    monstro_id, monstro_nome = random.choice(lista_monstros)
    return {"id": monstro_id, "nome": monstro_nome}


def verificar_inimigo(seed_sala, sala):
    if sala["visitado"]:
        return False #se a sala ja foi visitada, nao ha inimigos

    digitos = ''.join(filter(str.isdigit, seed_sala))

    if not digitos:
        return False
    
    hash_val = hashlib.sha256(seed_sala.encode()).hexdigest()
    num = int(hash_val[:8], 16) % 100 

    return num < 80  #chance de inimigo

def menu_batalha(monstro):
    global musica_atual
    musica_atual_anterior = musica_atual
    musicbattle()

    while True:
        limpar_terminal()

        print(f"{Style.BRIGHT}{Fore.YELLOW}════════════════════════════════════════════════════".center(largura_terminal))
        print(f"{Style.BRIGHT}{Fore.YELLOW}{dadosMasmorra[0]}".center(largura_terminal))
        print(f"{Style.BRIGHT}{Fore.YELLOW}════════════════════════════════════════════════════".center(largura_terminal))
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Seed: {seedMasmorra}".center(largura_terminal))
        print("\n")

        print(f"{Fore.RED + Style.BRIGHT}Você encontrou um {monstro}!")
        print(f"\n{Fore.LIGHTYELLOW_EX}O que deseja fazer?\n")
        print(f"{Fore.GREEN}1- Batalhar")
        print(f"{Fore.CYAN}2- Usar item")
        print(f"{Fore.MAGENTA}3- Fugir")

        escolha = input(f"{Fore.LIGHTWHITE_EX}\n>>> ").strip()

        #comandos da batalha
        if escolha == '1':
            print(Fore.GREEN + "Você se prepara para a batalha!")
            trocar_musica(musica_atual_anterior)
            return "batalhar"
        
        elif escolha == '2':
            print(Fore.CYAN + "Você abre sua mochila para usar um item.")
            return "usar_item"
        
        elif escolha == '3':
            print(Fore.MAGENTA + "Você joga um dado de 20 lados para fugir da batalha...")
            time.sleep(2)
            chance_fuga = random.randint(1, 20)
            if (chance_fuga < 18):
                print(Fore.MAGENTA + f"Dado: {chance_fuga} - Você não conseguiu fugir.")
                time.sleep(1)
                
            else:
                print(Fore.MAGENTA + f"Dado {chance_fuga} - Você fugiu com segurança")
                time.sleep(1)
                trocar_musica(musica_atual_anterior)
                return "fugir"
        else:
            print(Fore.RED + "Opção inválida. Escolha 1, 2 ou 3.")
            time.sleep(1)


def explorar_masmorra(matriz, pos_inicial=(7, 7), nickname=None):
    global seedMasmorra

    def revelar_salvas_conectadas(matriz, pos):
        sala = matriz.get(pos)
        if not sala:
            return

        sala["descoberto"] = True
        direcoes = sala["conexoes"]

        dx_dy = {
            'N': (-1, 0),
            'S': (1, 0),
            'L': (0, 1),
            'O': (0, -1)
        }

        for direcao in direcoes:
            dx, dy = dx_dy[direcao]
            vizinha = (pos[0] + dx, pos[1] + dy)
            if vizinha in matriz:
                matriz[vizinha]["descoberto"] = True

    def ler_tecla():
        if sys.platform.startswith('win'):
            # Windows
            tecla = msvcrt.getch()
            # Teclas especiais retornam prefixo 224, ignora
            if tecla in b'\x00\xe0':
                msvcrt.getch()
                return ''
            return tecla.decode('utf-8').lower()
        else:
            # Linux/macOS
            if getch:
                tecla = getch.getch()
                return tecla.lower()
            else:
                # fallback: input normal (com Enter)
                return input("\nDigite uma direção ou 'q' para sair: ").lower()

    pos = pos_inicial
    matriz[pos]["descoberto"] = True
    matriz[pos]["visitado"] = True
    revelar_salvas_conectadas(matriz, pos)
    lista_monstros = obter_monstros()

    while True:
        limpar_terminal()
        mostrar_minimapa(matriz, pos)
        sala_atual = matriz.get(pos)

        if not sala_atual:
            print("Você está em uma sala inválida.")
            break

        opcoes = {}
        if 'N' in sala_atual["conexoes"]:
            opcoes['w'] = (pos[0] - 1, pos[1])
        if 'S' in sala_atual["conexoes"]:
            opcoes['s'] = (pos[0] + 1, pos[1])
        if 'L' in sala_atual["conexoes"]:
            opcoes['d'] = (pos[0], pos[1] + 1)
        if 'O' in sala_atual["conexoes"]:
            opcoes['a'] = (pos[0], pos[1] - 1)

        print(Fore.CYAN + "\nMovimentos possíveis:")
        for tecla in opcoes:
            direcao = {
                'w': "↑ Cima",
                's': "↓ Baixo",
                'a': "← Esquerda",
                'd': "→ Direita"
            }[tecla]
            print(Fore.YELLOW + f"  {tecla.upper()} - {direcao}")
        print("\n" + Fore.RED + "  Q - sair")

        comando = ler_tecla()

        if comando == 'q':
            print("Saindo da masmorra...")
            break
        elif comando in opcoes:
            nova_pos = opcoes[comando]
            if nova_pos in matriz:
                pos = nova_pos
                sala_atual = matriz[pos]
                revelar_salvas_conectadas(matriz, pos)
                atualiza_posicao_jogador(nickname, pos[0], pos[1])

                #verifica se tem inimigo na sala
                seed_sala = matriz[pos].get("seedSala")

                if verificar_inimigo(seed_sala, sala_atual):
                    monstro = sortear_monstro(seed_sala, lista_monstros)
                    acao = menu_batalha(monstro['nome'])

                    if acao == "batalhar":
                        matriz[pos]["visitado"] = True
                        trocar_musica(musica_atual)
                        
                    elif acao == "usar_item":
                        pass
                    elif acao == "fugir":
                        trocar_musica(musica_atual)

                    time.sleep(2)

                else:
                    print(Fore.GREEN + "A sala esta vazia...")
                    matriz[pos]["visitado"] = True
                    time.sleep(1)

            else:
                print("Movimento inválido. Nenhuma sala nessa direção.")
                time.sleep(1)
        else:
            print("Comando inválido.")
            time.sleep(1)

def mainMasmorra(nickname):
    global seedMasmorra, dadosMasmorra, dadosMundo

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

            try:
                salas = carregar_salas(seedMasmorra)
                matriz = construir_matriz_masmorra(salas)
                explorar_masmorra(matriz, pos_inicial=(12,12), nickname=nickname)
            except Exception as e:
                print("ERRO")
                traceback.print_exc()
                input("Pressione enter para continuar...")

            # pygame.mixer.music.fadeout(7000)
            # time.sleep(7)
            # limpar_terminal()
            # print('\033[?25h', end='', flush=True)
        else:
            limpar_terminal()
            print('\033[?25l', end='', flush=True)
            print(logo)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT}{Fore.RED}Opção inválida. Por favor, digite 's' ou 'n'.".center(largura_terminal))
            time.sleep(2)
            print('\033[?25h', end='', flush=True)
            continue