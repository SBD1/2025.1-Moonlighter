import subprocess
import platform
import os

def abrir_terminal(script_rel_path):
    main_path = os.path.abspath(script_rel_path)
    sistema = platform.system()

    if sistema == "Windows":
        subprocess.Popen(f'start cmd /c python "{main_path}"', shell=True)
    elif sistema == "Linux":
        subprocess.Popen(['gnome-terminal', '--', 'python3', main_path])

abrir_terminal("apps/cli/src/inicial.py")