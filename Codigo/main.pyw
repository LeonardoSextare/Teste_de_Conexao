import subprocess as cmd
import re
import sys
import socket
import datetime
import funcoes
import argparse

# Recebimento de argumentos na execução do script
argumentos = argparse.ArgumentParser()
argumentos.add_argument('--servidor', type=str, help='Servidor Destino', default='18103')
args = argumentos.parse_args()

# Captura informações da máquina utilizadas pelo programa
NOME_MAQUINA = socket.gethostname()
IP_MAQUINA = socket.gethostbyname(socket.gethostname())
DRIVER = funcoes.obter_Driver_Rede()
HORA = datetime.datetime.now().time().strftime("%H:%M:%S")
DATA = datetime.date.today().strftime("%d/%m/%Y")

# Informações para execução do programa
executavel = 'Sources\\speedtest.exe'
servidor = args.servidor
print(servidor)
argumentos_speedtest = ['--accept-license', '--accept-gdpr', f'--server-id={servidor}']

# Verifica se está sendo executado pelo arquivo binario (gerado pelo Pyinstaller) ou pelo interpretador do Python
try:
    executavel = sys._MEIPASS + '\\speedtest.exe'
    modo_script = False
except:
    print('Iniciado em modo script')
    modo_script = True

# Programa Principal
tentativas = 0
while tentativas <= 3:
    tentativas += 1
    # Inicia o 'speedtest.exe' e captura sua saida.
    try:
        print('Executando teste...\n')
        speedtest = cmd.run(args=argumentos_speedtest, executable=executavel, capture_output=True,
                             text=True, check=True, creationflags=cmd.CREATE_NO_WINDOW)
        saida = speedtest.stdout

    except FileNotFoundError:
        print('speedtest.exe não encontrado')
        break

    except cmd.CalledProcessError as error: 
        # Codigo de retorno 2, significa que ocorreu um erro na comunicação.
        if error.returncode == 2: 
            print('Falha durante o teste, tentando novamente...')
            continue
        
        print(f'ERRO! Codigo {error.returncode}')
        print(f'Erro: {error.stderr}')
        print(f'Saida: {error.stdout}')
        break
        
    except Exception as error:
        print('Erro desconhecido ao iniciar "speedtest.exe"')
        print(error.__class__)
        break

    # Fltro das informações utilizando REGEX
    dados = {}
    capturar_dados = {'imagem': r'Result URL:\s*(\S+)',
                      'provedor': r'ISP:\s+(.+)\n',
                      'servidor': r'Server:\s+(.+)\n',
                      'download': r'Download:\s+([\d.]+)\s+Mbps',
                      'upload': r'Upload:\s+([\d.]+)\s+Mbps',
                      'ping': r'Idle Latency:\s+([\d.]+)\s+ms',
                      'packet_loss': r'Packet Loss:\s+([\d.]+)' + '%'}
    
    # Coloca os valores obtidos pela expressão regex em um dicionario
    try:
        for chave, valor in capturar_dados.items():
            dados[chave] = re.search(valor, saida).group(1)

    except AttributeError:
        # Caso entre nessa exceção significa que:
        # O teste foi interrompido ou não foi executado até o final, portanto as expressões não conseguiram localizar todos os dados.
        # Em seguida ele testa qual informação não foi encontrada e alerta o usuario.

        # Se a chave "imagem" não for encontrada em "dados", significa que teste não foi executado com sucesso.
        # Logo não é preciso testar o restante.
        if 'imagem' not in dados:
            print('Falha durante o teste, tentando novamente...')
            continue
        
        # Se o teste foi finalizado e alguma informaçao esteja faltando, completa o dict com o valor 'Erro'
        # Nota: Normalmente o problema é o "packet_loss".
        for chave in capturar_dados.keys():
            if chave not in dados:
                dados[chave] = 'Erro'

    except Exception as error:
        print('Erro desconhecido ao obter as informações')
        print(error.__class__)
        break

    resultado = f'Resultado do Teste:\
            \n============================================\
            \n Maquina: {NOME_MAQUINA} ({IP_MAQUINA})\
            \n Driver: {DRIVER}\
            \n Horario: {DATA} - {HORA}\
            \n Provedor Interno: {dados["provedor"]} \
            \n Servidor Destino: {dados["servidor"]} \
            \n Latencia: {dados["ping"]} ms \
            \n Download: {dados["download"]} Mbps\
            \n Upload: {dados["upload"]} Mbps\
            \n Packet Loss: {dados["packet_loss"]}\
            \n Imagem: {dados["imagem"] + ".png"}'
    
    print(resultado)
    break

else: # Se o número de tentativas chegar a 3, irá cair nesse bloco.
    print('\nNúmero de tentativas excedido., encerrando o programa...')
    input('\nPressione Enter para sair...') if modo_script else None
    exit()


funcoes.enviar_Mensagem(resultado)
input('\nPressione Enter para sair...') if modo_script else None
