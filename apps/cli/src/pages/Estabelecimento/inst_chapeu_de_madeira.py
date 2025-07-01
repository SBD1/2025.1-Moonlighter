import time
from pages.Estabelecimento.db_estabelecimento import *
# from pages.IniciarJogo.db_iniciarJogo import buscar_seed_mundo
from pages.Estabelecimento.db_estabelecimento import (
    verificar_instancia_chapeu_de_madeira_por_jogador,
    visualizar_itens_chapeu_de_madeira_por_jogador,
    comprar_item_chapeu_de_madeira_por_jogador,
    criar_instancia_chapeu_de_madeira_por_jogador,
    exibir_dialogo_saudacao,
    exibir_dialogo_catalogo,
    exibir_dialogo_compra,
    exibir_dialogo_venda,
    exibir_dialogo_despedida
)
from setup.database import connect_to_db
from utils.limparTerminal import limpar_terminal
from utils.enterContinue import enter_continue
from colorama import Fore, Back, Style, init
import pygame
import shutil

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

def cabecalho_chapeu_de_madeira():
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}=================== O CHAPÉU DE MADEIRA ===================".center(largura_terminal))
    print(f"{Fore.YELLOW}Loja de Poções - Especializada em Poções".center(largura_terminal))
    print(f"{Fore.LIGHTGREEN_EX}========================================================".center(largura_terminal))

def calcular_preco_dinamico(preco_base, tipo_item, vendas_jogador=0):
    """
    Calcula o preço dinâmico baseado no tipo do item e comportamento do jogador
    """
    # Converter decimal.Decimal para float se necessário
    if hasattr(preco_base, '__float__'):
        preco_base = float(preco_base)
    
    # Modificador baseado no tipo do item
    modificador_tipo = 1.0
    if tipo_item == 'Pocao':
        modificador_tipo = 1.2  # +20% para poções
    elif tipo_item == 'Arma':
        modificador_tipo = 1.5  # +50% para armas
    elif tipo_item == 'Armadura':
        modificador_tipo = 1.3  # +30% para armaduras
    elif tipo_item == 'Material':
        modificador_tipo = 0.9  # -10% para materiais
    
    # Modificador baseado no comportamento do jogador
    modificador_comportamento = 1.0 - (vendas_jogador * 0.05)  # -5% por venda
    modificador_comportamento = max(0.7, modificador_comportamento)  # Mínimo 70%
    
    # Modificador de "sorte" do dia (±3%)
    import random
    modificador_sorte = 0.97 + (random.random() * 0.06)
    
    preco_final = int(preco_base * modificador_tipo * modificador_comportamento * modificador_sorte)
    return max(1, preco_final)  # Preço mínimo de 1 ouro

def buscar_vendas_jogador(jogador, item_id):
    """
    Busca quantas vezes o jogador vendeu este item
    """
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM inst_item 
                WHERE nickname = %s AND idItem = %s AND quantidade < 0
            """, (jogador, item_id))
            resultado = cursor.fetchone()
            cursor.close()
            connection.close()
            return resultado[0] if resultado else 0
        except:
            if connection:
                connection.close()
    return 0

def buscar_inventario_jogador(jogador):
    """
    Busca itens no inventário do jogador que podem ser vendidos
    """
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT ii.idItem, i.nome, i.descricao, i.tipo, i.precoBase, ii.quantidade
                FROM inst_item ii
                JOIN item i ON ii.idItem = i.idItem
                WHERE ii.nickname = %s AND ii.quantidade > 0
                ORDER BY i.nome
            """, (jogador,))
            resultado = cursor.fetchall()
            cursor.close()
            connection.close()
            return resultado
        except:
            if connection:
                connection.close()
    return []

def vender_item_para_loja(jogador, item_id, quantidade):
    """
    Vende um item para a loja
    """
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Verificar se o jogador tem o item
            cursor.execute("""
                SELECT quantidade FROM inst_item 
                WHERE nickname = %s AND idItem = %s
            """, (jogador, item_id))
            resultado = cursor.fetchone()
            
            if not resultado or resultado[0] < quantidade:
                cursor.close()
                connection.close()
                return False, "Quantidade insuficiente no inventário"
            
            # Buscar informações do item
            cursor.execute("""
                SELECT nome, precoBase, tipo FROM item WHERE idItem = %s
            """, (item_id,))
            item_info = cursor.fetchone()
            
            if not item_info:
                cursor.close()
                connection.close()
                return False, "Item não encontrado"
            
            nome_item, preco_base, tipo_item = item_info
            
            # Calcular preço de venda (metade do preço de compra)
            vendas_jogador = buscar_vendas_jogador(jogador, item_id)
            preco_compra = calcular_preco_dinamico(preco_base, tipo_item, vendas_jogador)
            preco_venda = int(preco_compra * 0.5)  # 50% do preço de compra
            
            # Calcular ouro total
            ouro_total = preco_venda * quantidade
            
            # Atualizar inventário do jogador
            cursor.execute("""
                UPDATE inst_item 
                SET quantidade = quantidade - %s 
                WHERE nickname = %s AND idItem = %s
            """, (quantidade, jogador, item_id))
            
            # Adicionar ouro ao jogador
            cursor.execute("""
                UPDATE jogador 
                SET ouro = ouro + %s 
                WHERE nickname = %s
            """, (ouro_total, jogador))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True, f"Vendeu {quantidade}x '{nome_item}' por {ouro_total} ouros"
            
        except Exception as e:
            if connection:
                connection.rollback()
                connection.close()
            return False, f"Erro ao vender item: {e}"
    
    return False, "Erro de conexão com o banco"

def menu_chapeu_de_madeira(jogador, seedMundo):
    """
    Menu principal da loja de poções
    """
    init(autoreset=True)
    
    # Exibir diálogo de saudação da comerciante
    limpar_terminal()
    cabecalho_chapeu_de_madeira()
    exibir_dialogo_saudacao("Eris", jogador)
    enter_continue()
    
    # Verificar e criar instância da loja se necessário
    if not verificar_instancia_chapeu_de_madeira_por_jogador(jogador):
        if seedMundo:
            sucesso = criar_instancia_chapeu_de_madeira_por_jogador(jogador, "O Chapéu de Madeira", 3, 15)
            if not sucesso:
                print(f"{Fore.RED}Erro ao inicializar a loja!")
                enter_continue()
                return
        else:
            print(f"{Fore.RED}Erro ao buscar informações do mundo!")
            enter_continue()
            return
    
    while True:
        limpar_terminal()
        cabecalho_chapeu_de_madeira()
        print("\n")
        print(f"{Style.BRIGHT}{Fore.CYAN}O que você gostaria de fazer?".center(largura_terminal))
        print("\n")
        print(f"{Fore.WHITE}1 - Ver poções disponíveis para compra")
        print(f"{Fore.WHITE}2 - Comprar uma poção")
        print(f"{Fore.WHITE}3 - Ver itens do seu inventário")
        print(f"{Fore.WHITE}4 - Vender um item")
        print(f"{Fore.WHITE}0 - Sair da Loja")
        print("\n")
        
        escolha = input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> ").strip()
        
        if escolha == "1":
            ver_itens_disponiveis(jogador)
        elif escolha == "2":
            comprar_item(jogador)
        elif escolha == "3":
            ver_inventario_jogador(jogador)
        elif escolha == "4":
            vender_item(jogador)
        elif escolha == "0":
            exibir_dialogo_despedida("Eris", jogador)
            enter_continue()
            break
        else:
            print(f"\n{Fore.RED}Opção inválida. Tente novamente.")
            enter_continue()

def ver_itens_disponiveis(jogador):
    """
    Função para ver poções disponíveis para compra
    """
    limpar_terminal()
    cabecalho_chapeu_de_madeira()
    
    # Exibir diálogo de catálogo
    exibir_dialogo_catalogo("Eris", jogador)
    enter_continue()
    
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== POÇÕES DISPONÍVEIS PARA COMPRA ===".center(largura_terminal))
    print(f"{Fore.YELLOW}💡 Dica: O estoque muda a cada dia!".center(largura_terminal))
    print("\n")
    
    itens = visualizar_itens_chapeu_de_madeira_por_jogador(jogador)
    if itens:
        print(f"{Fore.WHITE}{'ID':<5} {'Nome':<25} {'Preço':<10} {'Tipo':<12}")
        print(f"{Fore.LIGHTBLACK_EX}{'='*55}")
        for item in itens:
            id_item, nome, preco, descricao = item
            
            # Buscar tipo do item
            connection = connect_to_db()
            tipo_item = "Outro"
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT tipo FROM item WHERE idItem = %s", (id_item,))
                    resultado = cursor.fetchone()
                    if resultado:
                        tipo_item = resultado[0] or "Outro"
                    cursor.close()
                    connection.close()
                except:
                    if connection:
                        connection.close()
            
            # Calcular preço dinâmico
            vendas_jogador = buscar_vendas_jogador(jogador, id_item)
            preco_dinamico = calcular_preco_dinamico(preco, tipo_item, vendas_jogador)
            
            print(f"{Fore.WHITE}{id_item:<5} {nome:<25} {preco_dinamico:<10} {tipo_item:<12}")
            print(f"{Fore.LIGHTBLACK_EX}     {descricao}")
            if vendas_jogador > 0:
                print(f"{Fore.YELLOW}     ⚠️  Você já vendeu {vendas_jogador}x deste item (preço reduzido)")
            print()
    else:
        print(f"{Fore.RED}Nenhuma poção disponível para compra!")
    
    print("\n")
    enter_continue()

def ver_inventario_jogador(jogador):
    """
    Função para ver itens do inventário do jogador
    """
    limpar_terminal()
    cabecalho_chapeu_de_madeira()
    
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== SEU INVENTÁRIO ===".center(largura_terminal))
    print("\n")
    
    itens = buscar_inventario_jogador(jogador)
    if itens:
        print(f"{Fore.WHITE}{'ID':<5} {'Nome':<25} {'Qtd':<5} {'Preço Venda':<12} {'Tipo':<12}")
        print(f"{Fore.LIGHTBLACK_EX}{'='*65}")
        for item in itens:
            id_item, nome, descricao, tipo, preco_base, quantidade = item
            
            # Calcular preço de venda
            vendas_jogador = buscar_vendas_jogador(jogador, id_item)
            preco_compra = calcular_preco_dinamico(preco_base, tipo, vendas_jogador)
            preco_venda = int(preco_compra * 0.5)  # 50% do preço de compra
            
            print(f"{Fore.WHITE}{id_item:<5} {nome:<25} {quantidade:<5} {preco_venda:<12} {tipo:<12}")
            print(f"{Fore.LIGHTBLACK_EX}     {descricao}")
            print()
    else:
        print(f"{Fore.RED}Seu inventário está vazio!")
    
    print("\n")
    enter_continue()

def vender_item(jogador):
    """
    Função para vender um item
    """
    limpar_terminal()
    cabecalho_chapeu_de_madeira()
    
    # Exibir diálogo de venda
    exibir_dialogo_venda("Eris", jogador)
    enter_continue()
    
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== VENDER ITEM ===".center(largura_terminal))
    print("\n")
    
    # Mostrar itens do inventário
    itens = buscar_inventario_jogador(jogador)
    if not itens:
        print(f"{Fore.RED}Você não tem itens para vender!")
        enter_continue()
        return
    
    print(f"{Fore.WHITE}{'ID':<5} {'Nome':<25} {'Qtd':<5} {'Preço Venda':<12}")
    print(f"{Fore.LIGHTBLACK_EX}{'='*50}")
    for item in itens:
        id_item, nome, descricao, tipo, preco_base, quantidade = item
        
        # Calcular preço de venda
        vendas_jogador = buscar_vendas_jogador(jogador, id_item)
        preco_compra = calcular_preco_dinamico(preco_base, tipo, vendas_jogador)
        preco_venda = int(preco_compra * 0.5)
        
        print(f"{Fore.WHITE}{id_item:<5} {nome:<25} {quantidade:<5} {preco_venda:<12}")
    
    print(f"\n{Fore.WHITE}Digite o ID do item que deseja vender:")
    try:
        item_id = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> "))
        
        # Verificar se o item existe no inventário
        item_encontrado = None
        for item in itens:
            if item[0] == item_id:
                item_encontrado = item
                break
        
        if not item_encontrado:
            print(f"{Fore.RED}Item não encontrado no seu inventário!")
            enter_continue()
            return
        
        print(f"\n{Fore.WHITE}Digite a quantidade que deseja vender:")
        quantidade = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> "))
        
        if quantidade <= 0:
            print(f"{Fore.RED}Quantidade deve ser maior que zero!")
            enter_continue()
            return
        
        if quantidade > item_encontrado[5]:  # quantidade no inventário
            print(f"{Fore.RED}Você não tem essa quantidade no inventário!")
            enter_continue()
            return
        
        # Vender o item
        sucesso, mensagem = vender_item_para_loja(jogador, item_id, quantidade)
        
        if sucesso:
            print(f"\n{Fore.GREEN}✅ {mensagem}")
        else:
            print(f"\n{Fore.RED}❌ {mensagem}")
            
    except ValueError:
        print(f"{Fore.RED}Por favor, digite um número válido!")
    except Exception as e:
        print(f"{Fore.RED}Erro inesperado: {e}")
    
    print("\n")
    enter_continue()

def comprar_item(jogador):
    """
    Função para comprar uma poção
    """
    limpar_terminal()
    cabecalho_chapeu_de_madeira()
    print(f"\n{Style.BRIGHT}{Fore.CYAN}=== COMPRAR POÇÃO ===".center(largura_terminal))
    print("\n")
    
    # Mostrar poções disponíveis
    itens = visualizar_itens_chapeu_de_madeira_por_jogador(jogador)
    if not itens:
        print(f"{Fore.RED}Nenhuma poção disponível para compra!")
        enter_continue()
        return
    
    print(f"{Fore.WHITE}{'ID':<5} {'Nome':<25} {'Preço':<10} {'Tipo':<12}")
    print(f"{Fore.LIGHTBLACK_EX}{'='*55}")
    for item in itens:
        id_item, nome, preco, descricao = item
        
        # Buscar tipo do item
        connection = connect_to_db()
        tipo_item = "Outro"
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT tipo FROM item WHERE idItem = %s", (id_item,))
                resultado = cursor.fetchone()
                if resultado:
                    tipo_item = resultado[0] or "Outro"
                cursor.close()
                connection.close()
            except:
                if connection:
                    connection.close()
        
        # Calcular preço dinâmico
        vendas_jogador = buscar_vendas_jogador(jogador, id_item)
        preco_dinamico = calcular_preco_dinamico(preco, tipo_item, vendas_jogador)
        
        print(f"{Fore.WHITE}{id_item:<5} {nome:<25} {preco_dinamico:<10} {tipo_item:<12}")
        print(f"{Fore.LIGHTBLACK_EX}     {descricao}")
        if vendas_jogador > 0:
            print(f"{Fore.YELLOW}     ⚠️  Você já vendeu {vendas_jogador}x deste item (preço reduzido)")
        print()
    
    print(f"\n{Fore.WHITE}Digite o ID da poção que deseja comprar:")
    try:
        item_id = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> "))
        
        # Verificar se o item existe
        item_encontrado = None
        for item in itens:
            if item[0] == item_id:
                item_encontrado = item
                break
        
        if not item_encontrado:
            print(f"{Fore.RED}Poção não encontrada!")
            enter_continue()
            return
        
        print(f"\n{Fore.WHITE}Digite a quantidade que deseja comprar:")
        quantidade = int(input(f"{Style.BRIGHT}{Fore.MAGENTA}>>> "))
        
        if quantidade <= 0:
            print(f"{Fore.RED}Quantidade deve ser maior que zero!")
            enter_continue()
            return
        
        # Exibir diálogo de compra
        exibir_dialogo_compra("Eris", jogador)
        
        # Comprar o item
        sucesso = comprar_item_chapeu_de_madeira_por_jogador(jogador, item_id, quantidade)
        
        if sucesso:
            print(f"\n{Fore.GREEN}✅ {quantidade}x '{item_encontrado[1]}' comprado(s) com sucesso!")
        else:
            print(f"\n{Fore.RED}❌ Erro ao comprar poção!")
            
    except ValueError:
        print(f"{Fore.RED}Por favor, digite um número válido!")
    except Exception as e:
        print(f"{Fore.RED}Erro inesperado: {e}")
    
    print("\n")
    enter_continue() 