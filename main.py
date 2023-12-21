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
        led = Leds(6, 28)
        sensor = HCSR04(17, 16)
        server = Server(IP_ADDR, 80, led)

        print("Device listening on Port: " + IP_ADDR)
        server.start()
        
        # changing colors depending on the measured distance from the HCSR04 or HTTP-request
        while True:
            server.check()        
            led.change(sensor.distance())

    except KeyboardInterrupt:
        server.close()
        wlan.disconnect()
    

if __name__ == '__main__':
    main()
