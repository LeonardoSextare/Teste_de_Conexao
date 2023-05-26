import logging
from logging.handlers import TimedRotatingFileHandler
import os
import argparse
import pymsteams

WEBHOOK_TEAMS = 'Seu Webhook Teams'
# Configurações para criação de logger
def configurar_logger():
    # Definindo configurações de geração de logs e criando a pasta logs caso não exista
    if os.path.exists('logs'):
        pass
    else:
        os.makedirs('logs')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(lineno)d %(levelname)s: %(message)s',
    )

    arquivo_log = TimedRotatingFileHandler(
        'logs\\teste_conexao.log', when='S', interval=60, backupCount=80)
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