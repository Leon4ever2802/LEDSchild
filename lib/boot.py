from network import WLAN, STA_IF
from time import sleep

SETTINGS: dict = {
    # WIFI:
    "SSID": "reusch.home.net",
    "Password": "1a2a3a4a5a"
}

if __name__ == '__main__':
    
    # this is an essential print! without, code breaks, sorry!
    print("Trying to connect to WIFI...")

    # activating WI-FI:
    #wfi = WLAN(STA_IF)
    #wfi.active(True)

    # trying to connect till connected:
    #while not wfi.isconnected():
        #try:
            #wfi.connect(SETTINGS["SSID"], SETTINGS["Password"])  # try to connect with the data from 'SETTINGS-dict'

        #except Exception as e:
            #print(f"\033[91mFailed to connect to WIFI. {e} Check the Connections and Settings!\033[0m")
            #sleep(15)  # if something went wrong waiting for 15secs and retrying

    #print(f"\033[92mConnected successfully to WLAN: {wfi.ifconfig()}\033[0m")
    