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

    if musica_atual == caminho_musica:
        return
    
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

def musicGolemKing(): #musica do chefe da masmorra do golem
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_08_GolemKing.mp3")

def musicMasmorraFloresta(): #musica da masmorra da floresta
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_10_MasmorraFloresta.mp3")

def musicCarnivorousMutae(): #musica do chefe da masmorra da floresta
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_13_CarnivorousMutae.mp3")

def musicMasmorraDeserto(): #musica da masmorra do deserto
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_14_MasmorraDeserto.mp3")

def musicNaja(): #musica do chefe da masmorra do deserto
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_16_Naja.mp3")

def musicMasmorraTecnologia(): #musica da masmorra da tecnologia
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_20_MasmorraTecnologia.mp3")

def musicFluxEnergy(): #musica do chefe da masmorra da tecnologia
    trocar_musica("apps/cli/assets/musics/MoonlighterOST_21_FluxEnergy.mp3")

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

def sortear_monstro(seed_sala, lista_monstros, tipo_sala):
    digitos = ''.join(filter(str.isdigit, seed_sala))
    if not digitos:
        digitos = '1'

    seed = int(digitos)
    random.seed(seed)

    # Filtra a lista de monstros conforme o tipo de sala:
    if tipo_sala == "Boss":
        # Só monstros que são chefes
        monstros_filtrados = [m for m in lista_monstros if m[8] == True]  # índice 9: "chefe"
    else:
        # Só monstros que não são chefes
        monstros_filtrados = [m for m in lista_monstros if m[8] == False]

        if not monstros_filtrados:
            # fallback caso não tenha monstros correspondentes, retorna algum monstro qualquer
            monstros_filtrados = lista_monstros

    (monstro_id, monstro_nome, monstro_vida, monstro_nivel, chance_critico, dado_ataque, multiplicador, multiplicador_critico, chefe) = random.choice(monstros_filtrados)

    return {
        "id": monstro_id,
        "nome": monstro_nome,
        "vidaMaxima": monstro_vida,
        "nivel": monstro_nivel,
        "chanceCritico": chance_critico,
        "dadoAtaque": dado_ataque,
        "multiplicador": multiplicador,
        "multiplicadorCritico": multiplicador_critico,
        "chefe": chefe
    }


def verificar_inimigo(seed_sala, sala):
    if sala["visitado"]:
        return False #se a sala ja foi visitada, nao ha inimigos

    if sala["tipo"] == "Boss":
        return True

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
    match = re.match(r'd(\d+)', str(dado_ataque_str).lower())
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

    match = re.match(r'(\d*)d(\d+)', str(dado_ataque_str).lower())
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
    print(f"  O {monstro['nome']} rolou {qtd_dados} d{dado_ataque} e tirou: {resultados_str}")

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

    match = re.match(r'd(\d+)', str(dado_defesa_str).lower())
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
    if monstro["chefe"]:
        if monstro["nome"] == "Rei Golem":
            musicGolemKing()
        elif monstro["nome"] == "Mutae Carnívora":
            musicCarnivorousMutae()
        elif monstro["nome"] == "Naja":
            musicNaja()
        elif monstro["nome"] == "Fluxo de Energia":
            musicFluxEnergy()
        else:
            musicbattle()  # fallback
    else:
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
                
                # Processa drops do monstro
                drops_obtidos = processar_drops_monstro(monstro["id"])
                if drops_obtidos:
                    print(f"\n{Fore.LIGHTGREEN_EX}  Você encontrou os seguintes itens:")
                    for drop in drops_obtidos:
                        print(f"    {Fore.YELLOW}• {drop['nome']} x{drop['quantidade']}")
                        # Adiciona o item ao inventário
                        adicionar_item_ao_inventario(nickname, drop['id_item'], drop['quantidade'])
                    print(f"{Fore.LIGHTGREEN_EX}  Itens adicionados ao seu inventário!")
                else:
                    print(f"\n{Fore.LIGHTBLACK_EX}  O monstro não dropou nenhum item.")
                
                trocar_musica(musica_atual_anterior)

                # Verifica se é o boss que libera a próxima masmorra
                if monstro["nome"] == "Rei Golem":
                    print("\n" + Fore.GREEN + Style.BRIGHT + "  Parabéns! Você derrotou o Rei Golem e desbloqueou a Masmorra da Floresta!")
                    desbloquear_masmorra(nickname, "Masmorra da Floresta")
                    time.sleep(3)  
                    atualizarParaLocalAnterior(ObterDadosJogador(nickname))
                    print(Fore.LIGHTCYAN_EX + "\n  Você foi transportado de volta para a Vila Rynoka.")
                    musicCity()
                    time.sleep(3)
                    return "sair", vida_jogador
                
                if monstro["nome"] == "Mutae Carnívora":
                    print("\n" + Fore.GREEN + Style.BRIGHT + "  Você se sente mais forte, desbloqueou a Masmorra do Deserto!")
                    desbloquear_masmorra(nickname, "Masmorra do Deserto") 
                    time.sleep(3)
                    atualizarParaLocalAnterior(ObterDadosJogador(nickname))
                    print(Fore.LIGHTCYAN_EX + "\n  Você foi transportado de volta para a Vila Rynoka.")
                    musicCity()
                    time.sleep(3)
                    return "sair", vida_jogador

                if monstro["nome"] == "Golem Mãe":
                    print("\n" + Fore.GREEN + Style.BRIGHT + "  Você visivelmente está mais forte! Desbloqueou a Masmorra da Tecnologia!")
                    desbloquear_masmorra(nickname, "Masmorra da Tecnologia") 
                    time.sleep(3)
                    atualizarParaLocalAnterior(ObterDadosJogador(nickname))
                    print(Fore.LIGHTCYAN_EX + "\n  Você foi transportado de volta para a Vila Rynoka.")
                    musicCity()
                    time.sleep(3)
                    return "sair", vida_jogador

                if monstro["nome"] == "Naja":
                    print("\n" + Fore.GREEN + Style.BRIGHT + "  Você visivelmente está mais forte! Desbloqueou a Masmorra da Tecnologia!")
                    desbloquear_masmorra(nickname, "Masmorra da Tecnologia")
                    time.sleep(3) 
                    atualizarParaLocalAnterior(ObterDadosJogador(nickname))
                    print(Fore.LIGHTCYAN_EX + "\n  Você foi transportado de volta para a Vila Rynoka.")
                    musicCity()
                    time.sleep(3)
                    return "sair", vida_jogador
                
                if monstro["nome"] == "Fluxo de Energia":
                    print("\n" + Fore.GREEN + Style.BRIGHT + "  Parabéns! Você derrotou o Fluxo de Energia e desbloqueou a última masmorra: a Masmorra desconhecida!")
                    desbloquear_masmorra(nickname, "Masmorra Desconhecida")
                    time.sleep(3)
                    atualizarParaLocalAnterior(ObterDadosJogador(nickname))
                    print(Fore.LIGHTCYAN_EX + "\n  Você foi transportado de volta para a Vila Rynoka.")
                    musicCity()
                    time.sleep(3)
                    return "sair", vida_jogador

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
            vida_jogador = usar_pocao_batalha(nickname, vida_jogador)
            if vida_jogador <= 0:
                print(Fore.RED + "  Você foi derrotado! Alguém te socorreu e te levou novamente para a cidade...")
                time.sleep(3)
                musicCity()
                return "morte", vida_jogador
        
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

    musicaLocal = musica_masmorra(nickname)
    if musicaLocal == "Masmorra do Golem":
        musicMasmorraGolem()
    elif musicaLocal == "Masmorra da Floresta":
        musicMasmorraFloresta()
    elif musicaLocal == "Masmorra do Deserto":
        musicMasmorraDeserto()
    elif musicaLocal == "Masmorra da Tecnologia":
        musicMasmorraTecnologia()

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
    lista_monstros = obter_monstros(nickname)
    dados_arma = obter_arma(nickname)
    dados_armadura = obter_armadura(nickname)
    dadosJogador = ObterDadosJogador

    if not dados_arma:
        print(Fore.RED + "Você não tem uma arma equipada. Fuja enquanto pode!")
        time.sleep(2)
        print(Fore.RED + "Equipe uma arma pelo seu inventário")
        time.sleep(2)
        atualizarParaLocalAnterior(dadosJogador)
        musicCity()
        return
    

    if isinstance(dados_arma, list) and len(dados_arma) > 0:
        arma_data = dados_arma[0]
    else:
        arma_data = dados_arma
    
    dado_bruto = str(arma_data[1])
    if not dado_bruto.startswith("d"):
        dado_bruto = f"d{dado_bruto}"

    arma = {
                "dadoAtaque": dado_bruto,
                "chanceCritico": arma_data[2],
                "multiplicador": arma_data[3],
                "multiplicadorCritico": arma_data[4]
            }
            
    if not dados_armadura:
        armadura = None
    
    else:
        dado_def = str(dados_armadura[1])
        if not dado_def.startswith("d"):
            dado_def = f"d{dado_def}"

        armadura = {
        "dadoDefesa": dado_def,
        "criticoDefensivo": dados_armadura[3],
        "defesaPassiva": dados_armadura[2],
        "bonusDefesa": dados_armadura[4]
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
        print("\n" + Fore.RED + "  Q - Sair")

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
                    monstro = sortear_monstro(seed_sala, lista_monstros, sala_atual["tipo"])
                    acao, vida_jogador = menu_batalha(monstro, arma, armadura, vida_jogador, nickname)

                    if acao == "batalhar":
                        matriz[pos]["visitado"] = True
                        trocar_musica(musica_atual)
                        
                    elif acao == "usar_item":
                        vida_jogador = usar_pocao_batalha(nickname, vida_jogador)
                        if vida_jogador <= 0:
                            print(Fore.RED + "  Você foi derrotado! Alguém te socorreu e te levou novamente para a cidade...")
                            time.sleep(3)
                            musicCity()
                            return "morte", vida_jogador
                    elif acao == "fugir":
                        trocar_musica(musica_atual)
                    elif acao == "morte":
                        matriz[pos]["visitado"] = True
                        # Recupera vida máxima
                        dados_jogador = ObterDadosJogador(nickname)
                        if dados_jogador and len(dados_jogador) > 1:
                            vida_maxima = dados_jogador[1]
                        else:
                            vida_maxima = 100  # valor padrão caso haja erro
                        atualizar_vida_jogador(nickname, vida_maxima)
                        atualizarParaLocalAnterior(dados_jogador)
                        print(Fore.LIGHTGREEN_EX + "\nVocê foi socorrido e sua vida foi restaurada!")
                        time.sleep(2)
                        from pages.IniciarJogo.iniciarJogo import iniciar_jogo
                        iniciar_jogo(nickname)
                        return
                    elif acao == "sair":
                        atualizarParaLocalAnterior(ObterDadosJogador(nickname))
                        return

                    time.sleep(2)

                else:
                    print(Fore.GREEN + "\n  A sala esta vazia...")
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

            pygame.mixer.music.fadeout(7000)
            time.sleep(2)
            limpar_terminal()
            print('\033[?25h', end='', flush=True)
            return

        else:
            limpar_terminal()
            print('\033[?25l', end='', flush=True)
            print(logo)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT}{Fore.RED}Opção inválida. Por favor, digite 's' ou 'n'.".center(largura_terminal))
            time.sleep(2)
            print('\033[?25h', end='', flush=True)
            continue

def usar_pocao_batalha(nickname, vida_atual):
    """
    Permite usar poções durante a batalha
    """
    from pages.Masmorra.db_masmorra import ObterDadosJogador
    from setup.database import connect_to_db
    from colorama import Fore, Style
    import time
    
    limpar_terminal()
    print(f"{Style.BRIGHT}{Fore.CYAN}══════════ USAR POÇÃO ══════════")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}JOGADOR: {nickname.upper()}")
    print(f"{Style.BRIGHT}{Fore.YELLOW}═══════════════════════════════")
    
    # Obter dados do jogador
    dados_jogador = ObterDadosJogador(nickname)
    vida_maxima = dados_jogador[1]
    
    print(f"\n{Fore.LIGHTBLUE_EX}HP Atual: {Fore.YELLOW}{vida_atual} {Fore.LIGHTWHITE_EX}/{vida_maxima}")
    
    # Buscar poções no inventário
    connection = connect_to_db()
    if connection is None:
        print(f"{Fore.RED}Erro ao conectar ao banco de dados.")
        return vida_atual
    
    cursor = connection.cursor()
    cursor.execute("""
        SELECT ii."idInstItem", i."idItem", i."nome", ii."quantidade", p."quantidade" as cura
        FROM "inst_item" ii
        JOIN "item" i ON ii."idItem" = i."idItem"
        JOIN "pocao" p ON i."idItem" = p."idItem"
        WHERE ii."nickname" = %s
        ORDER BY p."quantidade" DESC
    """, (nickname,))
    
    pocoes = cursor.fetchall()
    cursor.close()
    connection.close()
    
    if not pocoes:
        print(f"\n{Fore.RED}Você não possui nenhuma poção no inventário!")
        print(f"{Fore.YELLOW}Volte ao menu principal e compre poções primeiro.")
        time.sleep(3)
        return vida_atual
    
    print(f"\n{Style.BRIGHT}{Fore.LIGHTCYAN_EX}POÇÕES DISPONÍVEIS:")
    print(f"{Fore.LIGHTBLUE_EX}{'Nº':<3} {'Nome':<25} {'Cura':<8} {'Qtd':<5}")
    print(f"{Fore.LIGHTBLACK_EX}{'─' * 55}")
    
    pocoes_numeradas = []
    for i, pocao in enumerate(pocoes, 1):
        id_inst, id_item, nome, qtd, cura = pocao
        print(f"{Fore.WHITE}{i:<3} {nome:<25} {cura:<8} {qtd:<5}")
        pocoes_numeradas.append(pocao)
    
    print(f"\n{Style.BRIGHT}{Fore.YELLOW}INSTRUÇÕES:")
    print(f"{Fore.LIGHTGREEN_EX}• Digite o número da poção que deseja usar")
    print(f"{Fore.LIGHTGREEN_EX}• Digite '0' para cancelar")
    
    while True:
        try:
            escolha = input(f"\n{Style.BRIGHT}{Fore.MAGENTA}>> ").strip()
            
            if escolha == '0':
                return vida_atual
            
            num_pocao = int(escolha)
            if 1 <= num_pocao <= len(pocoes_numeradas):
                pocao_selecionada = pocoes_numeradas[num_pocao - 1]
                id_inst, id_item, nome, qtd, cura = pocao_selecionada
                print(f"\n{Fore.LIGHTYELLOW_EX}Você selecionou: {nome} (Cura: {cura}, Quantidade: {qtd})")
                confirm = input(f"{Fore.LIGHTGREEN_EX}Deseja usar esta poção? (s/n): ").strip().lower()
                if confirm != 's':
                    print(f"{Fore.YELLOW}Ação cancelada.")
                    time.sleep(1)
                    return vida_atual
                if vida_atual >= vida_maxima:
                    print(f"{Fore.YELLOW}Sua vida já está cheia! Não é possível usar poção agora.")
                    time.sleep(2)
                    return vida_atual
                # Usar apenas UMA poção
                nova_vida = min(vida_atual + cura, vida_maxima)
                vida_restaurada = nova_vida - vida_atual
                # Atualizar/remover poção do inventário
                connection = connect_to_db()
                cursor = connection.cursor()
                if qtd > 1:
                    cursor.execute("""
                        UPDATE "inst_item" SET "quantidade" = "quantidade" - 1 WHERE "idInstItem" = %s
                    """, (id_inst,))
                else:
                    cursor.execute("""
                        DELETE FROM "inst_item" WHERE "idInstItem" = %s
                    """, (id_inst,))
                connection.commit()
                cursor.close()
                connection.close()
                print(f"\n{Fore.LIGHTGREEN_EX}Você usou {nome}! {Fore.GREEN}+{vida_restaurada} HP")
                print(f"{Fore.LIGHTBLUE_EX}HP: {vida_atual} → {nova_vida}{Style.RESET_ALL}")
                time.sleep(2)
                return nova_vida
            else:
                print(f"{Fore.RED}Número inválido! Escolha entre 1 e {len(pocoes_numeradas)}")
        except ValueError:
            print(f"{Fore.RED}Por favor, digite um número válido!")