import random
from colorama import Fore, Style, init
init(autoreset=True)

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
        "conexoes": [],
        "ordem_criacao": index
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

from colorama import Fore, Style

def imprimir_mapa_detalhado(matriz):
    print(Fore.YELLOW + f"seed da masmorra: {seedMasmorra}\n")
    
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
    for x, linha in enumerate(matriz):
        linha_str = []
        for y, valor in enumerate(linha):
            if valor != 0:
                cor = Fore.RED
                char = "0"
            else:
                cor = Style.RESET_ALL
                char = "."
            
            if x == 7 and y == 7:
                cor = Fore.YELLOW
                char = "0"  
            
            linha_str.append(cor + char + Style.RESET_ALL)
        print(" ".join(linha_str))


#seedMasmorra = 41859
seedMasmorra = random.randint(1000, 9999)

while True:
    global index
    index = 0

    qtd_salas = gerar_numero_salas('Díficil')
    matriz = criar_matriz()
    posicaoX = 7
    posicaoY = 7

    criar_sala(posicaoX, posicaoY, matriz, qtd_salas)

    if index == qtd_salas:
        break

imprimir_mapa_detalhado(matriz)