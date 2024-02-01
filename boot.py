# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

from network import WLAN, STA_IF
from time import sleep
from machine import reset
from settings import SETTINGS

if __name__ == '__main__':
    
    # this is an essential print! without, code breaks, sorry!
    print("Trying to connect to WLAN...")

    # activating WI-FI:
    global wlan
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(SETTINGS["SSID"], SETTINGS["Password"])  # try to connect with the data from 'SETTINGS-dict'

    # waiting until device has an IP-Addr and is fully connected
    counter = 0
    while not wlan.status() == 3:
        if counter == 5:
            wlan.disconnect()
            break
        sleep(1)
        counter = counter + 1
        continue
    
    if wlan.status() == 3:
        SETTINGS["IP-Addr"] = wlan.ifconfig()[0]
        print(f"\033[92mConnected successfully to WLAN: {wlan.ifconfig()}\033[0m")
    else:
        SETTINGS["IP-Addr"] = ""
        print("Could not connect to WLAN!")
