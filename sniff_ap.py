from socket import timeout
from numpy import empty
from scapy.all import *
from scapy.layers.dot11 import *
from multiprocessing import Process

import sys, os, signal
from multiprocessing import Process

import pandas
import time
import os

import mode
import pretty_print
import tools

beacons_count = {}

AP_LIST = []
ESSID = 0
BSSID = 1
CHANNEL = 2

BSSID_SET = []

flag = False
interface = ""

# initialize the networks dataframe that will contain all access points nearby
networks = pandas.DataFrame(columns=["SSID", "BSSID", "Password", "Beacons", "Channel"])
# set the index BSSID (MAC address of the AP)
networks.set_index("SSID", inplace=True)


def callback(packet):
    global AP_LIST, BSSID_SET, beacons_count
    if packet.haslayer(Dot11Beacon):
        try:
            # extract the MAC address of the network
            bssid = packet[Dot11].addr3
            # pretty_print.pretty(f'========== {bssid} ==========')
            if bssid not in BSSID_SET:
                # pretty_print.pretty('Found a 802.11 Packet!')
                beacons_count[bssid] = 1
            else:
                beacons_count[packet[Dot11].addr3] += 1
            # get the name of it
            bytes_encode(packet[Dot11Elt].info)
            # pretty_print.pretty(f'******* About to decode packet: {bssid} *******')
            ssid = packet[Dot11Elt].info.decode()
            # pretty_print.pretty(f'===============================================================')

            # extract network stats
            # stats = packet[Dot11Elt].network_stats()
            # get the channel of the AP
            channel = int(ord(packet[Dot11Elt:3].info))
            # get the crypto
            crypto = packet.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                    {Dot11ProbeResp:%Dot11ProbeResp.cap%}")

            if re.search("privacy", crypto):
                crypto = "YES"
            else:
                crypto = "NO"

            networks.loc[ssid] = (bssid, crypto, beacons_count[bssid], channel)
            if bssid not in BSSID_SET:
                BSSID_SET.append(bssid)
                AP_LIST.append([ssid, bssid, channel])
        except Scapy_Exception as e:
            os.system(f'echo {e} > scapy_errors.txt')
            print('err')
        except IndexError as e:
            os.system(f'echo {e}')
        except Exception as e:
            os.system(f'echo {e}...\nTry rerunning')


def print_all():
    while True:
        if flag:
            break
        try:
            os.system("clear")
            print(networks)
            time.sleep(0.35)

        except Exception as e:
            print(e)
            print('PRINT PROBLEM')



def change_channel():
    ch = 1
    while True:
        if flag:
            break
        try:
            os.system(f"iwconfig {interface} channel {ch}")
            # switch channel from 1 to 14 each 0.5s
            # print(f'channel = {ch}')
            ch = ch % 13 + 1
            if ch == 1 or ch == 6 or ch == 11:
                time.sleep(0.2)
            time.sleep(0.2)

        except Exception as e:
            os.system(f'echo {e} > output2.txt')
            print('CHANNEL PROBLEM')


TIMEOUT = 60


def start(nic_card, time_to_sniff=TIMEOUT):
    global interface
    # interface name, check using iwconfig
    interface = nic_card
    
    os.system("clear")
    pretty_print.pretty(
        "===============================================\n"
        "================= AP Sniffer ==================\n"
        "===============================================\n")
    
    time_to_sniff=int(input(f'Sniffing time (Default {TIMEOUT} sec): '))
    if time_to_sniff is None:
        time_to_sniff = TIMEOUT
    
    
    # start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()

    # start the channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()

    # start sniffing
    sniff(prn=callback, iface=interface, timeout=time_to_sniff)

    time.sleep(time_to_sniff)
    # printer.join(timeout=time_to_sniff)
    global flag
    flag = True


# if __name__ == '__main__':
#     pretty_print.pretty(
#         "===============================================\n"
#         "================= AP Sniffer ==================\n"
#         "===============================================\n")
    
#     args = sys.argv
#     if len(args) > 1:
#         nic = args[1]
#     else:
#         nic = tools.choose_interface()

#     t = Thread(target=lambda: start(nic, time_to_sniff=int(input(f'Sniffing time (Default {TIMEOUT} sec): '))))
#     t.start()
#     os.system(f'echo "SOMETHING!..." > output.txt')
#     t.join(timeout=TIMEOUT)
#     input('Finished Sniffing Access Points!')
#     print(f'Results: {AP_LIST}')

