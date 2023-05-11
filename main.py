from subprocess import *
import pymsteams, os, re, sys, socket, datetime

# Informações da máquina utilizadas pelo programa
TEMP = os.environ['TEMP']
NOME_MAQUINA = socket.gethostname()
IP_MAQUINA = socket.gethostbyname(socket.gethostname())
HORA = datetime.datetime.now().time().strftime("%H:%M:%S")
DATA = datetime.date.today().strftime("%d/%m/%Y")

# Define o caminho do programa
# Se executado pelo exe(Pyinstaller), define a pasta _MEIxxxx como caminho.
# Se não, define a pasta "Sources" onde o programa está sendo executado como caminho. (Requer o speedtest.exe no diretorio)
try:
    # Executando pelo arquivo binario
    caminho_programa = sys._MEIPASS + '\\speedtest.exe'

except Exception as error:
    # Executando por outras fontes
    caminho_programa = 'Sources\\speedtest.exe'

# Parametros do speedtest.exe
comando = [caminho_programa, '--accept-license', '--accept-gdpr', '--server-id=18103']

tentativa = 0
while tentativa < 3:
    print('Executando teste de conexão...\n')
    try:
        # Executa o speedtest.exe e captura a saida do comando para a variavel: resultado
        resultado = run(comando, text=True,
                        capture_output=True, check=True).stdout

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

    # Informações a capturar via regex === ESTUDAR MAIS SOBRE ===
    dados = {}
    capturar_dados = {'imagem': r'Result URL:\s*(\S+)',
             'provedor': r'ISP:\s+(.+)\n',
             'servidor': r'Server:\s+(.+)\n',
             'download': r'Download:\s+([\d.]+)\s+Mbps',
             'upload': r'Upload:\s+([\d.]+)\s+Mbps',
             'ping': r'Idle Latency:\s+([\d.]+)\s+ms',
             'packet_loss': r'Packet Loss:\s+([\d.]+)' + '%'}
    
    try:
        # Captura as informações de saida através de expresões regex. ===ESTUDAR MAIS SOBRE===
        for dado, expressao in capturar_dados.items():
            dados[dado] = re.search(expressao, resultado).group(1)
            
    except AttributeError:
        # Caso entre nessa exceção significa que:
        # O teste foi interrompido ou não foi executado até o final, portanto as expressões não conseguiram localizar todos os dados.
        # Em seguida ele testa qual informação não foi encontrada e alerta o usuario.

        # Se a chave "imagem" não for encontrada em "dados", significa que teste não foi executado completamente.
        # Logo não precisa testar o restante. Então, faz o teste novamente.
        if 'imagem' not in dados:
            print('Falha durante o teste, tentando novamente...')
            tentativa += 1
            continue

        # Caso a imagem exista, significa que o teste foi executado, mas ainda sim alguma informação está em falta.
        # Nota: Normalmente essa informação é o "packet_loss".
        print('Erro ao obter os dados:')
        for chave in capturar_dados.keys():
            if chave not in dados:
                print(chave, end='\n\n')
                dados[chave] = 'Erro'

    except Exception as error:
        print('Erro desconhecido durante o teste')
        print(error.__class__)

    resultado_formatado = f'Resultado do Teste: \
          \nProvedor Interno: {dados["provedor"]} \
          \nServidor Destino: {dados["servidor"]} \
          \nLatencia: {dados["ping"]} ms \
          \nDownload: {dados["download"]} Mbps\
          \nUpload: {dados["upload"]} Mbps\
          \nPacket Loss: {dados["packet_loss"]}\
          \nImagem: {dados["imagem"] + ".png"}'
    
    print(resultado_formatado)
    break

if tentativa >= 3:
    print('\nNúmeros de tentativas excedido, execute o programa novamente!')
    input('\nPressione Enter para sair...')
    exit()

# EM TESTES (FUNCIONAL)
Teams = pymsteams.connectorcard("Webhook teams")

mensagem = f'Maquina: {NOME_MAQUINA} ({IP_MAQUINA})\
            \n {DATA} as {HORA}\
            \n ======================== \
            \n{resultado_formatado}'

Teams.text(mensagem)

try:
    Teams.send()
except Exception as error:
    print(error.__class__)

input('\nPressione Enter para sair...')
