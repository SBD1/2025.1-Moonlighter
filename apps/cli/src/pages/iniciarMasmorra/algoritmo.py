import random
from db_iniciarMasmorra import salvarMasmorra

def gerar_numero_salas(dificuldade):
    if (dificuldade == 'Fácil'):
        qtd_salas: int = (seedMasmorra % 5) + 5 #de 5 a 10 salas
    elif (dificuldade == 'Médio'):
        qtd_salas: int = (seedMasmorra % 7) + 8 #de 7 a 15 salas
    elif (dificuldade == 'Díficil'):
        qtd_salas: int = (seedMasmorra % 10) + 10 #de 10 a 20 salas
    else:
        print("Erro ao gerar o numero de salas")

    return qtd_salas

def gerar_seed(): #gerar seed da sala

    global seedMasmorra

    #fazer algoritmo de gerar seed
    cofA = 2654435761
    cofB = 1597334677
    seedSala: int = (seedMasmorra * cofA) + (index * cofB)
    random.seed(seedSala)

    qtd_conexoes: int = random.randint(0, 3)
    ordem_preenchimento: int = random.randint(0, 3)

    seedSala = seedSala * 10 + qtd_conexoes
    seedSala = seedSala * 10 + ordem_preenchimento
    # os 2 ultimos digitios da seed representam a qtd de conexoes e ordem de preenchimento, nessa ordem

    return seedSala

def criar_matriz():
    linhas: int = 15
    colunas: int = 15
    matriz = [[0 for _ in range(colunas)] for _ in range(linhas)]

    return matriz

def pode_criar_sala(x, y, matriz, limite):
    global index 

    #verificacao se a sala criada sai do espaco da matriz
    if ((x >= 15) or (x < 0) or (y >= 15) or (y < 0)):
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
            "visitado": True #evita chamadas infinitas, marca que a logica de geracao ja foi feita
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

def algoritmo_central(nickname):
    global index
    global seedMasmorra

    #centro da matriz
    posicaoX = 7
    posicaoY = 7

    while True: #Verifica a quantidade de salas, se nao foi criado todas, descarta a matriz e comeca do zero
        index = 0
        seedMasmorra = random.randint(1000, 9999)
        qtd_salas = gerar_numero_salas(dificuldade)
        
        matriz = criar_matriz()
        criar_sala(posicaoX, posicaoY, matriz, qtd_salas) #comeca a geracao de salas a partir do centro

        if (index == qtd_salas):  
            break

    #logica de definir a sala do chefe
    caminho_mais_longo = encontrar_caminho_mais_longo(matriz, posicaoX, posicaoY)
    marcar_sala_boss(matriz, caminho_mais_longo)

    salvarMasmorra(nickname)
    return matriz #mapa completo, matriz preenchida