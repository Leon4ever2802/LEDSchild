# -----------------------------------------------------------------------------
# Author               :   Jonas Witte, Leon Reusch, Jannis Dickel
# -----------------------------------------------------------------------------

from machine import Pin
import neopixel


class Leds:
    # initialization of all colors as statics
    RED = (255, 0, 0)
    MAGENTA = (255, 0, 255)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    OFF = (0, 0, 0)

    def __init__(self, num_leds: int, pin: int) -> None:
        """
        Constructs a Led-Stripe-Object to connect to

        :param num_leds: a int with the count of the LEDs in the Stripe
        :param pin: a int which represents the Pin on the ESP32
        """

        self.num_leds = num_leds
        self.np = neopixel.NeoPixel(Pin(pin), num_leds)
        self.color = self.OFF

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
            
    def rainbow_unlimited(self) -> None:
        """
        Switches all the colors in a rainbow line unlimitely
        
        :return: None
        """
        while True:
            if self.color == self.OFF:
                for j in range(255):
                    self.set_all((self.color[0]+1, 0, 0))
            if self.color == self.RED:
                for j in range(255):
                    self.set_all((255, 0, self.color[2]+1))
            if self.color == self.MAGENTA:
                for j in range(255):
                    self.set_all((self.color[0]-1, 0, 255))
            if self.color == self.BLUE:
                for j in range(255):
                    self.set_all((0, self.color[1]+1, 255))
            if self.color == self.CYAN:
                for j in range(255):
                    self.set_all((0, 255, self.color[2]-1))
            if self.color == self.GREEN:
                for j in range(255):
                    self.set_all((self.color[0]+1, 255, 0))
            if self.color == self.YELLOW:
                for j in range(255):
                    self.set_all((255, self.color[1]-1, 0))
    
    def rainbow(self, loop_duration: int) -> None:
        """
        Switches all the colors in a rainbow line for a specifide duration
        
        :param loop_duration: number of rainbow run throughs
        :return: None
        """
        for i in range(loop_duration):
            if self.color == self.OFF:
                for j in range(255):
                    self.set_all((self.color[0]+1, 0, 0))
            if self.color == self.RED:
                for j in range(255):
                    self.set_all((255, 0, self.color[2]+1))
            if self.color == self.MAGENTA:
                for j in range(255):
                    self.set_all((self.color[0]-1, 0, 255))
            if self.color == self.BLUE:
                for j in range(255):
                    self.set_all((0, self.color[1]+1, 255))
            if self.color == self.CYAN:
                for j in range(255):
                    self.set_all((0, 255, self.color[2]-1))
            if self.color == self.GREEN:
                for j in range(255):
                    self.set_all((self.color[0]+1, 255, 0))
            if self.color == self.YELLOW:
                for j in range(255):
                    self.set_all((255, self.color[1]-1, 0))
                
    def fade(self, distance: int) -> None:
        
        print(1)
        