import pkgutil
from socket import timeout
from struct import pack
from scapy.all import *
from threading import Thread
import pandas
import time
import os

from scapy import layers


CL_LIST = []

AP_MAC = ""



def callback(packet):
    if (packet.addr2 == AP_MAC or packet.addr3 == AP_MAC) and (packet.addr1 != "ff:ff:ff:ff:ff:ff"):
        if packet.addr1 not in CL_LIST:
            CL_LIST.append(packet.addr1)

            print("Client Added     " + packet.addr1)









def start(ap_mac, channel):
    os.system("clear")
    os.system("sudo iwconfig wlo1 channel %d " %(channel))
    global AP_MAC
    AP_MAC = ap_mac
    
    
    # start sniffing
    print("Sniffing Clients...")
    print("AccessPoint= "+str(ap_mac)+", Channel="+str(channel))
    interface = "wlo1"
    sniff(prn=callback, iface=interface, timeout=10)
