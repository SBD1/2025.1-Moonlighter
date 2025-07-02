from colorama import Fore, Style
import shutil

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

def enter_continue():
    print('\033[?25l', end='', flush=True)  # Esconde o cursor
    print("\n")
    print(f"{Style.BRIGHT}{Fore.LIGHTBLACK_EX}Pressione Enter para continuar...".center(largura_terminal))
    input("")
    print('\033[?25h', end='', flush=True)  # Mostra o cursor