from lib.leds import Leds
from lib.HCSR04 import HCSR04
from lib.server import Server


def main() -> None:
    """
    The main function to a "LEDSchild"

    functions:
        - Changing the colors of a LED stripe by fading to a color corresponding to the measured distance of a
        HCSR04 sensor
        - in dev.: network connection to the raspberry to change color via HTTP-request

    :return: None
    """
    # initialization
    l = Leds(6, 28)
    h = HCSR04(17, 16)
    # s = Server("192.168.0.237", 65432)

    # s.start()

    # changing colors depending on the measured distance from the HCSR04
    while True:
        distance = h.distance()
        print(distance)
        l.change(distance)


if __name__ == '__main__':
    main()
