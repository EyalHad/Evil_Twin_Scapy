import os
import sys


interface = sys.argv[1]



def monitor(interface):
    os.system("sudo ifconfig " + interface + " down")
    os.system("sudo iwconfig " + interface + " mode monitor")
    os.system("sudo ifconfig " + interface + " up")
    
    
def manage(interface):
    os.system("sudo ifconfig " + interface + " down")
    os.system("sudo iwconfig " + interface + " mode manage")
    os.system("sudo ifconfig " + interface + " up")
    
    
manage(interface)