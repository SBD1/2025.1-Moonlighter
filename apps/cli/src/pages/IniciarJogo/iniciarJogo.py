import time
from pages.IniciarJogo.db_iniciarJogo import *
from pages.IniciarJogo.db_iniciarJogo import selecionar_jogador
from pages.Estabelecimento import menu_chapeu_de_madeira, menu_forja, menu_banco
from utils.limparTerminal import limpar_terminal
from utils.enterContinue import enter_continue
from colorama import Fore, Back, Style, init
import pygame
import shutil

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

def musicCity(): #musica da cidade
    pygame.mixer.init() 
    pygame.mixer.music.load("apps/cli/assets/musics/MoonlighterOST_02_Cidade.mp3")
    pygame.mixer.music.play(-1, fade_ms=3000)

def cabecalho():
        local_jogador: str = buscar_local_jogador()
        print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}=================== MOONLIGHTER GAME ===================".center(largura_terminal))
        print(Fore.YELLOW + f"dia: XX, periodo: XX, local: {local_jogador}".center(largura_terminal))
        print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}========================================================".center(largura_terminal))


def cabecalho_completo():
        local_jogador: str = buscar_local_jogador()
        print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}=================== MOONLIGHTER GAME ===================".center(largura_terminal))
        print(Fore.YELLOW + f"dia: XX, periodo: XX, local: {local_jogador}".center(largura_terminal))
        print(Style.BRIGHT + Fore.CYAN + "Para onde deseja ir?".center(largura_terminal))
        print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}========================================================".center(largura_terminal))
        print("\n\n")


        locais = exibir_locais(local_jogador)

        for i, local in enumerate(locais, start=1):
            print(f"{i}- {local[0]}")
        
        if (local_jogador == 'Vila Rynoka'): print(Fore.LIGHTBLACK_EX + "0- sair do jogo")
        else: print(Fore.LIGHTBLACK_EX + "0- voltar")

        while True:
            entrada = input("\nDigite: ").strip()
            if entrada == '':
                print("Por favor, digite um número.")
                continue
            
            try:
                escolha = int(entrada)
                return escolha, local_jogador
            except ValueError:
                print("Por favor, digite um número válido.")
                continue


#funcao principal
def iniciar_jogo():
    init(autoreset=True) #terminal colorido
    
    # Selecionar jogador uma vez no início
    jogador_atual = selecionar_jogador()
    if not jogador_atual:
        print(f"{Fore.RED}Erro ao selecionar jogador!")
        enter_continue()
        return
    
    musicCity()
    local_inicial("Vila Rynoka")

    # loop dos locais no terminal
    while True:

        limpar_terminal()
        escolha, local_jogador = cabecalho_completo()
        local_anterior = local_jogador

        if (escolha == 0): #sair do jogo
            pygame.mixer.music.stop()
            print("Salvando seu progresso...")
            time.sleep(2)
            print("Jogo salvo!")
            enter_continue()
            break;

        elif (escolha == 1): #Centro comercial
            novo_local: str = "Centro Comercial"
            atualizar_local_jogador(novo_local)

            while True:

                limpar_terminal()
                escolhaCC, local_jogador = cabecalho_completo()

                if (escolhaCC == 0): #voltar
                    atualizar_local_jogador(local_anterior)
                    break

                elif (escolhaCC == 1): #Forja vulcanica
                    menu_forja(jogador_atual)
                
                elif (escolhaCC == 2): #O chapeu de madeira
                    menu_chapeu_de_madeira(jogador_atual)

                elif (escolhaCC == 3): #Banco de rynoka
                    menu_banco(jogador_atual)

                elif (escolhaCC == 4): #Tenda da bruxa
                    print(f"\nBem-vindo! Ainda estão nos desenvolvendo, volte mais tarde!")
                    enter_continue()

                elif (escolhaCC == 5): #Barraca do tom
                    print(f"\nBem-vindo! Ainda estão nos desenvolvendo, volte mais tarde!")
                    enter_continue()

                else:
                    print("\nDigite um numero válido")
                    enter_continue()


        elif (escolha == 2): #Praca
            novo_local: str = "Centro Comercial"
            atualizar_local_jogador(novo_local)

            limpar_terminal()
            novo_local: str = "Praça"
            atualizar_local_jogador(novo_local)
            cabecalho()
            print("\nAinda não há nada aqui, volte mais tarde\n")
            enter_continue()
            atualizar_local_jogador(local_anterior)

            
        elif (escolha == 3): #Moonlighter    
            novo_local: str = "Moonlighter"
            atualizar_local_jogador(novo_local)

            while True:

                limpar_terminal()
                escolhaML, local_jogador = cabecalho_completo()

                if (escolhaML == 0): #voltar
                    atualizar_local_jogador(local_anterior)
                    break

                elif (escolhaML == 1): #Quarto
                    print(f"\nBem-vindo! Ainda estão nos desenvolvendo, volte mais tarde!")
                    enter_continue()
                
                elif (escolhaML == 2): #Salao de exposicao
                    print(f"\nBem-vindo! Ainda estão nos desenvolvendo, volte mais tarde!")
                    enter_continue()
                
                else:
                    print("\nDigite um numero válido")
                    enter_continue()
        

        elif (escolha == 4): #Area das masmorras
            novo_local: str = "Área das Masmorras"
            atualizar_local_jogador(novo_local)

            while True:

                limpar_terminal()
                escolhaM, local_jogador = cabecalho_completo()

                if (escolhaM == 0): #voltar
                    atualizar_local_jogador(local_anterior)
                    break

                elif (escolhaM == 1): #Golem
                    print(f"\nBem-vindo! Ainda estão nos desenvolvendo, volte mais tarde!")
                    enter_continue()
                
                elif (escolhaM == 2): #Floresta
                    print(f"\nBem-vindo! Ainda estão nos desenvolvendo, volte mais tarde!")
                    enter_continue()

                elif (escolhaM == 3): #Deserto
                    print(f"\nBem-vindo! Ainda estão nos desenvolvendo, volte mais tarde!")
                    enter_continue()

                elif (escolhaM == 4): #Recnologia
                    print(f"\nBem-vindo! Ainda estão nos desenvolvendo, volte mais tarde!")
                    enter_continue()

                else:
                    print("\nDigite um numero válido")
                    enter_continue()
        

        else:
            print("\nDigite um numero válido")
            enter_continue()