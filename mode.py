import os
import sys

import pretty_print
import tools


def monitor(interface):
    os.system("sudo ifconfig " + interface + " down")
    os.system("sudo iwconfig " + interface + " mode monitor")
    os.system("sudo ifconfig " + interface + " up")


def manage(interface):
    os.system("sudo ifconfig " + interface + " down")
    os.system("sudo iwconfig " + interface + " mode manage")
    os.system("sudo ifconfig " + interface + " up")


if __name__ == "__main__":

    interface = None
    mode = 'managed'

    args = sys.argv
    if len(args) > 3:
        print("Usage: sudo python3 mode.py <NIC> <monitor/managed>")
    elif len(args) == 3:
        interface = args[1]
        mode = args[2]
    elif len(args) == 2:
        nics = tools.nics_from_ifconfig()
        if args[1] in nics:
            interface = args[1]
        else:
            mode = args[1]

    if not ('managed' in mode or 'monitor' in mode):
        print("Usage: sudo python3 mode.py <NIC> <monitor/managed>")
        exit(1)
    if interface is None:
        interface = tools.choose_interface(f'\nWhich network interface would you like to put in \'{mode}\' mode?')

    if 'monitor' in mode:
        monitor(interface)
    elif 'managed' in mode:
        manage(interface)

    print(f'{interface} is now in \'{mode}\' mode!')

