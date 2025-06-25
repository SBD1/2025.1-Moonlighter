import random
seedMasmorra = random.randint(100, 999)

def gerar_numero_salas(dificuldade):
    if (dificuldade == 'Fácil'):
        qtd_salas: int = random.randint(5, 10)
    elif (dificuldade == 'Médio'):
        qtd_salas: int = random.randint(7, 15)
    elif (dificuldade == 'Díficil'):
        qtd_salas: int = random.randint(10, 20)
    else:
        print("Erro ao gerar o numero de salas")

    return qtd_salas

def gerar_seed(seedMasmorra): #gerar seed da sala

    #fazer algoritmo de gerar seed
    cofA = 2654435761
    cofB = 1597334677
    seedSala: int = (seedMasmorra * cofA) + (index* cofB)

    qtd_conexoes: int = random.randint(0,3)
    ordem_preenchimento: int = random.randint(0,3)

    seedSala = seedSala * 10 + qtd_conexoes
    seedSala = seedSala * 10 + ordem_preenchimento
    # os 2 ultimos digitios da seed representam a qtd de conexoes e ordem de preenchimento, nessa ordem

    return seedSala

def criar_matriz():
    linhas: int = 15
    colunas: int = 15
    matriz = [[0 for _ in range(colunas)] for _ in range(linhas)]

    return matriz

def criar_sala(x, y, matriz, limite):
    global index

    #verificacao se a sala criada sai do espaco da matriz
    if ((x >= 15) or (x < 0) or (y >= 15) or (y < 0)):
        return
    
    #verificacao se a sala criada sobrepoe outra
    if (matriz[x][y] != 0):
        return
    
    #verificacao se a sala criada excede o limite maximo de salas
    if (index>= limite):
        return

    index+= 1 #acresenta o indexglobal para o calculo da seed
    seed = gerar_seed(seedMasmorra)
    saidas = seed % 100
    ordem = seed % 10

    matriz[x][y] = seed #salva a seed da sala atual

    if (saidas != 0): #se a sala tiver pelo menos uma saida

        #ordem de preenchimento das proximas salas
        if (ordem == 0): #ordem: N-L-S-O
            criar_sala(x-1, y, matriz, limite) #norte
            criar_sala(x, y+1, matriz, limite) #leste
            criar_sala(x+1, y, matriz, limite) #sul
            criar_sala(x, y-1, matriz, limite) #oeste

        elif (ordem == 1): #ordem: L-O-N-S
            criar_sala(x, y+1, matriz, limite) #leste
            criar_sala(x, y-1, matriz, limite) #oeste
            criar_sala(x-1, y, matriz, limite) #norte
            criar_sala(x+1, y, matriz, limite) #sul

        elif (ordem == 2): #ordem: S-L-N-O
            criar_sala(x+1, y, matriz, limite) #sul
            criar_sala(x, y+1, matriz, limite) #leste
            criar_sala(x-1, y, matriz, limite) #norte
            criar_sala(x, y-1, matriz, limite) #oeste

        elif (ordem == 3): #ordem: O-L-S-N
            criar_sala(x, y-1, matriz, limite) #oeste
            criar_sala(x, y+1, matriz, limite) #leste
            criar_sala(x+1, y, matriz, limite) #sul
            criar_sala(x-1, y, matriz, limite) #norte

    else: 
        return
    


global index
index = 1

qtd_salas = gerar_numero_salas('Fácil')
matriz = criar_matriz()
posicaoX = 7
posicaoY = 7

criar_sala(posicaoX, posicaoY, matriz, qtd_salas)

for linha in matriz:
    print([0 if x != 0 else "." for x in linha])
