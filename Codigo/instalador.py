import os
import shutil
import sys
import subprocess


try:
    os.makedirs('C:\\Program Files\\Teste de Conexao', exist_ok=True)
    shutil.copy(sys._MEIPASS + '\\Testar_Conexao.exe',
                'C:\\Program Files\\Teste de Conexao')

except Exception as error:
    print('Ocorreu um erro ao copiar os arquivos')
    print(error.__class__)
    input('Pressione Enter para sair')
    exit()

try:
    subprocess.run(['schtasks', '/Create', '/TN', 'Testar Conexao',
                    '/XML', 'Testar_Conexao.xml', '/RU', 'SYSTEM'],
                   check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
except subprocess.CalledProcessError as error:
    if error.returncode == 1:
        print('Tarefa já existe. OK')
    else:
        print('Ocorreu um erro ao agendar a tarefa')
        print(error.__class__)

    input('Pressione Enter para sair')
    exit()

except Exception as error:
    print('Ocorreu um erro ao agendar a tarefa')
    print(error.__class__)
    input('Pressione Enter para sair')
    exit()
