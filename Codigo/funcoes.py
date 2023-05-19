from pymsteams import *
import wmi


def enviar_Mensagem(mensagem):
    # Webhook teams
    teams = connectorcard("Webhook Teams")

    teams.text(mensagem)
    try:
        teams.send()
    except Exception as error:
        print('Erro ao enviar notificação no Teams')
        print(error.__class__)



def obter_Driver_Rede():
    redes = wmi.WMI()
    for rede in redes.Win32_NetworkAdapter():
        if rede.NetConnectionStatus == 2:
            return str(rede.Name)
