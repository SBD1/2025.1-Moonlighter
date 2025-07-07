import random
from colorama import Fore, Style, init
init(autoreset=True)

def gerar_numero_salas(dificuldade):
    if (dificuldade == 'Fácil'):
        qtd_salas: int = (seedMasmorra % 3) + 7 #de 7 a 10 salas
    elif (dificuldade == 'Médio'):
        qtd_salas: int = (seedMasmorra % 7) + 10 #de 10 a 17 salas
    elif (dificuldade == 'Difícil'):
        qtd_salas: int = (seedMasmorra % 8) + 17 #de 17 a 25 salas
    else:
        print("Erro ao gerar o numero de salas")

    return qtd_salas

def gerar_seed(seedMasmorra): #gerar seed da sala

    #fazer algoritmo de gerar seed
    cofA = 2654435761
    cofB = 1597334677
    seedSala: int = (seedMasmorra * cofA) + (index* cofB)
    random.seed(seedSala)

    qtd_conexoes: int = random.randint(0, 3)
    ordem_preenchimento: int = random.randint(0, 3)

    seedSala = seedSala * 10 + qtd_conexoes
    seedSala = seedSala * 10 + ordem_preenchimento
    # os 2 ultimos digitios da seed representam a qtd de conexoes e ordem de preenchimento, nessa ordem

    return seedSala

def criar_matriz():
    linhas: int = 25
    colunas: int = 25
    matriz = [[0 for _ in range(colunas)] for _ in range(linhas)]

    return matriz

def pode_criar_sala(x, y, matriz, limite):
    global index 

    #verificacao se a sala criada sai do espaco da matriz
    if ((x >= 25) or (x < 0) or (y >= 25) or (y < 0)):
        return False
    
    #se a sala ainda nao existe verifica o limmite de salas
    if (matriz[x][y] == 0):
        if (index >= limite):
            return False
        return True
    
    else:
        return True #sala já existe mas pode criar conexao

def adicionar_conexao(matriz, x, y, direcao): #evitar a conexao ser feita duas vezes na mesma direcao
    if direcao not in matriz[x][y]["conexoes"]:
        matriz[x][y]["conexoes"].append(direcao)

def criar_sala(x, y, matriz, limite):
    global index

    if (matriz[x][y] == 0): 

        index += 1 #acresenta o index global para o calculo da seed
        seed = gerar_seed(seedMasmorra)
        saidas = seed % 100
        ordem = seed % 10

        matriz[x][y] = { #salva a seed da sala atual e armazena as conexoes da sala
            "seed": seed,
            "conexoes": [],
            "ordem_criacao": index,
            "visitado": True,
            "boss": False
        } 
    
    else: #se a sala ja existe nao recria, apenas gera conexao
        if "visitado" in matriz[x][y] and matriz[x][y]["visitado"]:
            return
        
        matriz[x][y]["visitado"] = True
        
        seed = matriz[x][y]["seed"]
        saidas = seed % 100
        ordem = seed % 10

    if (saidas != 0): #se a sala tiver pelo menos uma saida

        #ordem de preenchimento das proximas salas
        if (ordem == 0): #ordem: N-L-S-O
            if (pode_criar_sala(x-1, y, matriz, limite)):
                criar_sala(x-1, y, matriz, limite)
                adicionar_conexao(matriz, x, y, "N") #norte
                adicionar_conexao(matriz, x-1, y, "S") #conexao oposta sul
            if (pode_criar_sala(x, y+1, matriz, limite)):
                criar_sala(x, y+1, matriz, limite) 
                adicionar_conexao(matriz, x, y, "L") #leste
                adicionar_conexao(matriz, x, y+1, "O") #conexao oposta oeste
            if (pode_criar_sala(x+1, y, matriz, limite)):
                criar_sala(x+1, y, matriz, limite) 
                adicionar_conexao(matriz, x, y, "S") #sul
                adicionar_conexao(matriz, x+1, y, "N") #conexao oposta norte
            if (pode_criar_sala(x, y-1, matriz, limite)):
                criar_sala(x, y-1, matriz, limite) 
                adicionar_conexao(matriz, x, y, "O") #oeste
                adicionar_conexao(matriz, x, y-1, "L") #conexao oposta leste

        elif (ordem == 1): #ordem: L-O-N-S
            if (pode_criar_sala(x, y+1, matriz, limite)):
                criar_sala(x, y+1, matriz, limite) 
                adicionar_conexao(matriz, x, y, "L") #leste
                adicionar_conexao(matriz, x, y+1, "O") #conexao oposta oeste
            if (pode_criar_sala(x, y-1, matriz, limite)):
                criar_sala(x, y-1, matriz, limite) 
                adicionar_conexao(matriz, x, y, "O") #oeste
                adicionar_conexao(matriz, x, y-1, "L") #conexao oposta leste
            if (pode_criar_sala(x-1, y, matriz, limite)):
                criar_sala(x-1, y, matriz, limite)
                adicionar_conexao(matriz, x, y, "N") #norte
                adicionar_conexao(matriz, x-1, y, "S") #conexao oposta sul
            if (pode_criar_sala(x+1, y, matriz, limite)):
                criar_sala(x+1, y, matriz, limite) 
                adicionar_conexao(matriz, x, y, "S") #sul
                adicionar_conexao(matriz, x+1, y, "N") #conexao oposta norte

        elif (ordem == 2): #ordem: S-L-N-O
            if (pode_criar_sala(x+1, y, matriz, limite)):
                criar_sala(x+1, y, matriz, limite) 
                adicionar_conexao(matriz, x, y, "S") #sul
                adicionar_conexao(matriz, x+1, y, "N") #conexao oposta norte
            if (pode_criar_sala(x, y+1, matriz, limite)):
                criar_sala(x, y+1, matriz, limite) 
                adicionar_conexao(matriz, x, y, "L") #leste
                adicionar_conexao(matriz, x, y+1, "O") #conexao oposta oeste
            if (pode_criar_sala(x-1, y, matriz, limite)):
                criar_sala(x-1, y, matriz, limite)
                adicionar_conexao(matriz, x, y, "N") #norte
                adicionar_conexao(matriz, x-1, y, "S") #conexao oposta sul
            if (pode_criar_sala(x, y-1, matriz, limite)):
                criar_sala(x, y-1, matriz, limite) 
                adicionar_conexao(matriz, x, y, "O") #oeste
                adicionar_conexao(matriz, x, y-1, "L") #conexao oposta leste

        elif (ordem == 3): #ordem: O-L-S-N
            if (pode_criar_sala(x, y-1, matriz, limite)):
                criar_sala(x, y-1, matriz, limite) 
                adicionar_conexao(matriz, x, y, "O") #oeste
                adicionar_conexao(matriz, x, y-1, "L") #conexao oposta leste
            if (pode_criar_sala(x, y+1, matriz, limite)):
                criar_sala(x, y+1, matriz, limite) 
                adicionar_conexao(matriz, x, y, "L") #leste
                adicionar_conexao(matriz, x, y+1, "O") #conexao oposta oeste
            if (pode_criar_sala(x+1, y, matriz, limite)):
                criar_sala(x+1, y, matriz, limite) 
                adicionar_conexao(matriz, x, y, "S") #sul
                adicionar_conexao(matriz, x+1, y, "N") #conexao oposta norte
            if (pode_criar_sala(x-1, y, matriz, limite)):
                criar_sala(x-1, y, matriz, limite)
                adicionar_conexao(matriz, x, y, "N") #norte
                adicionar_conexao(matriz, x-1, y, "S") #conexao oposta sul

    else: 
        return
    
def encontrar_caminho_mais_longo(matriz, inicio_x, inicio_y):
    linhas = len(matriz)
    colunas = len(matriz[0])
    
    melhor_caminho = []
    visitados = set()

    # Mapear direções para deslocamentos (x, y)
    direcoes = {
        "N": (-1, 0),
        "S": (1, 0),
        "L": (0, 1),
        "O": (0, -1)
    }

    def dfs(x, y, caminho_atual):
        nonlocal melhor_caminho

        visitados.add((x, y))
        caminho_atual.append((x, y))

        # Atualiza o melhor caminho se o atual for maior
        if len(caminho_atual) > len(melhor_caminho):
            melhor_caminho = caminho_atual.copy()

        # Explora conexões
        for direcao in matriz[x][y]["conexoes"]:
            dx, dy = direcoes[direcao]
            nx, ny = x + dx, y + dy

            if 0 <= nx < linhas and 0 <= ny < colunas:
                if matriz[nx][ny] != 0 and (nx, ny) not in visitados:
                    dfs(nx, ny, caminho_atual)

        caminho_atual.pop()
        visitados.remove((x, y))

    dfs(inicio_x, inicio_y, [])

    return melhor_caminho

def marcar_sala_boss(matriz, caminho):
    if not caminho:
        print("Nenhum caminho encontrado.")
        return

    boss_x, boss_y = caminho[-1]
    matriz[boss_x][boss_y]["boss"] = True
    # print(Fore.YELLOW + f"Sala do Boss definida em ({boss_x},{boss_y})")


def imprimir_mapa_detalhado(matriz):
    print(Fore.YELLOW + f"seed da masmorra: {seedMasmorra}\n")
    
    # Imprime detalhes de cada sala
    for x, linha in enumerate(matriz):
        for y, sala in enumerate(linha):
            if sala == 0:
                pass
            else:
                seed = sala["seed"]
                conexoes = "".join(sala["conexoes"]) if sala["conexoes"] else "-"
                ordem = sala.get("ordem_criacao", "?")
                print(f"({x},{y}): Ordem {ordem}, Seed {seed}, Conexoes: {conexoes}")
    
    print("\n")
    
    # Imprime o mapa visual
    for x, linha in enumerate(matriz):
        linha_str = []
        for y, valor in enumerate(linha):
            if valor != 0:
                if "boss" in valor and valor["boss"]:
                    cor = Fore.YELLOW
                    char = "B"
                else:
                    cor = Fore.RED
                    char = "0"
            else:
                cor = Style.RESET_ALL
                char = "."
            
            if x == 12 and y == 12:
                cor = Fore.YELLOW
                char = "0"
            
            linha_str.append(cor + char + Style.RESET_ALL)
        print(" ".join(linha_str))



def gerarMasmorra(dadosMasmorra):
    global seedMasmorra
    seedMasmorra = random.randint(1000, 9999)

    while True:
        global index
        index = 0

        qtd_salas = gerar_numero_salas(dadosMasmorra[2])
        matriz = criar_matriz()

        #centro da matriz
        posicaoX = 12 
        posicaoY = 12

        criar_sala(posicaoX, posicaoY, matriz, qtd_salas)

        if index == qtd_salas:
            break

    caminho_mais_longo = encontrar_caminho_mais_longo(matriz, posicaoX, posicaoY)
    marcar_sala_boss(matriz, caminho_mais_longo)
    # imprimir_mapa_detalhado(matriz)
    return matriz, seedMasmorra