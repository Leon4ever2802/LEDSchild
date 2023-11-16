# -----------------------------------------------------------------------------
# Author               :   Jonas Witte, Leon Reusch, Jannis Dickel
# -----------------------------------------------------------------------------

# better imports with form ... import? -->
import machine, neopixel


class Leds:
    # initialization of all colors as statics
    RED = (255, 0, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    OFF = (0, 0, 0)

    def __init__(self, num_leds: int, pin: int) -> None:
        """
        Constructs a Led-Stripe-Object to connect to

        :param num_leds: a int with the count of the LEDs in the Stripe
        :param pin: a int which represents the Pin on the ESP32
        """

        self.num_leds = num_leds
        self.np = neopixel.NeoPixel(machine.Pin(pin), num_leds)
        self.color = None

    def set_all(self, color: tuple[int, int, int]) -> None:
        """
        setts all LEDs to the given color

        :param color: a tuple of 3 ints representing the color on the LED-Stripe (use the 'leds.py' attributes!)
        :return: None
        """

        for led in range(self.num_leds):
            self.np[led] = color
            self.np.write()
            self.color = color

    def change(self) -> None:
        """
         Switches between the three main colors for one button

        :return: None
        """
        if self.color == self.RED:
            self.set_all(self.GREEN)

        elif self.color == self.GREEN:
            self.set_all(self.YELLOW)

        else:
            self.set_all(self.RED)
