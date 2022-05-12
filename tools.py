import os
import sys

import pretty_print
# import tools


def monitor(interface):
    os.system("sudo ifconfig " + interface + " down")
    os.system("sudo iwconfig " + interface + " mode monitor")
    os.system("sudo ifconfig " + interface + " up")
    print(f'{interface} is now in mode monitor')


def manage(interface):
    os.system("sudo ifconfig " + interface + " down")
    os.system("sudo iwconfig " + interface + " mode manage")
    os.system("sudo ifconfig " + interface + " up")
    print(f'{interface} is now in mode managed')


def nics_from_ifconfig():
    """Execute ifconfig and return a list of all NIC's found"""
    tmp_out = 'ifcfg.txt'
    os.system(f'iwconfig > {tmp_out}')
    nics_found = []
    with open(tmp_out, 'r') as file:
        for line in file.readlines():
            for word in line.split("  "):
                if "wl" in word:
                    nics_found.append(word)
        file.close()
    os.system(f'rm {tmp_out}')
    return nics_found


def in_monitor_mode(iface):
    tmp_out = 'iwcfg.txt'
    os.system(f'iwconfig {iface} > {tmp_out}')
    with open(tmp_out, 'r') as file:
        for line in file.readlines():
            for word in line.split(": "):
                if 'Mode:Managed' in word:
                    return True
                # print(f'word: {word}')
        file.close()
    os.system(f'rm {tmp_out}')
    # return nics_found
    return False


def choose_interface(message=None):
    """Execute ifconfig and wait for user input to choose a network interface from the list"""
    # Choose an interface to be used as an AP

    if message is not None:
        pretty_print.pretty(f'\n{message}\n')
    ifaces = nics_from_ifconfig()
    size = len(ifaces)
    if size == 0:
        pretty_print.pretty('No NIC\'s were found!')
        reset_network_settings()
        print('\nPlease run this command again:')

        pretty_print.pretty(f'\n\tsudo python3 {sys.argv[0]} [Optional <NIC-Name>]')
        exit(2)
    index = -1
    while index > size or index < 0:
        print('\nAvailable Network Interface Cards:')
        for i in range(size):
            print(f'{i + 1}: {ifaces[i]}')
        try:
            index = int(input(f"\nChoose an interface (1-{size}): "))
        except Exception as e:
            print('Invalid input!')
    print()
    return ifaces[index - 1]


def choose_ssid():
    return input('Network SSID:\nPlease choose a name for the fake AP: ')


def reset_network_settings(ask_usr=True):
    if ask_usr:
        x = input(f'Restore network settings? [y/n] ')
        if 'y' not in x:
            return

    os.system('service NetworkManager start')
    os.system('service avahi-daemon start')
    os.system('service wpa_supplicant start')

    NICs = nics_from_ifconfig()
    for nic in NICs:
        os.system(f'sudo python3 mode.py {nic} managed')

    pretty_print.pretty('\nNetwork Settings are back to normal!')

