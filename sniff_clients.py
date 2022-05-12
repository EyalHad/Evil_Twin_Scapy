import pkgutil
from socket import timeout
from struct import pack
from scapy.all import *
from threading import Thread
import pandas
import time
import os

from scapy.layers import *
from scapy.layers.dot11 import *

CL_LIST = []

AP_MAC = ""


def callback(packet):
    global CL_LIST
    
    if not packet.haslayer(Dot11ProbeResp):
        if (packet.addr1 == AP_MAC) or (packet.addr2 == AP_MAC) or (packet.addr3 == AP_MAC):
            if packet.addr1 != AP_MAC and packet.addr1 != "ff:ff:ff:ff:ff:ff" and packet.addr1 != None:
                if packet.addr1 not in CL_LIST:
                    CL_LIST.append(packet.addr1)
                    print("Client Appended...  " + packet.addr1)
            elif packet.addr2 != AP_MAC and packet.addr2 not in CL_LIST and packet.addr2 != None:
                CL_LIST.append(packet.addr2)
                print("Client Appended...  " + packet.addr2)
                
                
                
        # print("Qos")
    
  

        # print("ProbeResp")
        # print(packet.addr1 +"----------------" + packet.addr2 + "--------------" + packet.addr3)       


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



# start("wlx7cc2c607f3a3","a0:a3:f0:d7:0f:be", 6)