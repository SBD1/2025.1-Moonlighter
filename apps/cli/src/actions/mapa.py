# mapa.py
import shutil
from colorama import Fore, Style, init
import pyfiglet
init(autoreset=True)
print('\033[?25l', end='', flush=True)

print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + '''
        ╔═══════════════════[ RYNOKA - MAPA ]══════════════════╗
        ║                                                      ║
        ║      ÁREA DAS MASMORRAS                              ║
        ║  ┌────────────────────────┐                          ║
        ║  | Masmorra do Golem      |                          ║
        ║  | Masmorra do Deserto    |                          ║
        ║  | Masmorra da Floresta   |                          ║
        ║  | Masmorra da Tecnologia |    CENTRO COMERCIAL      ║
        ║  | Masmorra Desconhecida  | ┌─────────────────────┐  ║
        ║  └────────────────────────┘ | Forja Vulcânica     |  ║
        ║                             | O chapéu de Madeira |  ║
        ║                ┌───────┐    | Banco de Rynoka     |  ║
        ║                | Praça |    | Tenda da Bruxa      |  ║
        ║                └───────┘    | Barraca do Tom      |  ║
        ║                             └─────────────────────┘  ║
        ║        MOONLIGHTER                                   ║
        ║   ┌────────────────────┐                             ║
        ║   | Quarto             |                             ║
        ║   | Salao de exposicao |                             ║
        ║   └────────────────────┘                             ║
        ║                                                      ║
        ╚══════════════════════════════════════════════════════╝
        '''.center(shutil.get_terminal_size().columns))
print("\n")
print(Style.BRIGHT + Fore.YELLOW + "Feche a janela para sair".center(shutil.get_terminal_size().columns))