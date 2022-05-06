import sniff_ap as sniffAP

import sniff_clients as sniffCL



if __name__ == '__main__':
    sniffAP.start()
    print("    \n\n\n    ")
    for i in range(len(sniffAP.AP_LIST)):
        print("index [{0}] -> {1}".format(i, sniffAP.AP_LIST[i]))
        
    index = int(input("Choose an Access Point to ATTACK -   "))
    
    mac_ap = sniffAP.AP_LIST[index][sniffAP.BSSID]
    channel = sniffAP.AP_LIST[index][sniffAP.CHANNEL]
    
    sniffCL.start(mac_ap, channel)
    
    for i in range(len(sniffCL.CL_LIST)):
        print("index [{0}] -> {1}".format(i, sniffCL.CL_LIST[i]))
    