# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

from network import WLAN, STA_IF

SETTINGS: dict = {
    # WIFI:
    "SSID": "",
    "Password": ""
}

if __name__ == '__main__':
    
    # this is an essential print! without, code breaks, sorry!
    print("Trying to connect to WIFI...")

    # activating WI-FI:
    global wlan # global so I can dc in the main
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(SETTINGS["SSID"], SETTINGS["Password"])  # try to connect with the data from 'SETTINGS-dict'

    # waiting until device has an IP-Addr and is fully connected
    while not wlan.status() == 3:
        continue
        
    global IP_ADDR # global so I can setup the socket with the given IP_ADDR
    IP_ADDR = wlan.ifconfig()[0]
    print(f"\033[92mConnected successfully to WLAN: {wlan.ifconfig()}\033[0m")
    