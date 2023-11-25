from lib.leds import Leds
from lib.HCSR04 import HCSR04

def main() -> None:
    # initialization
    l = Leds(6, 28)
    h = HCSR04(17, 16)

    # changing colors depending on the measured distance from the HCSR04
    while True:
        distance = h.distance()
        print(distance)
        l.fade(distance)
    
if __name__ == '__main__':
    main()