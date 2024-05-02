# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

from lib.leds import Leds
from lib.HCSR04 import HCSR04
from lib.server import Server
from settings import SETTINGS
import asyncio
from asyncio import Task


async def connect_to_wlan(loop, led: Leds, sensor_task: Task, sensor: HCSR04) -> None:
    """
    Function which continuously tries to connect to the WLAN alongside with the HCSR04.
    Distance measuring will still work and change the LEDs.
        
    :return: None
    """
    while True:
        # try to connect with the data from 'SETTINGS-dict'
        wlan.connect(SETTINGS["SSID"], SETTINGS["Password"])

        # waiting until device has an IP-Addr and is fully connected
        counter = 0
        while not wlan.status() == 3:
            if counter == 5:
                wlan.disconnect()
                break
            await asyncio.sleep(1)
            counter = counter + 1
            continue

        if wlan.status() == 3:
            SETTINGS["IP-Addr"] = wlan.ifconfig()[0]
            print(f"\033[92mConnected successfully to WLAN: {wlan.ifconfig()}\033[0m")

            server = Server(SETTINGS["IP-Addr"], SETTINGS["ServerPort"], led, loop, sensor_task, sensor)
            loop.create_task(server.start())
            print("Device listening on Port: " + SETTINGS["IP-Addr"])
            break


def main() -> None:
    """
    Main function of the LED-Schild.
    Starts all the different tasks to be executed and lets them run inside an event loop just like threads.
        
    :return: None
    """
    loop = asyncio.get_event_loop()

    led = Leds(SETTINGS["AnzLEDs"], SETTINGS["LEDPin"])

    sensor = HCSR04(SETTINGS["TriggerPin"], SETTINGS["EchoPin"], led)
    sensor_task = loop.create_task(sensor.change_by_distance())

    if SETTINGS["IP-Addr"] != "":
        server = Server(SETTINGS["IP-Addr"], SETTINGS["ServerPort"], led, loop, sensor_task, sensor)
        loop.create_task(server.start())
        print("Device listening on: " + SETTINGS["IP-Addr"])
        led.wlan_active()
    else:
        loop.create_task(connect_to_wlan(loop, led, sensor_task, sensor))
        print("Continuously trying to connect to WLAN.")
        led.wlan_not_active()

    try:
        loop.run_forever()

    except KeyboardInterrupt:
        try:
            server.close()
            wlan.disconnect()
        except:
            pass


if __name__ == '__main__':
    main()
