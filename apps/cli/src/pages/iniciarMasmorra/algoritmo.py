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
    
    #verificacao se a sala criada sobrepoe outra
    elif (matriz[x][y] != 0):
        return False
    
    #verificacao se a sala criada excede o limite maximo de salas
    elif (index >= limite):
        return False
    
    return True


def criar_sala(x, y, matriz, limite):
    global index

    index += 1 #acresenta o index global para o calculo da seed
    seed = gerar_seed(seedMasmorra)
    saidas = seed % 100
    ordem = seed % 10

    matriz[x][y] = { #salva a seed da sala atual e armazena as conexoes da sala
        "seed": seed,
        "conexoes": []
    } 

    if (saidas != 0): #se a sala tiver pelo menos uma saida

        #ordem de preenchimento das proximas salas
        if (ordem == 0): #ordem: N-L-S-O
            if (pode_criar_sala(x-1, y, matriz, limite)):
                criar_sala(x-1, y, matriz, limite)
                matriz[x][y]["conexoes"].append("N") #norte
            if (pode_criar_sala(x, y+1, matriz, limite)):
                criar_sala(x, y+1, matriz, limite) 
                matriz[x][y]["conexoes"].append("L") #leste
            if (pode_criar_sala(x+1, y, matriz, limite)):
                criar_sala(x+1, y, matriz, limite) 
                matriz[x][y]["conexoes"].append("S") #sul
            if (pode_criar_sala(x, y-1, matriz, limite)):
                criar_sala(x, y-1, matriz, limite) 
                matriz[x][y]["conexoes"].append("O") #oeste

        elif (ordem == 1): #ordem: L-O-N-S
            if (pode_criar_sala(x, y+1, matriz, limite)):
                criar_sala(x, y+1, matriz, limite) 
                matriz[x][y]["conexoes"].append("L") #leste
            if (pode_criar_sala(x, y-1, matriz, limite)):
                criar_sala(x, y-1, matriz, limite) 
                matriz[x][y]["conexoes"].append("O") #oeste
            if (pode_criar_sala(x-1, y, matriz, limite)):
                    criar_sala(x-1, y, matriz, limite)
                    matriz[x][y]["conexoes"].append("N") #norte
            if (pode_criar_sala(x+1, y, matriz, limite)):
                criar_sala(x+1, y, matriz, limite) 
                matriz[x][y]["conexoes"].append("S") #sul

        elif (ordem == 2): #ordem: S-L-N-O
            if (pode_criar_sala(x+1, y, matriz, limite)):
                criar_sala(x+1, y, matriz, limite) 
                matriz[x][y]["conexoes"].append("S") #sul
            if (pode_criar_sala(x, y+1, matriz, limite)):
                criar_sala(x, y+1, matriz, limite) 
                matriz[x][y]["conexoes"].append("L") #leste
            if (pode_criar_sala(x-1, y, matriz, limite)):
                    criar_sala(x-1, y, matriz, limite)
                    matriz[x][y]["conexoes"].append("N") #norte
            if (pode_criar_sala(x, y-1, matriz, limite)):
                criar_sala(x, y-1, matriz, limite) 
                matriz[x][y]["conexoes"].append("O") #oeste

        elif (ordem == 3): #ordem: O-L-S-N
            if (pode_criar_sala(x, y-1, matriz, limite)):
                criar_sala(x, y-1, matriz, limite) 
                matriz[x][y]["conexoes"].append("O") #oeste
            if (pode_criar_sala(x, y+1, matriz, limite)):
                criar_sala(x, y+1, matriz, limite) 
                matriz[x][y]["conexoes"].append("L") #leste
            if (pode_criar_sala(x+1, y, matriz, limite)):
                criar_sala(x+1, y, matriz, limite) 
                matriz[x][y]["conexoes"].append("S") #sul
            if (pode_criar_sala(x-1, y, matriz, limite)):
                    criar_sala(x-1, y, matriz, limite)
                    matriz[x][y]["conexoes"].append("N") #norte

    else: 
        return
    

def algoritmo_central(nickname):
    global index
    global seedMasmorra

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

        #fazer logica de definir o chefe
       
    salvarMasmorra(nickname)
    return matriz #mapa completo, matriz preenchida