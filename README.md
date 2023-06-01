![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=flat)
![Badge em Desenvolvimento](https://img.shields.io/badge/Python-v3.11-blue)

#  🌐 Teste de Conexão
O objetivo principal é monitorar a velocidade e qualidade da conexão com a internet e caso necessario, solicitar suporte.


## Como Usar
Ao executar o programa, não irá exibir nenhuma janela e irá gerar uma pasta com o nome "logs" com arquivos contendo os resultados do programa.
Os dados também serão enviados pelo Microsoft Teams, caso tenha sido configurado o link do Webhook em [funcoes.py](https://github.com/LeonardoSextare/Teste_de_Conexao/blob/main/Codigo/funcoes.py)


É possivel passar alguns parametros para o programa ao executar diretamente pelo terminal.
--servidor (ID_servidor) - Define um servidor de destino diferente do padrão. 
--download (Mbps) - Define a velocidade média de download em Mbps para usar como criterio para envio de notificação.
--upload (Mbps) - Define a velocidade média de upload em Mbps para usar como criterio para envio de notificação.
--latencia (ms) - Define a latencia máxima em milisegundos para usar como criterio para envio de notificação.
--pacote (%) - Define a perda de pacotes máxima em porcetagem para usar como criterio para envio de notificação.
--debug - Quando presente envia o resultado ignorando todos os criterios estabelecidos para notificação.

Exemplo: Testar_Conexao.exe --servidor 123456 --download 80 --upload 50 --latencia 80 --pacote 10

[Como obter o ID do servidor](https://www.dcmembers.com/skwire/how-to-find-a-speedtest-net-server-id/)

## Como Compilar
- Instalar todas as [bibliotecas](https://github.com/LeonardoSextare/Teste_de_Conexao/edit/main/README.md#bibliotecas-utilizadas)
- Instalar a biblioteca [pyinstaller](https://pypi.org/project/pyinstaller/)
- Executar o arquivo Compilar.bat


Irá ser gerado o arquivo executavel com o nome "Testar_Conexao.exe".


## Bibliotecas Utilizadas
- subprocess
- re
- sys
- os
- socket
- datetime
- argparse
- pymsteams
- wmi
- logging
- shutil


## Funcionamento e Dados Coletados
Captura os dados da velocidade de conexão com a internet utilizando software Speedtest CLI, armazena em logs na máquina local e se necessario envia uma notificação pelo Microsoft Teams

Captura outras informações da máquina relacionados a conexão.

- Nome do Computador
- Endereço de IP Local
- Driver de Rede Ativo
- Modelo do Computador (Em desenvolvimento)
- Provedor Interno
- Servidor Destino
- Latencia
- Velocidade de Download
- Velocidade de Upload
- Perda de Pacotes


