# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

from lib.leds import Leds
from lib.HCSR04 import HCSR04
from lib.server import Server
from time import sleep

def main() -> None:
    """
    The main function to a "LEDSchild"

    functions:
        - Changing the colors of a LED stripe by fading to a color corresponding to the measured distance of a
        HCSR04 sensor
        - network connection to the raspberry to change color via HTTP-request

    :return: None
    """
try:
    # initialization
    l = Leds(6, 28)
    h = HCSR04(17, 16)
    s = Server(IP_ADDR, 80)

    print("Device listening on Port: " + IP_ADDR)
    s.start()
    
    # changing colors depending on the measured distance from the HCSR04
    while True:
        if s.check_conn_isconnected():
            if s.check_conn():
                color = s.accept_conn()
                if not color == None:
                    if color[:3] == (666, 666, 666):
                        l.rainbow(color[3])
                    l.fade_to(color)
        else:
            if s.check_socket():
                if s.check_conn():
                    color = s.accept_conn()
                    if not color == None:
                        if color[:3] == (666, 666, 666):
                            l.rainbow(color[3])
                        l.fade_to(color)
                    
        l.change(h.distance())

except KeyboardInterrupt:
    s.close()
    wlan.disconnect()
    

if __name__ == '__main__':
    main()
