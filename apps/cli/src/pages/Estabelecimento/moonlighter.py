from colorama import Fore, Back, Style, init
import time
from utils.limparTerminal import limpar_terminal
from utils.enterContinue import enter_continue
import shutil
import textwrap
import sys
from pages.Estabelecimento.db_moonlighter import *
from pages.IniciarJogo.db_iniciarJogo import buscar_dadosJogador, buscarInfoMundo, buscarDescricaoLocal

# definição da largura da janela do terminal:
largura_terminal = shutil.get_terminal_size().columns

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

def print_in_centered(text):
    largura_terminal = shutil.get_terminal_size().columns
    # Quebra o texto em linhas que caibam no terminal
    linhas = textwrap.wrap(text, width=largura_terminal - 4)  # margem para centralizar
    for linha in linhas:
        linha_centralizada = linha.center(largura_terminal)
        print(Style.BRIGHT + Fore.WHITE + linha_centralizada)

def cabecalho(nickname):
    limpar_terminal()
    dadosJogador = buscar_dadosJogador(nickname)
    dadosMundo = buscarInfoMundo(nickname)

    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╔════════════════════[ MOONLIGHTER GAME ]════════════════════╗".center(largura_terminal))
    print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}{dadosJogador[0]}".center(largura_terminal))
    print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}HP: {dadosJogador[1]} / {dadosJogador[2]} | OURO: {dadosJogador[3]}".center(largura_terminal))
    print("\n")
    print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}{dadosJogador[6]}".center(largura_terminal))
    print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}DIA: {dadosMundo[3]} | PERÍODO: {dadosMundo[2]}".center(largura_terminal))
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╚════════════════════════════════════════════════════════════╝".center(largura_terminal))
    
    print("\n")

    print_in_centered(buscarDescricaoLocal(dadosJogador[6]))
    print("\n")

def quarto(nickname):
  limpar_terminal()

  while True:
    cabecalho(nickname)
    print(f"{Style.BRIGHT + Fore.YELLOW}O que você deseja fazer?".center(largura_terminal))

    print(Style.BRIGHT + Fore.YELLOW + "1. Dormir")
    print(Style.BRIGHT + Fore.YELLOW + "2. Ver Baú da Casa")
    print(Style.BRIGHT + Fore.YELLOW + "3. Ir para a Sala de Exposição")
    print(Style.BRIGHT + Fore.RED + "4. Sair de Moonlighter")

    print("\n\n\n")
    print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "Digite a opção desejada: ")
    opcao = input(Style.BRIGHT + Fore.MAGENTA + ">>> ")

    if not opcao.isdigit():
      limpar_terminal()
      print("\n\n\n\n\n\n")
      print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
      time.sleep(2)
      continue
    elif int(opcao) == 1:
      restaurarSaudeJogador(nickname)
      limpar_terminal()
      print('\033[?25l', end='', flush=True)
      dialogo = ""
      busca = None

      while True:
        limpar_terminal()
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        dialogo = buscarNarracao(busca)


        if dialogo is None:
            print('\033[?25h', end='', flush=True)
            break

        print_fade_in_centered(dialogo[0], delay=0.03)
        time.sleep(3)
        busca = dialogo[1]
        limpar_terminal()
        print("\n\n\n\n\n")
      
      passarDiaMundo(nickname)
      limpar_terminal()
      continue
    elif int(opcao) == 2:
      limpar_terminal()
      cabecalho(nickname)
      itensJogador = buscarItensJogador(nickname)
      itensBau = buscarItensBaudeCasa(nickname)
      print(f"{Style.BRIGHT}{Fore.YELLOW}══════════════════════════[ INVENTÁRIO ]══════════════════════════".center(largura_terminal))
      if not itensJogador:
         print(f"{Style.BRIGHT}{Fore.WHITE}Nenhum item no inventário".center(largura_terminal))
         print(f"{Style.BRIGHT}{Fore.YELLOW}═══════════════════════════════════════════════════════════════".center(largura_terminal))
      else:
         for item in itensJogador:
             print(f"{Style.BRIGHT}{Fore.WHITE}{item[0]} (x{item[1]})".center(largura_terminal))
         print(f"{Style.BRIGHT}{Fore.YELLOW}══════════════════════════════════════════════════════════════════".center(largura_terminal))
      
      print("\n")
      print(f"{Style.BRIGHT}{Fore.YELLOW}══════════════════════════[ BAÚ DA CASA ]══════════════════════════".center(largura_terminal))
      if not itensBau:
         print(f"{Style.BRIGHT}{Fore.WHITE}Nenhum item no baú".center(largura_terminal))
         print(f"{Style.BRIGHT}{Fore.YELLOW}═══════════════════════════════════════════════════════════════".center(largura_terminal))
      else:
         for item in itensBau:
             print(f"{Style.BRIGHT}{Fore.WHITE}{item[0]} (x{item[1]})".center(largura_terminal))
         print(f"{Style.BRIGHT}{Fore.YELLOW}══════════════════════════════════════════════════════════════════".center(largura_terminal))

      print("\n")
      print(f"{Style.BRIGHT}{Fore.YELLOW}O que você deseja fazer?".center(largura_terminal))
      print(Style.BRIGHT + Fore.YELLOW + "1. Guardar Itens no Baú")
      print(Style.BRIGHT + Fore.YELLOW + "2. Retirar Itens do Baú")
      print(Style.BRIGHT + Fore.RED + "3. Fechar o Baú")

      print("\n\n\n")
      print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "Digite a opção desejada: ")
      opcao = input(Style.BRIGHT + Fore.MAGENTA + ">>> ")

      if not opcao.isdigit():
        limpar_terminal()
        print("\n\n\n\n\n\n")
        print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
        time.sleep(2)
        continue
      elif int(opcao) < 1 or int(opcao) > 3:
        limpar_terminal()
        print("\n\n\n\n\n\n")
        print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
        time.sleep(2)
        continue
      elif int(opcao) == 1:
        limpar_terminal()
        cabecalho(nickname)
        print(f"{Style.BRIGHT}{Fore.YELLOW}Escolha um item para guardar no baú:".center(largura_terminal))
        print(f"{Style.BRIGHT}{Fore.RED}>> DIGITE 0 PARA VOLTAR <<".center(largura_terminal))
        print("\n")
        for opcao, item in enumerate(itensJogador, start=1):
          print(f"{Style.BRIGHT + Fore.WHITE}{opcao}. {item[0]} (x{item[1]})".center(largura_terminal))

        print("\n")
        print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "Digite a opção desejada: ")
        opcao = input(Style.BRIGHT + Fore.MAGENTA + ">>> ")

        if not opcao.isdigit():
          limpar_terminal()
          print("\n\n\n\n\n\n")
          print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
          time.sleep(2)
          continue
        elif int(opcao) == 0:
          limpar_terminal()
          continue
        elif int(opcao) < 1 or int(opcao) > len(itensJogador):
          limpar_terminal()
          print("\n\n\n\n\n\n")
          print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
          time.sleep(2)
          continue
        else:
          item = itensJogador[int(opcao) - 1]
          if item[1] > 1:
            limpar_terminal()
            cabecalho(nickname)
            print(f"{Style.BRIGHT + Fore.YELLOW}Quantas unidades de [{item[0]}] você deseja guardar? (Máximo {item[1]})".center(largura_terminal))
            quantidade = input(f"{Style.BRIGHT + Fore.MAGENTA}>>> ")
            if not quantidade.isdigit():
              limpar_terminal()
              print("\n\n\n\n\n\n")
              print(Style.BRIGHT + Fore.RED + "Quantidade inválida. Tente novamente.".center(largura_terminal))
              time.sleep(2)
              continue
            quantidade = int(quantidade)
            if quantidade < 1 or quantidade > item[1]:
              limpar_terminal()
              print("\n\n\n\n\n\n")
              print(Style.BRIGHT + Fore.RED + "Quantidade inválida. Tente novamente.".center(largura_terminal))
              time.sleep(2)
              continue
            else:
              limpar_terminal()
              cabecalho(nickname)
              print("\n\n\n\n")
              print(f"{Style.BRIGHT + Fore.YELLOW}Guardando {quantidade} unidades de [{item[0]}] no Baú....".center(largura_terminal))
              time.sleep(2)
              moverItemParaBaudeCasa(nickname, item[3], quantidade, item[4], item[5])
              limpar_terminal()
              cabecalho(nickname)
              print("\n\n\n\n")
              print(f"{Style.BRIGHT + Fore.YELLOW}Item guardado com sucesso!".center(largura_terminal))
              time.sleep(2)
              continue
          else:
            limpar_terminal()
            cabecalho(nickname)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT + Fore.YELLOW}Guardando {item[0]} no Baú....".center(largura_terminal))
            time.sleep(2)
            moverItemParaBaudeCasa(nickname, item[3], item[1], item[4], item[5])
            limpar_terminal()
            cabecalho(nickname)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT + Fore.YELLOW}Item guardado com sucesso!".center(largura_terminal))
            time.sleep(2)
            continue
      elif int(opcao) == 2:
        limpar_terminal()
        cabecalho(nickname)
        print(f"{Style.BRIGHT}{Fore.YELLOW}Escolha um item para guardar no baú:".center(largura_terminal))
        print(f"{Style.BRIGHT}{Fore.RED}>> DIGITE 0 PARA VOLTAR <<".center(largura_terminal))
        print("\n")
        for opcao, item in enumerate(itensBau, start=1):
          print(f"{Style.BRIGHT + Fore.WHITE}{opcao}. {item[0]} (x{item[1]})".center(largura_terminal))

        print("\n")
        print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "Digite a opção desejada: ")
        opcao = input(Style.BRIGHT + Fore.MAGENTA + ">>> ")

        if not opcao.isdigit():
          limpar_terminal()
          print("\n\n\n\n\n\n")
          print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
          time.sleep(2)
          continue
        elif int(opcao) == 0:
          limpar_terminal()
          continue
        elif int(opcao) < 1 or int(opcao) > len(itensBau):
          limpar_terminal()
          print("\n\n\n\n\n\n")
          print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
          time.sleep(2)
          continue
        else:
          item = itensBau[int(opcao) - 1]
          if item[1] > 1:
            limpar_terminal()
            cabecalho(nickname)
            print(f"{Style.BRIGHT + Fore.YELLOW}Quantas unidades de [{item[0]}] você deseja retirar? (Máximo {item[1]})".center(largura_terminal))
            quantidade = input(f"{Style.BRIGHT + Fore.MAGENTA}>>> ")
            if not quantidade.isdigit():
              limpar_terminal()
              print("\n\n\n\n\n\n")
              print(Style.BRIGHT + Fore.RED + "Quantidade inválida. Tente novamente.".center(largura_terminal))
              time.sleep(2)
              continue
            quantidade = int(quantidade)
            if quantidade < 1 or quantidade > item[1]:
              limpar_terminal()
              print("\n\n\n\n\n\n")
              print(Style.BRIGHT + Fore.RED + "Quantidade inválida. Tente novamente.".center(largura_terminal))
              time.sleep(2)
              continue
            else:
              limpar_terminal()
              cabecalho(nickname)
              print("\n\n\n\n")
              print(f"{Style.BRIGHT + Fore.YELLOW}Retirando {quantidade} unidades de [{item[0]}] do Baú....".center(largura_terminal))
              time.sleep(2)
              moverItemDoBaudeCasa(nickname, item[5], quantidade, item[3])
              limpar_terminal()
              cabecalho(nickname)
              print("\n\n\n\n")
              print(f"{Style.BRIGHT + Fore.YELLOW}Item retirado com sucesso!".center(largura_terminal))
              time.sleep(2)
              continue
          else:
            limpar_terminal()
            cabecalho(nickname)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT + Fore.YELLOW}Retirando {item[0]} do Baú....".center(largura_terminal))
            time.sleep(2)
            moverItemDoBaudeCasa(nickname, item[5], item[1], item[3])
            limpar_terminal()
            cabecalho(nickname)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT + Fore.YELLOW}Item retirado com sucesso!".center(largura_terminal))
            time.sleep(2)
            continue
      
      elif int(opcao) == 3:
        limpar_terminal()
        continue

    elif int(opcao) == 3:
      mudarLocalizacaoJogador(nickname, "Salão de Exposição")
      return "Salao de Exposição"
    elif int(opcao) == 4:
      atualizarParaLocalAnterior(nickname)
      return "Sair"

def sala_exposicao(nickname):
  limpar_terminal()

  while True:
    cabecalho(nickname)
    print(f"{Style.BRIGHT + Fore.YELLOW}O que você deseja fazer?".center(largura_terminal))

    print(Style.BRIGHT + Fore.YELLOW + "1. Gerenciar Itens para Vender")
    print(Style.BRIGHT + Fore.YELLOW + "2. Abrir o Moonlighter para Vendas")
    print(Style.BRIGHT + Fore.YELLOW + "3. Ir para o Quarto")
    print(Style.BRIGHT + Fore.RED + "4. Sair de Moonlighter")

    print("\n\n\n")
    print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "Digite a opção desejada: ")
    opcao = input(Style.BRIGHT + Fore.MAGENTA + ">>> ")

    if not opcao.isdigit():
      limpar_terminal()
      print("\n\n\n\n\n\n")
      print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
      time.sleep(2)
      continue
    elif int(opcao) < 1 or int(opcao) > 4:
      limpar_terminal()
      print("\n\n\n\n\n\n")
      print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
      time.sleep(2)
      continue
    elif int(opcao) == 1:
      limpar_terminal()
      cabecalho(nickname)
      itensJogador = buscarItensJogador(nickname)
      itensMoonlighter = buscarItensMoonlighter(nickname)
      print(f"{Style.BRIGHT}{Fore.YELLOW}══════════════════════════[ INVENTÁRIO ]═══════════════════════════".center(largura_terminal))
      if not itensJogador:
         print(f"{Style.BRIGHT}{Fore.WHITE}Nenhum item no inventário".center(largura_terminal))
         print(f"{Style.BRIGHT}{Fore.YELLOW}═══════════════════════════════════════════════════════════════".center(largura_terminal))
      else:
         for item in itensJogador:
             print(f"{Style.BRIGHT}{Fore.WHITE}{item[0]} (x{item[1]})".center(largura_terminal))
         print(f"{Style.BRIGHT}{Fore.YELLOW}══════════════════════════════════════════════════════════════════".center(largura_terminal))
      print("\n")
      print(f"{Style.BRIGHT}{Fore.YELLOW}══════════════════════════[ ITENS NO MOONLIGHTER ]═══════════════════════════".center(largura_terminal))
      if not itensMoonlighter:
         print(f"{Style.BRIGHT}{Fore.WHITE}Nenhum item no Moonlighter".center(largura_terminal))
         print(f"{Style.BRIGHT}{Fore.YELLOW}═══════════════════════════════════════════════════════════════".center(largura_terminal))
      else:
         for item in itensMoonlighter:
             print(f"{Style.BRIGHT}{Fore.WHITE}{item[0]} (x{item[1]})".center(largura_terminal))
         print(f"{Style.BRIGHT}{Fore.YELLOW}══════════════════════════════════════════════════════════════════".center(largura_terminal))
      print("\n")
      print(f"{Style.BRIGHT}{Fore.YELLOW}O que você deseja fazer?".center(largura_terminal))
      print(Style.BRIGHT + Fore.YELLOW + "1. Adicionar Itens para Vender")
      print(Style.BRIGHT + Fore.YELLOW + "2. Remover Itens do Moonlighter")
      print(Style.BRIGHT + Fore.RED + "3. Fechar o Gerenciador de Itens")

      print("\n\n\n")
      print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "Digite a opção desejada: ")
      opcao = input(Style.BRIGHT + Fore.MAGENTA + ">>> ")

      if not opcao.isdigit():
        limpar_terminal()
        print("\n\n\n\n\n\n")
        print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
        time.sleep(2)
        continue
      elif int(opcao) < 1 or int(opcao) > 3:
        limpar_terminal()
        print("\n\n\n\n\n\n")
        print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
        time.sleep(2)
        continue
      elif int(opcao) == 1:
        limpar_terminal()
        cabecalho(nickname)
        print(f"{Style.BRIGHT + Fore.YELLOW}Escolha um item para adicionar ao Moonlighter:".center(largura_terminal))
        print(f"{Style.BRIGHT + Fore.RED}>> DIGITE 0 PARA VOLTAR <<".center(largura_terminal))
        print("\n")
        for opcao, item in enumerate(itensJogador, start=1):
          print(f"{Style.BRIGHT + Fore.WHITE}{opcao}. {item[0]} (x{item[1]})".center(largura_terminal))

        print("\n")
        print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "Digite a opção desejada: ")
        opcao = input(Style.BRIGHT + Fore.MAGENTA + ">>> ")

        if not opcao.isdigit():
          limpar_terminal()
          print("\n\n\n\n\n\n")
          print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
          time.sleep(2)
          continue
        elif int(opcao) == 0:
          limpar_terminal()
          continue
        elif int(opcao) < 1 or int(opcao) > len(itensJogador):
          limpar_terminal()
          print("\n\n\n\n\n\n")
          print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
          time.sleep(2)
          continue
        else:
          item = itensJogador[int(opcao) - 1]
          if item[1] > 1:
            limpar_terminal()
            cabecalho(nickname)
            print(f"{Style.BRIGHT + Fore.YELLOW}Quantas unidades de [{item[0]}] você deseja adicionar? (Máximo {item[1]})".center(largura_terminal))
            quantidade = input(f"{Style.BRIGHT + Fore.MAGENTA}>>> ")
            if not quantidade.isdigit():
              limpar_terminal()
              print("\n\n\n\n\n\n")
              print(Style.BRIGHT + Fore.RED + "Quantidade inválida. Tente novamente.".center(largura_terminal))
              time.sleep(2)
              continue
            quantidade = int(quantidade)
            if quantidade < 1 or quantidade > item[1]:
              limpar_terminal()
              print("\n\n\n\n\n\n")
              print (Style.BRIGHT + Fore.RED + "Quantidade inválida. Tente novamente.".center(largura_terminal))
              time.sleep(2)
              continue
            else:
              limpar_terminal()
              cabecalho(nickname)
              print("\n\n\n\n")
              print(f"{Style.BRIGHT + Fore.YELLOW}Adicionando {quantidade} unidades de [{item[0]}] ao Moonlighter....".center(largura_terminal))
              time.sleep(2)
              adicionarItemMoonlighter(nickname, item[5], quantidade, item[4], item[3])
              limpar_terminal()
              cabecalho(nickname)
              print("\n\n\n\n")
              print(f"{Style.BRIGHT + Fore.YELLOW}Item adicionado com sucesso!".center(largura_terminal))
              time.sleep(2)
              continue
          else:
            limpar_terminal()
            cabecalho(nickname)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT + Fore.YELLOW}Adicionando [{item[0]}] ao Moonlighter....".center(largura_terminal))
            time.sleep(2)
            adicionarItemMoonlighter(nickname, item[5], item[1], item[4], item[3])
            limpar_terminal()
            cabecalho(nickname)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT + Fore.YELLOW}Item adicionado com sucesso!".center(largura_terminal))
            time.sleep(2)
            continue
      elif int(opcao) == 2:
        limpar_terminal()
        cabecalho(nickname)
        print(f"{Style.BRIGHT + Fore.YELLOW}Escolha um item para remover do Moonlighter:".center(largura_terminal))
        print(f"{Style.BRIGHT + Fore.RED}>> DIGITE 0 PARA VOLTAR <<".center(largura_terminal))
        print("\n")
        for opcao, item in enumerate(itensMoonlighter, start=1):
          print(f"{Style.BRIGHT + Fore.WHITE}{opcao}. {item[0]} (x{item[1]})".center(largura_terminal))

        print("\n")
        print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "Digite a opção desejada: ")
        opcao = input(Style.BRIGHT + Fore.MAGENTA + ">>> ")

        if not opcao.isdigit():
          limpar_terminal()
          print("\n\n\n\n\n\n")
          print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
          time.sleep(2)
          continue
        elif int(opcao) == 0:
          limpar_terminal()
          continue
        elif int(opcao) < 1 or int(opcao) > len(itensMoonlighter):
          limpar_terminal()
          print("\n\n\n\n\n\n")
          print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
          time.sleep(2)
          continue
        else:
          item = itensMoonlighter[int(opcao) - 1]
          if item[1] > 1:
            limpar_terminal()
            cabecalho(nickname)
            print(f"{Style.BRIGHT + Fore.YELLOW}Quantas unidades de [{item[0]}] você deseja remover? (Máximo {item[1]})".center(largura_terminal))
            quantidade = input(f"{Style.BRIGHT + Fore.MAGENTA}>>> ")
            if not quantidade.isdigit():
              limpar_terminal()
              print("\n\n\n\n\n\n")
              print(Style.BRIGHT + Fore.RED + "Quantidade inválida. Tente novamente.".center(largura_terminal))
              time.sleep(2)
              continue
            quantidade = int(quantidade)
            if quantidade < 1 or quantidade > item[1]:
              limpar_terminal()
              print("\n\n\n\n\n\n")
              print(Style.BRIGHT + Fore.RED + "Quantidade inválida. Tente novamente.".center(largura_terminal))
              time.sleep(2)
              continue
            else:
              limpar_terminal()
              cabecalho(nickname)
              print("\n\n\n\n")
              print(f"{Style.BRIGHT + Fore.YELLOW}Removendo {quantidade} unidades de [{item[0]}] do Moonlighter....".center(largura_terminal))
              time.sleep(2)
              removerItemMoonlighter(nickname, item[3], quantidade, item[5])
              limpar_terminal()
              cabecalho(nickname)
              print("\n\n\n\n")
              print(f"{Style.BRIGHT + Fore.YELLOW}Item removido com sucesso!".center(largura_terminal))
              time.sleep(2)
              continue
          else:
            limpar_terminal()
            cabecalho(nickname)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT + Fore.YELLOW}Removendo [{item[0]}] do Moonlighter....".center(largura_terminal))
            time.sleep(2)
            removerItemMoonlighter(nickname, item[3], item[1], item[5])
            limpar_terminal()
            cabecalho(nickname)
            print("\n\n\n\n")
            print(f"{Style.BRIGHT + Fore.YELLOW}Item removido com sucesso!".center(largura_terminal))
            time.sleep(2)
            continue
      elif int(opcao) == 3:
        limpar_terminal()
        continue
    elif int(opcao) == 2:
      dadosMundo = obterDadosMundo(nickname)
      if dadosMundo[2] == "Noite":
        limpar_terminal()
        cabecalho(nickname)
        print("\n\n\n\n")
        print(f"{Style.BRIGHT + Fore.RED}Você não pode abrir o Moonlighter durante a noite!".center(largura_terminal))
        time.sleep(2)
        continue
      else:
        limpar_terminal()
        cabecalho(nickname)
        print("\n\n\n\n")
        print(f"{Style.BRIGHT + Fore.YELLOW}Abrindo o Moonlighter para Vendas....".center(largura_terminal))
        time.sleep(2)
        venderItens(nickname)
        limpar_terminal()
        cabecalho(nickname)
        print("\n\n\n\n")
        print(f"{Style.BRIGHT + Fore.YELLOW}Seus Itens foram Vendidos!".center(largura_terminal))
        time.sleep(2)
        limpar_terminal()
        cabecalho(nickname)
        print(f"{Style.BRIGHT + Fore.YELLOW}Você ficou o dia inteiro vendendo seus itens. Já anoiteceu!".center(largura_terminal))
        time.sleep(2)
        limpar_terminal()
        continue
    elif int(opcao) == 3:
      mudarLocalizacaoJogador(nickname, "Quarto")
      return "Quarto"
    elif int(opcao) == 4:
      atualizarParaLocalAnterior(nickname)
      return "Sair"


def mainMoonlighter(nickname, opcao):
  limpar_terminal()
  init(autoreset=True)

  while True:
    if opcao == "Quarto":
      opcao = quarto(nickname)
    elif opcao == "Salao de Exposição":
      opcao = sala_exposicao(nickname)
    elif opcao == "Sair":
      break
    else:
      limpar_terminal()
      print(Style.BRIGHT + Fore.RED + "Opção inválida. Tente novamente.".center(largura_terminal))
      time.sleep(2)
      break
  
  return