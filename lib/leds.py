# -----------------------------------------------------------------------------
# Credits           :   Jonas Witte, Jannis Dickel
# Author            :   Leon Reusch
# -----------------------------------------------------------------------------

from machine import Pin
import neopixel
from time import sleep


class Leds:
    # initialization of all colors as statics
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    MAGENTA = (255, 0, 255)
    WHITE = (255, 255, 255)
    COLOR_LST =[(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255), (0, 0, 0)]
    OFF = (0, 0, 0)

    def __init__(self, num_leds: int, pin: int):
        """
        Constructs a Led-Stripe-Object to connect to

        :param num_leds: an int with the count of the LEDs in the Stripe
        :param pin: an int which represents the Pin on the ESP32
        :return: LED-object
        """
        self.num_leds = num_leds
        self.np = neopixel.NeoPixel(Pin(pin), num_leds)
        self.color = self.OFF

    def set_all(self, color: tuple[int, int, int]) -> None:
        """
        Sets all LEDs to the given color

        :param color: a tuple of 3 ints representing the color on the LED-Stripe (use the 'leds.py' attributes!)
        :return: None
        """
        for led in range(self.num_leds):
            self.np[led] = color
            self.np.write()
            self.color = color
    
    def rainbow(self, loop_duration: int) -> None:
        """
        Switches all the colors in a rainbow line for a specified duration
        
        :param loop_duration: number of rainbow run throughs
        :return: None
        """
        self.set_all(self.OFF)
        print(loop_duration)
        for i in range(loop_duration):
            if self.color == self.OFF:
                for j in range(255):
                    self.set_all((self.color[0]+1, 0, 0))
                    sleep(0.02)
            if self.color == self.RED:
                for j in range(255):
                    self.set_all((255, self.color[1]+1, 0))
                    sleep(0.02)
            if self.color == self.YELLOW:
                for j in range(255):
                    self.set_all((self.color[0]-1, 255, 0))
                    sleep(0.02)
            if self.color == self.GREEN:
                for j in range(255):
                    self.set_all((0, 255, self.color[2]+1))
                    sleep(0.02)
            if self.color == self.CYAN:
                for j in range(255):
                    self.set_all((0, self.color[1]-1, 255))
                    sleep(0.02)
            if self.color == self.BLUE:
                for j in range(255):
                    self.set_all((self.color[0]+1, 0, 255))
                    sleep(0.02)
            if self.color == self.MAGENTA:
                for j in range(255):
                    self.set_all((255, 0, self.color[2]-1))
                    sleep(0.02)
                
    def change_color(self, color: (int, int, int)) -> None:
        """
        Changes the color to the given color or simply turns the LEDs on when they are OFF

        :param color: the wanted color
        :return: None
        """
        if self.color == self.OFF:
            self.set_all(color)
        else:
            self.fade_to(color)
        
        #new_pos = self.COLOR_LST.index(color)
        #old_pos = self.COLOR_LST.index(self.color)
        #pos_change = new_pos - old_pos
        
        #if pos_change > 0:
            #for i in range(old_pos+1, new_pos+1, 1):
                #self.fade_to(self.COLOR_LST[i])
        #elif pos_change < 0:
            #for i in range(old_pos-1, new_pos-1, -1):
                #self.fade_to(self.COLOR_LST[i])
                
    def fade_to(self, color_to: (int, int, int)) -> None:
        """
        Changes the color of the LEDS to the given color by fading to them

        :param color: the wanted color which should be faded to
        :return: None
        """
        dif_r = color_to[0] -self.color[0]
        dif_g = color_to[1] -self.color[1]
        dif_b = color_to[2] -self.color[2]
        
        for i in range(0, max(abs(dif_r), abs(dif_g), abs(dif_b)), 1):
            new_color = ()
            if not self.color[0] == color_to[0]:
                new_color += (self.color[0]+int(dif_r/abs(dif_r)), )
            else:
                new_color += (self.color[0], )
            if not self.color[1] == color_to[1]:
                new_color += (self.color[1]+int(dif_g/abs(dif_g)), )
            else:
                new_color += (self.color[1], )
            if not self.color[2] == color_to[2]:
                new_color += (self.color[2]+int(dif_b/abs(dif_b)), )
            else:
                new_color += (self.color[2], )
            self.set_all(new_color)
        
        
    def change(self, distance: int) -> None:
        """
        Changes the color to the corresponding color for the given distance by fading to it

        :param distance: the distance measured by the HCSR04 sensor
        :return: None
        """
        if distance < 5:
            self.change_color(self.RED)
        elif 6 < distance < 10:
            self.change_color(self.YELLOW)
        elif 11 < distance < 15:
            self.change_color(self.GREEN)
        elif 16 < distance < 20:
            self.change_color(self.CYAN)
        elif 21 < distance < 25:
            self.change_color(self.BLUE)
        elif 26 < distance < 30:
            self.change_color(self.MAGENTA)
        elif 32 < distance < 35:
            self.set_all(self.OFF)
        