# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

from lib.leds import Leds
from lib.HCSR04 import HCSR04
from lib.server import Server
import asyncio

async def main(led, sensor, server) -> None:
    """
    The main function to a "LEDSchild"

    functions:
        - Changing the colors of a LED stripe by fading to a color corresponding to the measured distance of a
        HCSR04 sensor
        - network connection to the raspberry to change color via HTTP-request

    :return: None
    """
    try:
        # changing colors depending on the measured distance from the HCSR04
        while True:
            led.change(sensor.distance())
            await asyncio.sleep(0)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    try:
        # initialization of everything ivolved
        led = Leds(6, 28)
        sensor = HCSR04(17, 16)
        server = Server(IP_ADDR, 80, led)
        
        print("Device listening on Port: " + IP_ADDR)
        
        # creating event-loop for sensor + server
        loop = asyncio.get_event_loop()
        loop.create_task(server.start())
        loop.create_task(main(led, sensor, server))
        loop.run_forever()
        
    except KeyboardInterrupt:
        server.close()
        wlan.disconnect()
