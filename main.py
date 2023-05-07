from subprocess import *
import os
import re
import sys


TEMP = os.environ['TEMP']

# Define o caminho do programa
# Se executado pelo exe(Pyinstaller), define a pasta _MEIxxxx como caminho.
# Se não, define a pasta onde o programa está sendo executado. (Requer o speedtest.exe no mesmo diretorio)
try:  
    #Executando pelo arquivo binario  
    caminho_programa = sys._MEIPASS + '\\speedtest.exe'
    
except Exception as error:
    #Executando por outras fontes
    caminho_programa = TEMP + '\\speedtest.exe'

# Parametros do speedtest.exe
comando = [caminho_programa, '--accept-license', '--accept-gdpr']

tentativa = 0
while tentativa < 3:
    print('Executando teste de conexão...')
    try:
        #Executa o speedtest.exe e captura a saida do comando para a variavel: resultado
        resultado = run(comando, text=True, capture_output=True, check=True).stdout

    except CalledProcessError as error:
        # Codigo de retorno 2, significa que ocorreu um erro na comunicação.
        if error.returncode == 2:
            print('Falha durante o teste, tentando novamente...')
            tentativa += 1
            continue
        
        # Encerra o programa para qualquer outro codigo diferente de 0
        print(f'Codigo {error.returncode} na execução do comando:')
        print(f'Erro: {error.stderr}')
        print(f'Output:{error.stdout}')
        break

    except Exception as error:
        print('Erro desconhecido a durante a execução do comando:')
        print(error.__class__)
        break

    try:
        # Captura as informações de saida através de expresões regex. ===ESTUDAR MAIS SOBRE===
        provedor = re.search(r'ISP:\s+(.+)\n', resultado).group(1)
        servidor = re.search(r'Server:\s+(.+)\n', resultado).group(1)
        download = re.search(r'Download:\s+([\d.]+)\s+Mbps', resultado).group(1)
        upload = re.search(r'Upload:\s+([\d.]+)\s+Mbps', resultado).group(1)
        ping = re.search(r'Idle Latency:\s+([\d.]+)\s+ms', resultado).group(1)
        packet_loss = re.search(r'Packet Loss:\s+([\d.]+)%', resultado).group(1)
        imagem = re.search(r'Result URL:\s*(\S+)', resultado).group(1)

    except AttributeError:
        # Caso entre nessa exceção significa que:
        # Se caso alguma informação estiver faltando ao definir as variaveis, o programa é executado novamente.
        print('Falha durante o teste, tentando novamente...')
        tentativa += 1
        continue

    except Exception as error:
        print('Erro desconhecido durante o teste')
        print(error.__class__)

    else:
        print(f'\nResultado do Teste:'
        f'\nProvedor Interno: {provedor}'
        f'\nServidor Destino: {servidor}'
        f'\nLatencia: {ping} ms'
        f'\nDownload: {download} Mbps'
        f'\nUpload: {upload} Mbps'
        f'\nPacket Loss: {packet_loss} %'
        f'\nImagem: {imagem}')
        break

if tentativa >= 3:
    print('\nNúmeros de tentativas excedido, execute o programa novamente!')

input('\nPressione Enter para sair...')
