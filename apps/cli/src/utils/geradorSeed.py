import random
import string

def gerarSeed(tamanho=30):
    caracteres = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e números
    return ''.join(random.choices(caracteres, k=tamanho))