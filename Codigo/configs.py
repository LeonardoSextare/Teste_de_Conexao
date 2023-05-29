import logging
from logging.handlers import TimedRotatingFileHandler
import os
import argparse
import pymsteams

WEBHOOK_TEAMS = 'https://precisaosistemas.webhook.office.com/webhookb2/e17c48a8-fd56-46ff-af5a-7d9e51eba43f@c31a0c79-c82f-45d6-abed-6a70879752ab/IncomingWebhook/a148630931c34fde8f972eae3e64ef69/a1b7af53-97cf-4af9-995a-4e6742682947'

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
    argumentos.add_argument('--servidor', type=str, help='Servidor Destino', default='18103')

    return argumentos.parse_args()

def configurar_msteams():
    teams = pymsteams.connectorcard(WEBHOOK_TEAMS)
    return teams