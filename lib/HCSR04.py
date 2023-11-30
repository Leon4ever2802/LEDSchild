# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

from machine import Pin
from time import sleep_us, ticks_us


class HCSR04:

    def __init__(self, pin_trigger: int, pin_echo: int) -> None:
        """
        Constructs a HCSR04-sensor-Object to connect to

        :param pin_trigger: an int with the number of the Pin the trigger is connected to
        :param pin_echo: an int with the number of the Pin the echo is connected to
        """
        self.trigger = Pin(pin_trigger, Pin.OUT)
        self.echo = Pin(pin_echo, Pin.IN)

    def distance(self) -> int:
        """
        Measuring the distance of an object in front of the sensor in cm
        
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
