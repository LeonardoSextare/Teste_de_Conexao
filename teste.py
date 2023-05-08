lista = {'imagem': r'Result URL:\s*(\S+)',
                 'provedor': r'ISP:\s+(.+)\n',
                 'servidor': r'Server:\s+(.+)\n',
                 'download': r'Download:\s+([\d.]+)\s+Mbps',
                 'upload': r'Upload:\s+([\d.]+)\s+Mbps',
                 'ping': r'Idle Latency:\s+([\d.]+)\s+ms',
                 'packet_loss': r'Packet Loss:\s+([\d.]+)%'}

for item in lista:
    variavel = item * 2
    # aqui o escopo da variável "variavel" se limita ao loop for
    print(item)

for c in range(5):
    print(c)

print(c)