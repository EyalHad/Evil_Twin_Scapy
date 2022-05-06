from socket import timeout
from struct import pack
from scapy.all import *
from threading import Thread
import pandas
import time
import os


CL_LIST = []

AP_MAC = ""




# # initialize the networks dataframe that will contain all access points nearby
# networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Password"])
# # set the index BSSID (MAC address of the AP)
# networks.set_index("BSSID", inplace=True)

def callback(packet):
    if (packet.addr2 == AP_MAC or packet.addr3 == AP_MAC) and (packet.addr1 != "ff:ff:ff:ff:ff:ff"):
        if packet.addr1 not in CL_LIST:
            CL_LIST.append(packet.addr1)
            
            print("added" + packet.addr1)









def start(ap_mac, channel):
    os.system("sudo iwconfig wlo1 channel %d " %(channel))
    AP_MAC = ap_mac
    # start sniffing
    interface = "wlo1"
    sniff(prn=callback, iface=interface, timeout=10)
    # channel_changer._stop()
    # printer._stop()