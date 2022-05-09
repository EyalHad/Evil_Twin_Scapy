from socket import timeout
from scapy.all import *
from multiprocessing import Process

import sys, os, signal
from multiprocessing import Process

import pandas
import time
import os

beacons_count = {}
AP_LIST = []
ESSID = 0
BSSID = 1
CHANNEL = 2

BSSID_SET = []

flag = ""
interface = ""

# initialize the networks dataframe that will contain all access points nearby
networks = pandas.DataFrame(columns=["SSID", "BSSID", "Password","Beacons", "Channel"])
# set the index BSSID (MAC address of the AP)
networks.set_index("SSID", inplace=True)

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr3
        if bssid not in BSSID_SET:
            beacons_count[bssid] = 1
        else:
            beacons_count[packet[Dot11].addr3] = beacons_count[packet[Dot11].addr3] + 1
        # get the name of it
        ssid = packet[Dot11Elt].info.decode()

        # extract network stats
        # stats = packet[Dot11Elt].network_stats()
        # get the channel of the AP
        channel = int( ord(packet[Dot11Elt:3].info))
        # get the crypto
        crypto = packet.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                {Dot11ProbeResp:%Dot11ProbeResp.cap%}")
        if re.search("privacy",crypto):
            crypto = "YES"
        else:
            crypto = "NO"
        
        networks.loc[ssid] = (bssid, crypto, beacons_count[bssid], channel)
        if bssid not in BSSID_SET:
            BSSID_SET.append(bssid)
            AP_LIST.append([ssid,bssid,channel])



def print_all():
    while True:
        if flag:
            break
        try:
            os.system("clear")
            print(networks)
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            break


def change_channel():
    ch = 1
    while True:
        if flag:
            break    
        try:
            os.system(f"iwconfig {interface} channel {ch}")
            # switch channel from 1 to 14 each 0.5s
            ch = ch % 13 + 1
            if ch == 1 or ch == 6 or ch == 11:
                time.sleep(0.2)
            time.sleep(0.2)
        
        except KeyboardInterrupt:
            break


def start(nic_card):
    
    
    global interface
    # interface name, check using iwconfig
    interface = nic_card
    
    # start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    
    # start the channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
    
    time_to_sniff = 15
    
    
    # start sniffing
    sniff(prn=callback, iface=interface, timeout=time_to_sniff)
    
    time.sleep(time_to_sniff)
    global flag
    flag = True
