import sniff_ap as sniffAP

import sniff_clients as sniffCL



if __name__ == '__main__':
    sniffAP.start()
    print("    \n\n\n    ")
    for i in range(len(sniffAP.AP_LIST)):
        print("index [{0}] -> {1}".format(i, sniffAP.AP_LIST[i]))
        
    index = input("Choooseee")
    
    sniffCL.start(sniffAP.AP_LIST[index][sniffAP.BSSID],sniffAP.AP_LIST[index][sniffAP.CHANNEL])
    