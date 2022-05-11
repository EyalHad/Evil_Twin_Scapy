import os
# from pretty_print import pretty


def nics_from_ifconfig():
    """Execute ifconfig and return a list of all NIC's found"""
    tmp_out = 'ifcfg.txt'
    os.system(f'ifconfig > {tmp_out}')
    nics_found = []
    with open(tmp_out, 'r') as file:
        for line in file.readlines():
            for word in line.split(": "):
                if "wl" in word:
                    nics_found.append(word)
        file.close()
    os.system(f'rm {tmp_out}')
    return nics_found


def choose_interface():
    """Execute ifconfig and wait for user input to choose a network interface from the list"""
    # Choose an interface to be used as an AP
    ifaces = nics_from_ifconfig()
    size = len(ifaces)
    index = -1
    while index > size or index < 0:
        print('\nAvailable Network Interface Cards:')
        for i in range(size):
            print(f'{i + 1}: {ifaces[i]}')

        index = int(input(f"\nChoose an interface (1-{size}): "))
    print()
    return ifaces[index - 1]


def choose_ssid():
    return input('Network SSID:\nPlease choose a name for the fake AP: ')