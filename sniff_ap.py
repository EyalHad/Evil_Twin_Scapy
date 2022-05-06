from socket import timeout
from scapy.all import *
from multiprocessing import Process

import pandas
import time
import os


AP_LIST = []
ESSID = 0
BSSID = 1
CHANNEL = 2

BSSID_SET = []

stop_event = threading.Event()




# initialize the networks dataframe that will contain all access points nearby
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Password"])
# set the index BSSID (MAC address of the AP)
networks.set_index("BSSID", inplace=True)

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        # get the name of it
        ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
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
        
        networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)
        if bssid not in BSSID_SET:
            BSSID_SET.append(bssid)
            AP_LIST.append([ssid,bssid,channel])


def print_all():
    while not stop_event.is_set():
        os.system("clear")
        print(networks)
        time.sleep(0.5)


def change_channel():
    ch = 1
    while not stop_event.is_set():
        os.system(f"iwconfig {interface} channel {ch}")
        # switch channel from 1 to 14 each 0.5s
        ch = ch % 14 + 1
        if ch == 1 or ch == 6 or ch == 11:
            time.sleep(0.2)
        time.sleep(0.2)


def start():

    # interface name, check using iwconfig
    interface = "wlo1"
    # start the thread that prints all the networks
    printer = Thread(target=print_all, args=(stop_event))
    printer.daemon = True
    printer.start()
    
    # start the channel changer
    channel_changer = Thread(target=change_channel, args=(stop_event))
    channel_changer.daemon = True
    channel_changer.start()
    
    
    
    
    # start sniffing
    sniff(prn=callback, iface=interface, timeout=10)
    
    time.sleep(10)
    stop_event.set()