from lib.leds import Leds
from time import sleep


l = Leds(6, 28)
l.set_all(l.RED)

# Initialisierung GPIO-Ausgang für Trigger-Signal
trigger = Pin(16, Pin.OUT)

# Initialisierung GPIO-Eingang für Echo-Signal
echo = Pin(17, Pin.IN)