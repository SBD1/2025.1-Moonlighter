from colorama import Fore, Style, init
from pages.IniciarJogo.iniciarJogo import iniciar_jogo
from pages.Tutorial.db_tutorial import buscarNarracao
from utils.limparTerminal import limpar_terminal
from utils.recolocarTexto import recolocarTexto
import time
import shutil
import pygame
import pyfiglet
import os
import sys
import textwrap

def musicTheme():
    pygame.mixer.init()
    pygame.mixer.music.load("apps/cli/assets/musics/MoonlighterOST_17_TiredRynoka.mp3")
    pygame.mixer.music.play(-1, fade_ms=5000)

def print_fade_in_centered(text, delay=0.05):
    largura_terminal = shutil.get_terminal_size().columns
    # Quebra o texto em linhas que caibam no terminal
    linhas = textwrap.wrap(text, width=largura_terminal - 4)  # margem para centralizar
    for linha in linhas:
        linha_centralizada = linha.center(largura_terminal)
        for i in range(1, len(linha_centralizada) + 1):
            sys.stdout.write('\r' + Style.BRIGHT + Fore.YELLOW + linha_centralizada[:i])
            sys.stdout.flush()
            time.sleep(delay)
        print(Style.RESET_ALL)  # Pula para a próxima linha e reseta o estilo

def exibirHistoria(dadosJogador):
  limpar_terminal()
  print('\033[?25l', end='', flush=True)
  musicTheme()
  dialogo = ""
  busca = None
  time.sleep(3)

#   while True:
#     limpar_terminal()
#     print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
#     dialogo = buscarNarracao(busca)


#     if dialogo is None:
#         break

#     print_fade_in_centered(recolocarTexto("<NOME_DO_JOGADOR>", dialogo[0], dadosJogador[0]), delay=0.04)
#     time.sleep(3)
#     busca = dialogo[1]

  limpar_terminal()
  pygame.mixer.music.fadeout(7000)
  time.sleep(7)
  print('\033[?25h', end='', flush=True)
  iniciar_jogo(dadosJogador[0])