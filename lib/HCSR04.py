# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

from machine import Pin
from time import sleep_us, ticks_us

class HCSR04:
    
    def __init__(self, pin_trigger: int, pin_echo: int) -> None:
        
        self.trigger = Pin(pin_trigger, Pin.OUT)
        self.echo = Pin(pin_echo, Pin.IN)
        
    def distance(self) -> int:
        self.trigger.high()
        sleep_us(3)
        self.trigger.low()
        while (self.echo.value()==0):
            pass #wait for echo
        lastreadtime = ticks_us() # record the time when signal went HIGH
        while (self.echo.value()==1):
            pass #wait for echo to finish
        echotime = ticks_us()-lastreadtime
        return (echotime * 0.03432) / 2
