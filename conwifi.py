import os
import time



# Run this program to monitor the change of freaquency
# See if the the channel is actually set\change on the chosen interface
while True:
    os.system("iwconfig")
    time.sleep(0.5)