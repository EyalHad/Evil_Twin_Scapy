from scapy.all import *
from scapy.layers.dot11 import Dot11Deauth
import os
import signal
# import subprocess
from threading import Thread

import pretty_print
import tools

DEV_NULL = ">/dev/null 2>&1"  # Discard output


def print_packet(pkt):
    if pkt.haslayer():
        print(pkt)



if __name__ == "__main__":
    os.system('clear')
    # print("===============================================")
    # print("==== Deauthentication Counter Measure Tool ====")
    # print("===============================================")

    # Reset network settings
    os.system(f'python3 reset_network_settings.py -y')

    # Run Deauthentication tool in a separate terminal
    os.system('gnome-terminal -- sh -c "python3 defence.py"')

    # Ask the user to reset network settings
    os.system(f'python3 reset_network_settings.py')

    exit(0)