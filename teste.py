import socket
import datetime

data = datetime.date.today().strftime("%d/%m/%Y")
print(data)

data_atual = datetime.date.today()
print(data_atual)

# Imprimir a data no formato DD/MM/YYYY
print("Data atual:", data_atual.strftime("%d/%m/%Y"))

# Obter apenas a hora atual
hora_atual = datetime.datetime.now().time()

# Imprimir a hora no formato HH:MM:SS
print("Hora atual:", hora_atual.strftime("%H:%M:%S"))

ip = socket.gethostbyname(socket.gethostname())
nome = socket.gethostname()

print(ip)
print(nome)