# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

from machine import Pin
from time import sleep_us, ticks_us
import asyncio

from lib.leds import Leds


class HCSR04:
    """
    An ultrasound sensor class which measures the distance of objects in front of the sensor.
    It can also change the color of the LEDs depending on the measured distance.
    """

    def __init__(self, pin_trigger: int, pin_echo: int, led: Leds):
        """
        Constructs a HCSR04-sensor-Object to connect to.

        :param pin_trigger: the number of the Pin the trigger is connected to
        :param pin_echo: the number of the Pin the echo is connected to
        :param led: Leds-object used for the connected LED stripe
        """
        self.trigger = Pin(pin_trigger, Pin.OUT)
        self.echo = Pin(pin_echo, Pin.IN)
        self.led = led

    def distance(self) -> int:
        """
        Measures the distance of an object in front of the sensor in cm.
        
        :return: distance of the object in cm
        """
        self.trigger.high()
        sleep_us(3)
        self.trigger.low()
        while self.echo.value() == 0:
            pass
        lastreadtime = ticks_us()
        while self.echo.value() == 1:
            pass
        echotime = ticks_us() - lastreadtime
        return (echotime * 0.03432) / 2

    async def change_by_distance(self) -> None:
        """
        Changes the color of the LED based on the measured distance.
        This is simply the async methode to call for asyncio.
        
        :return: None
        """
        try:
            # changing colors depending on the measured distance from the HCSR04
            while True:
                self.led.change(self.distance())
                await asyncio.sleep(0)

        except KeyboardInterrupt:
            pass
