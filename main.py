from lib.leds import Leds
from lib.HCSR04 import HCSR04
from time import sleep

l = Leds(6, 28)

h = HCSR04(17, 16)

l.set_all(l.OFF)
#l.rainbow_unlimited()
#while True:
    #print(h.distance())
    #sleep(0.5)