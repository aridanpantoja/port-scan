import os
import socket
from time import time
from concurrent.futures import ThreadPoolExecutor

# Cores usadas no Terminal
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# Setup
portasAbertas = [] # Armazena (porta, serviço)
portasFechadas = [] # Armazena apenas o número da porta
numThreads = 50 # Número de Threads (Entre 10 e 50)
portaInicio = 1 # Primeira porta a ser scaneada
portaFim = 512 # Última porta a ser scaneada


def limparTerminal():
    sistema = os.name
    if sistema == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')

def scanPorta(porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.connect((host, porta))
            servico = obterServico(porta)
            portasAbertas.append((porta, servico))
        except:
            portasFechadas.append(porta)

def obterServico(porta):
    try:
        return socket.getservbyport(porta)
    except OSError:
        return "Não identificado"

def exibeTempo(tempo):
    printColorido(YELLOW, f"\nRelatório executado em: {tempo:.2f} segundos\n")

def printColorido(color, texto):
    print(f"{color}{texto}{RESET}")
    

limparTerminal()

print(f"""{GREEN}

             ____            _     ____                  
            |  _ \ ___  _ __| |_  / ___|  ___ __ _ _ __  
            | |_) / _ \| '__| __| \___ \ / __/ _` | '_ \ 
            |  __/ (_) | |  | |_   ___) | (_| (_| | | | |
            |_|   \___/|_|   \__| |____/ \___\__,_|_| |_|
                                                                                          
===================================================================
|                                                                 |
|  Feito por: Ana Beatriz, Aridan Pantoja e Jaqueline Nascimento  | 
|                                                                 |
|  Disponível em: https://www.github.com/aridanpantoja/port-scan  |
|                                                                 |
===================================================================
{RESET}""")

host = input("\nDigite o domínio ou ip do host: ") # Host a ser scaneado
print(f"\nRelatório de portas em {host} ({portaInicio} até {portaFim})\n")

inicioTempo = time() # Inicia contagem do tempo de execução

with ThreadPoolExecutor(max_workers=numThreads) as executor:
    futures = [executor.submit(scanPorta, porta) for porta in range(portaInicio, portaFim + 1)]
    for future in futures:
        result = future.result()

execucaoTempo = time() - inicioTempo # Finaliza contagem do tempo de execução

if (len(portasAbertas) > 0):
    printColorido(GREEN, "O host está online ✔")
    printColorido(RED, f"{len(portasFechadas)} portas fechadas\n")

    # Imprime o cabeçalho da tabela
    print(f"{'PORTA':<15} {'ESTADO':<10}")  
    print("-" * 25)

    # Para cada porta aberta
    for porta, servico in portasAbertas:
        saida = f"{porta}/{servico}" # Cria a saída formatada com porta/servico
        print(f"{saida:<15} {'aberta':<10}")

    exibeTempo(execucaoTempo)

else:
    printColorido(RED, "Host offline ou não encontrado ✕")
    printColorido(RED, "Nenhuma porta aberta ✕")
    exibeTempo(execucaoTempo)