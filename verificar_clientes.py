import pandas as pd
import subprocess
import os
import time
import re

# Função para verificar o status do IP e obter o tempo de resposta
def verificar_ip(ip):
    try:
        response = subprocess.run(
            ['ping', '-n', '1', '-w', '1000', ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Verifica se a resposta contém "tempo=xxms"
        if response.returncode == 0 and "tempo=" in response.stdout:
            tempos = re.findall(r'tempo=(\d+)ms', response.stdout)
            if tempos:
                media_tempo = sum(int(t) for t in tempos) // len(tempos)
                return True, f"{media_tempo}ms"
        
        # Se não receber "tempo=xxms", considera offline
        return False, "-"
    except Exception as e:
        print(f"Erro ao tentar pingar {ip}: {e}")
        return False, "-"

# Função para ajustar o tamanho da janela do terminal (Windows)
def ajustar_janela_terminal(largura, altura):
    os.system(f'mode con: cols={largura} lines={altura}')

# Função para limpar a tela
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para exibir o logotipo e o menu inicial
def mostrar_interface_inicializacao():
    mensagem_boas_vindas = "\n \n \033[1;31m ██████╗ ██╗███╗   ██╗ ██████╗ ██╗    ██╗██╗███╗   ██╗\n" \
                           "  ██╔══██╗██║████╗  ██║██╔════╝ ██║    ██║██║████╗  ██║\n" \
                           "  ██████╔╝██║██╔██╗ ██║██║  ███╗██║ █╗ ██║██║██╔██╗ ██║\n" \
                           "  ██╔═══╝ ██║██║╚██╗██║██║   ██║██║███╗██║██║██║╚██╗██║\n" \
                           "  ██║     ██║██║ ╚████║╚██████╔╝╚███╔███╔╝██║██║ ╚████║\n" \
                           "  ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝\n" \
                           "       \033[1;36m--= By: Ícaro Lopes | Pinguim.py =--\033[0m"
    
    limpar_tela()
    print(mensagem_boas_vindas)

    print("\n\033[1;34m+-------------------------------------------------------+")
    print("+\t\033[1;32mSelecione uma opção de abaixo\t\t+")
    print("\033[1;34m+-------------------------------------------------------+")
    time.sleep(0.3)
    print("+ \033[1;33m[1] \033[1;37mIniciar Monitoramento de IPs\033[1;34m                      +")
    print("+ \033[1;33m[2] \033[1;37mConfigurar Intervalo de Ping\033[1;34m                      +")
    print("+ \033[1;33m[3] \033[1;37mVisualizar Log de Erros\033[1;34m                           +")
    print("+ \033[1;33m[4] \033[1;37mSair\033[1;34m                                              +")
    print("+-------------------------------------------------------+\033[0m")

    opcao = input("\n\033[1;32m[#] Escolha uma opção: \033[0m")
    return opcao

# Função para configurar intervalo de ping
def configurar_intervalo_ping():
    intervalo = input("\033[1;33m[#] Digite o intervalo de ping em segundos: \033[0m")
    try:
        intervalo = int(intervalo)
        print(f"\033[1;32mIntervalo de ping configurado para {intervalo} segundos.\033[0m")
        time.sleep(2)
    except ValueError:
        print("\033[1;31mIntervalo inválido. Tente novamente.\033[0m")
        time.sleep(2)
        configurar_intervalo_ping()
    return intervalo

# Função para visualizar log de erros (simulação)
def visualizar_log_erros():
    print("\033[1;33m[!] Exibindo log de erros...\033[0m")
    print("\033[1;37mNenhum erro registrado até o momento.\033[0m")
    time.sleep(3)

# Função principal que carrega o arquivo e verifica os IPs
def verificar_clientes():
    df = pd.read_excel('clientes.xlsx')
    
    # Inicializando o status_tracker para rastrear falhas de conexão
    status_tracker = {ip: {"count": 0, "last_status": "ONLINE"} for ip in df['IP']}
    
    # Calcula a largura do nome com base no maior nome presente
    largura_nome = df['Nome'].apply(len).max() + 2  # Adiciona 2 para uma margem extra
    largura_porta = 8
    largura_status = 24
    largura_tempo = 10
    
    largura_total = largura_nome + largura_porta + largura_status + largura_tempo + 9

    while True:
        limpar_tela()

        print(f"+{'-' * largura_total}+")
        print(f"| {'Nome'.center(largura_nome)} | {'Porta'.center(largura_porta)} | {'Status'.center(largura_status)} | {'Tempo'.center(largura_tempo)} |")
        print(f"+{'-' * largura_total}+")
        
        for index, row in df.iterrows():
            nome_cliente = row['Nome']
            ip_cliente = row['IP']
            porta_cliente = str(row['Porta'])

            online, tempo_resposta = verificar_ip(ip_cliente)
            status = "ONLINE" if online else "OFFLINE"

            # Atualizar status e contagem de falhas
            if online:
                status_tracker[ip_cliente]["count"] = 0
                status_tracker[ip_cliente]["last_status"] = "ONLINE"
            else:
                status_tracker[ip_cliente]["count"] += 1
                if status_tracker[ip_cliente]["count"] >= 10:
                    status_tracker[ip_cliente]["last_status"] = "OFFLINE_RECENTE"

            # Determinar a cor com base no status e contagem
            if online:
                cor_status = "\033[1;32m"  # Verde
            elif status_tracker[ip_cliente]["count"] < 10 and not online:
                cor_status = "\033[1;33m"  # Amarelo
            else:
                cor_status = "\033[1;31m"  # Vermelho
                print("\a")  # Beep de alerta

            print(f"| {nome_cliente.ljust(largura_nome)} | {porta_cliente.center(largura_porta)} | {cor_status}{status.center(largura_status)}\033[0m | {tempo_resposta.center(largura_tempo)} |")
        
        print(f"+{'-' * largura_total}+")
        
        time.sleep(3)

# Função para iniciar o programa baseado na escolha do usuário
def iniciar_programa():
    opcao = mostrar_interface_inicializacao()

    if opcao == '1':
        verificar_clientes()
    elif opcao == '2':
        intervalo = configurar_intervalo_ping()
        while True:
            verificar_clientes()
            time.sleep(intervalo)
    elif opcao == '3':
        visualizar_log_erros()
        iniciar_programa()
    elif opcao == '4':
        print("\033[1;31mSaindo...\033[0m")
        time.sleep(1)
        exit()
    else:
        print("\033[1;31mOpção inválida. Tente novamente.\033[0m")
        time.sleep(2)
        iniciar_programa()

# Inicia o programa com o menu inicial
iniciar_programa()
