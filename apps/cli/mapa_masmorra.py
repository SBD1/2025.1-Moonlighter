import time
import os

mapa = [
    "###########",
    "#@        #",
    "#   ##    #",
    "#        ##",
    "###########"
]

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("== MAPA DA MASMORRA ==")
    for linha in mapa:
        print(linha)
    time.sleep(1)
