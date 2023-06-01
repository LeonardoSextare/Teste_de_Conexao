import os
import shutil
import sys
import subprocess as sub

CAMINHO_PROGRAMA = 'C:\\Program Files\\Teste de Conexao'
CAMINHO_TEMP = sys._MEIPASS
CMD_TAREFA = ['schtasks', '/Create', '/TN', 'Testar Conexao', '/XML', f'{CAMINHO_TEMP}\\Testar_Conexao.xml', '/RU', 'SYSTEM']


def encerrar_programa():
    input('\nPressione Enter para sair')
    exit()

try:
    # Cria Pasta e copia o programa
    print('Extraindo arquivos...')
    os.makedirs(CAMINHO_PROGRAMA, exist_ok=True)
    shutil.copy(f'{CAMINHO_TEMP}\\Testar_Conexao.exe', CAMINHO_PROGRAMA)
    print('OK')
    
except Exception as error:
    print('Ocorreu um erro ao copiar os arquivos')
    print(error.__class__)
    encerrar_programa()

try:
    print('Agendando Tarefa...')
    sub.run(CMD_TAREFA, check=True)

except sub.CalledProcessError as error:
    print('Ocorreu um erro ao agendar a tarefa')
    print(error.__class__)

except Exception as error:
    print('Ocorreu um erro ao agendar a tarefa')
    print(error.__class__)

encerrar_programa()



