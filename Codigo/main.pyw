from configs import *
from funcoes import *
import subprocess as cmd
import re
import sys
import socket
import datetime

# Configurações iniciais das bibliotecas
logger = configurar_logger()
args = configurar_argumentos()
teams = configurar_msteams()

# Parametros do filtro de envio de relatorio
PARAMETRO_BANDA = 0.20  # Valor entre 0 e 1
UP_MIN = args.upload - (args.upload * PARAMETRO_BANDA)
UP_MAX = args.upload + (args.upload * PARAMETRO_BANDA)
DOWN_MIN = args.download - (args.upload * PARAMETRO_BANDA)
DOWN_MAX = args.download + (args.upload * PARAMETRO_BANDA)
PING_MIN = args.latencia
PERDA_PACOTE_MIN = args.pacote

# Captura informações da máquina utilizadas pelo programa
NOME_MAQUINA = socket.gethostname()
IP_MAQUINA = socket.gethostbyname(socket.gethostname())
REDE_ATIVA = ...
DRIVER = obter_Driver_Rede()
HORA = datetime.datetime.now().time().strftime("%H:%M:%S")
DATA = datetime.date.today().strftime("%d/%m/%Y")

# Informações para execução do programa
caminho_executavel = 'Sources\\speedtest.exe'
argumentos_speedtest = ['--accept-license', '--accept-gdpr', 
                        f'--server-id={args.servidor}']

# Verifica se está sendo executado pelo arquivo binario (gerado pelo Pyinstaller) ou pelo interpretador do Python
try:
    caminho_executavel = sys._MEIPASS + '\\speedtest.exe'
    modo_script = False
except:
    logger.info('Iniciado em modo script')
    modo_script = True


# Programa Principal
tentativas = 0
while tentativas <= 3:
    tentativas += 1
    # Inicia o 'speedtest.exe' e captura sua saida.
    try:
        logger.info('Executando teste...\n')
        speedtest = cmd.run([caminho_executavel, *argumentos_speedtest], capture_output=True,
                            text=True, check=True, creationflags=cmd.CREATE_NO_WINDOW)

        saida = speedtest.stdout

    except FileNotFoundError:
        logger.critical('speedtest.exe não encontrado')
        break

    except cmd.CalledProcessError as error:
        # Codigo de retorno 2, significa que ocorreu um erro na comunicação.
        if error.returncode == 2:
            logger.warning('Erro! Falha na comunicacao, tentando novamente...')
            continue

        logger.error(f'ERRO! Codigo {error.returncode}')
        logger.error(f'Erro: {error.stderr}')
        logger.error(f'Saida: {error.stdout}')
        continue

    except Exception as error:
        logger.critical('Erro desconhecido ao iniciar "speedtest.exe"')
        logger.critical(error.__class__)

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

    # Coloca os valores obtidos pela expressão regex em um dicionario e já converte os números em float
    try:
        for chave, valor in capturar_dados.items():
            dados[chave] = re.search(valor, saida).group(1)

            try:
                dados[chave] = float(dados[chave])
            except Exception as error:
                logger.warning(f'Erro ao converter valor para float: {chave}')

    except AttributeError:
        # Caso entre nessa exceção significa que:
        # O teste foi interrompido ou não foi executado até o final, portanto as expressões não conseguiram localizar todos os dados.
        # Em seguida ele testa qual informação não foi encontrada e alerta o usuario.

        # Se a chave "imagem" não for encontrada em "dados", significa que teste não foi executado com sucesso.
        # Logo não é preciso testar o restante.
        if 'imagem' not in dados:
            logger.warning('Imagem nao foi gerada, tentando novamente...')
            continue

        # Se o teste foi finalizado e alguma informaçao esteja faltando, completa o dict com o valor 'Erro'
        # Nota: Normalmente o problema é o "packet_loss".
        for chave in capturar_dados.keys():
            if chave not in dados:
                dados[chave] = 'Erro'

    except Exception as error:
        logger.critical('Erro desconhecido ao obter as informações')
        logger.errcriticalor(error.__class__)
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

    logger.info(resultado)

    # Filtro
    enviar_relatorio = False
    modo_debug = args.debug
    problemas = []

    if modo_debug:
        logger.info('Modo debug ativado!')
        resultado += '\n\n!!Executado pelo colaborador!!'
        teams.text(resultado)

        try:
            logger.info('Enviando relatorio para o teams...')
            teams.send()
            logger.info('Enviando com sucesso...')

        except Exception as error:
            logger.error('Erro desconhecido ao enviar relatorio para o Teams')
            logger.error(f'{error.__class__}')

    else:
        if not (UP_MIN <= dados['upload'] <= UP_MAX):
            logger.warning('Problemas com Upload!')
            problemas.append('Upload')
            enviar_relatorio = True

        if not (DOWN_MIN <= dados['download'] <= DOWN_MAX):
            logger.warning('Problemas com Download!')
            problemas.append('Download')
            enviar_relatorio = True

        if dados['ping'] >= PING_MIN:
            logger.warning('Problemas com Latencia!')
            problemas.append('Ping')
            enviar_relatorio = True

        if dados['packet_loss'] != 'Erro' and dados['packet_loss'] >= PERDA_PACOTE_MIN:
            logger.warning('Problemas com Perda de Pacotes!')
            problemas.append('Perda de Pacotes')
            enviar_relatorio = True

        if enviar_relatorio:
            mensagem_extra = '\n\nProblemas identificados: '

            for indice, itens in enumerate(problemas):
                if indice == len(problemas) - 1:
                    mensagem_extra += f'{itens}.'
                else:
                    mensagem_extra += f'{itens}, '

            resultado += mensagem_extra
            teams.text(resultado)

        else:
            logger.info(
                'Internet estavel, armazenando logs apenas na máquina.')
        try:
            logger.info('Enviando relatorio para o teams...')
            teams.send()
            logger.info('Enviando com sucesso...')

        except Exception as error:
            logger.error('Erro desconhecido ao enviar relatorio para o Teams')
            logger.error(f'{error.__class__}')

    input('\nPressione Enter para sair...') if modo_script else None
    break

else:  # Se o número de tentativas chegar a 3, irá cair nesse bloco.
    logger.error('\nNúmero de tentativas excedido., encerrando o programa...')
    input('\nPressione Enter para sair...') if modo_script else None
    exit() if modo_script else None
