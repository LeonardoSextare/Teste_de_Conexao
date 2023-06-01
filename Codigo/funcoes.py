import wmi

def obter_Driver_Rede():
    redes = wmi.WMI()
    for rede in redes.Win32_NetworkAdapter():
        if rede.NetConnectionStatus == 2:
            return str(rede.Name)