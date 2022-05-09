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
    global CL_LIST
    if (packet.addr2 == AP_MAC or packet.addr3 == AP_MAC) and (packet.addr1 != "ff:ff:ff:ff:ff:ff"):
        if packet.addr1 not in CL_LIST:
            if packet.addr2 != packet.addr1 and packet.addr1 != packet.addr3:
                CL_LIST.append(packet.addr1)
                print("Client Added     " + packet.addr1)



def start(nic_card, ap_mac, channel):

    
    os.system("clear")
    os.system("sudo iwconfig %s channel %d " %(nic_card, channel))
    
    print(nic_card)
    
    global AP_MAC
    AP_MAC = ap_mac
    
    # start sniffing
    print("Sniffing Clients...")
    print("AccessPoint= "+str(ap_mac)+", Channel="+str(channel))
    
    sniff(prn=callback, iface=nic_card, timeout=55)



# start("wlo1","a0:a3:f0:d7:0f:be", 6)