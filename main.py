# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

from lib.leds import Leds
from lib.HCSR04 import HCSR04
from lib.server import Server
from settings import SETTINGS
import asyncio

def main():
    loop = asyncio.get_event_loop()
    
    led = Leds(6, 28)
    
    sensor = HCSR04(17, 16, led)
    sensor_task = loop.create_task(sensor.change_by_distance())
    
    server = Server(SETTINGS["IP-Addr"], 80, led, loop, sensor_task, sensor)
    loop.create_task(server.start())
    
    print("Device listening on Port: " + SETTINGS["IP-Addr"])
    
    try:
        loop.run_forever()
        
    except KeyboardInterrupt:
        server.close()
        wlan.disconnect()

if __name__ == '__main__':
    main()
