import logging
from logging.handlers import TimedRotatingFileHandler
import os
import argparse
import pymsteams


WEBHOOK_TEAMS = 'Webhook Teams'


# Configurações para criação de logger
def configurar_logger():
    pasta_logs = 'C:\\Program Files\\Teste de Conexao\\logs'
    # Definindo configurações de geração de logs e criando a pasta logs caso não exista
    if os.path.exists(pasta_logs):
        pass
    else:
        os.makedirs(pasta_logs)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(lineno)d %(levelname)s: %(message)s',
    )

    arquivo_log = TimedRotatingFileHandler(
        f'{pasta_logs}\\teste_conexao.log', when='S', interval=60, backupCount=80)
    arquivo_log.setFormatter(logging.Formatter(
        '%(asctime)s - %(lineno)d %(levelname)s: %(message)s'))

    logger = logging.getLogger()
    logger.addHandler(arquivo_log)

    return logger

# Recebimento de argumentos na execução do script


def configurar_argumentos():
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--servidor', type=str,
                            help='Define um servidor de destino diferente do padrão.', default='18103')
    argumentos.add_argument('--download', type=int,
                            help='Define a velocidade média de download em Mbps para usar como criterio para envio de notificação.', default='100')
    argumentos.add_argument('--upload', type=int,
                            help='Define a velocidade média de upload em Mbps para usar como criterio para envio de notificação.', default='100')
    argumentos.add_argument('--latencia', type=int,
                            help='Define a latencia máxima em milisegundos para usar como criterio para envio de notificação.', default='60')
    argumentos.add_argument('--pacote', type=int,
                            help='Define a perda de pacotes máxima em porcetagem para usar como criterio para envio de notificação.', default='15')
    argumentos.add_argument('--debug', action='store_true',
                            help='Quando presente envia o resultado ignorando todos criterios estabelecidos para notificação.')

    return argumentos.parse_args()


def configurar_msteams():
    teams = pymsteams.connectorcard(WEBHOOK_TEAMS)
    return teams
