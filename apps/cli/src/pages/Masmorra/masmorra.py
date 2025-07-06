import random
import re
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

def mostrar_minimapa(matriz, pos_jogador=(7, 7), nickname=None, vida_jogador=None):
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
    dadosJogador = ObterDadosJogador(nickname)
    print(f"{Fore.LIGHTBLUE_EX}  HP: {Fore.YELLOW}{vida_jogador} {Fore.LIGHTWHITE_EX}/{dadosJogador[1]}")
    print(f"{Fore.LIGHTBLUE_EX}  Ouro: {Fore.YELLOW}{dadosJogador[3]}\n")

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

    (monstro_id, monstro_nome, monstro_vida, monstro_nivel, chance_critico, dado_ataque, multiplicador, multiplicador_critico) = random.choice(lista_monstros)

    return {
        "id": monstro_id,
        "nome": monstro_nome,
        "vidaMaxima": monstro_vida,
        "nivel": monstro_nivel,
        "chanceCritico": chance_critico,
        "dadoAtaque": dado_ataque,
        "multiplicador": multiplicador,
        "multiplicadorCritico": multiplicador_critico
    }


def verificar_inimigo(seed_sala, sala):
    if sala["visitado"]:
        return False #se a sala ja foi visitada, nao ha inimigos

    digitos = ''.join(filter(str.isdigit, seed_sala))

    if not digitos:
        return False
    
    hash_val = hashlib.sha256(seed_sala.encode()).hexdigest()
    num = int(hash_val[:8], 16) % 100 

    return num < 80  #chance de inimigo

def calcular_dano(arma):
    chance_critico = arma["chanceCritico"]
    dado_ataque_str = arma["dadoAtaque"]
    multiplicador = arma["multiplicador"]  
    multiplicador_critico = arma["multiplicadorCritico"]

    #extrair numero do dado
    match = re.match(r'd(\d+)', dado_ataque_str.lower())
    if not match:
        print("Erro: formato de dado inválido.")
        return 0
    dado_ataque = int(match.group(1))

    # Sorteio se é crítico
    chance = random.randint(1, 100)
    critico = chance <= chance_critico

    resultado_dado = random.randint(1, dado_ataque)

    print(f"  Você rolou um d{dado_ataque} e tirou: {resultado_dado}")

    if critico:
        dano = int(resultado_dado * multiplicador_critico)
        print(Fore.RED + f"  !! CRÍTICO! Dano(x{multiplicador_critico}): {dano}")
    else:
        dano = int(resultado_dado * multiplicador)
        print(f"  Dano: {dano}")

    return dano

def calcular_dano_monstro(monstro):
    dado_ataque_str = monstro.get("dadoAtaque", "")

    if not dado_ataque_str:
        print("Erro: dado de ataque do monstro está vazio.")
        return 0
    
    chance_critico = monstro.get("chanceCritico", 0)
    multiplicador = monstro.get("multiplicador", 1)
    multiplicador_critico = monstro.get("multiplicadorCritico", 2)

    match = re.match(r'(\d*)d(\d+)', dado_ataque_str.lower())
    if not match:
        print("Erro: formato de dado do monstro inválido.")
        return 0
    
    qtd_dados = int(match.group(1)) if match.group(1) else 1
    dado_ataque = int(match.group(2))

    chance = random.randint(1, 100)
    critico = chance <= chance_critico

    resultados = [random.randint(1, dado_ataque) for _ in range(qtd_dados)]
    resultado_total = sum(resultados)
    resultados_str = ' e '.join(map(str, resultados))
    print(f"  O {monstro['nome']} rolou {qtd_dados}d{dado_ataque} e tirou: {resultados_str}")

    if critico:
        dano = int(resultado_total * multiplicador_critico)
        print(Fore.RED + f"  O {monstro['nome']} acertou um CRÍTICO! Dano: {dano}")
    else:
        dano = int(resultado_total * multiplicador)
        print(f"  O {monstro['nome']} atacou! Dano: {dano}")

    return dano

def calcular_defesa(armadura):
    if not armadura:
        return 0
    
    dado_defesa_str = armadura["dadoDefesa"]
    critico_defensivo = armadura["criticoDefensivo"]
    defesa_passiva = armadura["defesaPassiva"]
    bonus_defesa = armadura["bonusDefesa"]

    match = re.match(r'd(\d+)', dado_defesa_str.lower())
    if not match:
        print("Erro: formato de dado de defesa inválido.")
        return 0
    dado_defesa = int(match.group(1))

    chance = random.randint(1, 100)
    critico = chance <= critico_defensivo

    resultado_dado = random.randint(1, dado_defesa)
    print(f"  Você rolou um d{dado_defesa} para defesa e tirou: {resultado_dado}")

    if critico:
        defesa_total = resultado_dado + defesa_passiva + bonus_defesa
        print(Fore.GREEN + f"  Defesa EFICIENTE! Defesa total: {defesa_total}")
    else:
        defesa_total = resultado_dado + defesa_passiva
        print(Fore.LIGHTBLUE_EX + f"  Defesa: {defesa_total}")

    return defesa_total

def menu_batalha(monstro, arma, armadura, vida_jogador, nickname):
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

        dadosJogador = ObterDadosJogador(nickname)
        print(f"{Fore.LIGHTBLUE_EX}  HP: {Fore.YELLOW}{vida_jogador} {Fore.LIGHTWHITE_EX}/{dadosJogador[1]}")
        print(f"{Fore.LIGHTBLUE_EX}  Ouro: {Fore.YELLOW}{dadosJogador[3]}\n")

        print(f"{Fore.RED + Style.BRIGHT}  Você encontrou um {monstro['nome']}!")
        print(f"{Fore.RED}  Vida: {monstro['vidaMaxima']} HP")
        print(f"{Fore.RED}  Nivel: {monstro['nivel']}\n")

        print(f"\n{Fore.LIGHTYELLOW_EX}  O que deseja fazer?\n")
        print(f"{Fore.GREEN}  1- Batalhar")
        print(f"{Fore.CYAN}  2- Usar item")
        print(f"{Fore.MAGENTA}  3- Fugir")

        escolha = input(f"{Fore.LIGHTWHITE_EX}\n>>> ").strip()

        #comandos da batalha
        if escolha == '1':
            print("  Você ataca o monstro!")
            time.sleep(1.5)
            dano = calcular_dano(arma)
            time.sleep(1.5)
            monstro["vidaMaxima"] -= dano

            if monstro["vidaMaxima"] <= 0:
                print(f"  {monstro['nome']} derrotado!")
                trocar_musica(musica_atual_anterior)
                time.sleep(2)
                return "batalhar", vida_jogador
            else:
                time.sleep(1.5)
                dano_monstro = calcular_dano_monstro(monstro)
                time.sleep(1.5)
                defesa_total = calcular_defesa(armadura) if armadura else 0
                time.sleep(1.5)
                dano_final = max(dano_monstro - defesa_total, 0)

                print(Fore.RED + f"  Dano final recebido: {dano_final}")
                vida_jogador -= dano_final
                atualizar_vida_jogador(nickname, vida_jogador)
                time.sleep(1.5)

                if vida_jogador <= 0:
                    print(Fore.RED + "  Você foi derrotado! Alguém te socorreu e te levou novamente para a cidade...")
                    time.sleep(3)
                    musicCity()
                    return "morte", vida_jogador
                
                time.sleep(2)
        
        elif escolha == '2':
            print(Fore.CYAN + "  Você abre sua mochila para usar um item.")
            return "usar_item", vida_jogador
        
        elif escolha == '3':
            print(Fore.MAGENTA + "  Você joga um dado de 20 lados para fugir da batalha...")
            time.sleep(2)
            chance_fuga = random.randint(1, 20)
            if (chance_fuga < 18):
                print(Fore.MAGENTA + f"  Dado: {chance_fuga} - Você não conseguiu fugir.")
                time.sleep(1)

                #monstro ataca após falha na fuga
                print(Fore.RED + f"  O {monstro['nome']} aproveita e ataca!")
                time.sleep(1.5)

                dano_monstro = calcular_dano_monstro(monstro)
                time.sleep(1.5)
                defesa_total = calcular_defesa(armadura) if armadura else 0
                time.sleep(1)

                dano_final = max(dano_monstro - defesa_total, 0)
                print(Fore.RED + f"  Dano final recebido: {dano_final}")
                vida_jogador -= dano_final
                atualizar_vida_jogador(nickname, vida_jogador)
                time.sleep(1.5)

                if vida_jogador <= 0:
                    print(Fore.RED + "  Você foi derrotado! Alguém te socorreu e te levou novamente para a cidade...")
                    time.sleep(3)
                    trocar_musica(musicCity)
                    return "morte", vida_jogador
            
            #continua a batalha
            else:
                print(Fore.MAGENTA + f"  Dado {chance_fuga} - Você fugiu com segurança")
                time.sleep(1)
                trocar_musica(musica_atual_anterior)
                return "fugir", vida_jogador
        else:
            print(Fore.RED + "  Opção inválida. Escolha 1, 2 ou 3.")
            time.sleep(1)


def explorar_masmorra(matriz, pos_inicial=(7, 7), nickname=None, vida_jogador=None):
    global seedMasmorra

    if vida_jogador is None:
        vida_jogador = obter_vida_jogador(nickname)

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
    dados_arma = obter_arma(nickname)
    dados_armadura = obter_armadura(nickname)

    if not dados_arma:
        # print(Fore.RED + "Você não tem uma arma equipada. Fuja enquanto pode!")
        # time.sleep(2)
        # print(Fore.RED + "Equipe uma arma pelo seu inventário")
        # time.sleep(2)
        # atualizarParaLocalAnterior(dadosJogador)
        # musicCity()
        dados_arma = [("d20", 50, 1.5, 3.0)] #arma e armadura para testes
        armadura = {
            "dadoDefesa": "d1",
            "criticoDefensivo": 0,
            "defesaPassiva": 0,
            "bonusDefesa": 0
        }
    
    if not dados_armadura:
        armadura = None
    
    else:
        armadura = {
        "dadoDefesa": dados_armadura[0],
        "criticoDefensivo": dados_armadura[1],
        "defesaPassiva": dados_armadura[2],
        "bonusDefesa": dados_armadura[3]
    }  # armadura padrão para teste, exemplo simples
    
    arma = {
    "dadoAtaque": dados_arma[0][0],
    "chanceCritico": dados_arma[0][1],
    "multiplicador": dados_arma[0][2],
    "multiplicadorCritico": dados_arma[0][3]
}

    while True:
        limpar_terminal()
        mostrar_minimapa(matriz, pos, nickname=nickname, vida_jogador=vida_jogador)
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

        print(Fore.CYAN + "\n  Movimentos possíveis:")
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
            print("  Saindo da masmorra...")
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
                    acao, vida_jogador = menu_batalha(monstro, arma, armadura, vida_jogador, nickname)

                    if acao == "batalhar":
                        matriz[pos]["visitado"] = True
                        trocar_musica(musica_atual)
                        
                    elif acao == "usar_item":
                        pass
                    elif acao == "fugir":
                        trocar_musica(musica_atual)
                    elif acao == "morte":
                        matriz[pos]["visitado"] = True
                        atualizar_vida_jogador(nickname, 0)
                        atualizarParaLocalAnterior(ObterDadosJogador(nickname))
                        return

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
    vida_jogador = dadosJogador[2]
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
                explorar_masmorra(matriz, pos_inicial=(12,12), nickname=nickname, vida_jogador=vida_jogador)
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