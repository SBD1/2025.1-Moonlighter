import subprocess
import platform
import os

def abrir_terminal(script_rel_path):
    main_path = os.path.abspath(script_rel_path)
    sistema = platform.system()

    if sistema == "Windows":
        subprocess.Popen(f'start cmd /k "mode con: cols=100 lines=30 && python \"{main_path}\""', shell=True)
    elif sistema == "Linux":
        subprocess.Popen(['gnome-terminal', '--geometry=100x30', '--', 'python3', main_path])

abrir_terminal("apps/cli/src/pg_inicial.py")