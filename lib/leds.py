# -----------------------------------------------------------------------------
# Based on             :   Jonas Witte, Leon Reusch, Jannis Dickel
# Edited by            :   Leon Reusch
# -----------------------------------------------------------------------------

from machine import Pin
import neopixel
from time import sleep
import asyncio

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
        Constructs a Led-Stripe-Object to connect to.

        :param num_leds: int - the count of the LEDs in the Stripe
        :param pin: int - Port-number of the Pin on the Raspberry
        """
        self.num_leds = num_leds
        self.np = neopixel.NeoPixel(Pin(pin), num_leds)
        self.color = self.OFF
        self.change_color(self.RED)
        self.rainbow_task = None

    def set_all(self, color: tuple[int, int, int]) -> None:
        """
        Sets all LEDs to the given color.

        :param color: (int, int, int) - 3 ints representing the color on the LED-Stripe (use the 'leds.py' attributes!)
        :return: None
        """
        for led in range(self.num_leds):
            self.np[led] = color
            self.np.write()
            self.color = color
            
    def cancel_rainbow(self) -> None:
        """
        Cancels the current rainbow async task.
        
        :return: None
        
        """
        try:
            self.rainbow_task.cancel()
            self.rainbow_task = None
        except:
            pass
        
    def set_rainbow_task(self, rainbow_task) -> None:
        """
        """
        self.rainbow_task = rainbow_task
    
    async def rainbow(self) -> None:
        """
        Switches all the colors in a rainbow line.
        
        :return: None
        """
        self.fade_to(self.RED)
        while True:
            await asyncio.sleep(0.5)
            if self.color == self.RED:
                for j in range(255):
                    self.set_all((255, self.color[1]+1, 0))
                    await asyncio.sleep(0.01)
            elif self.color == self.YELLOW:
                for j in range(255):
                    self.set_all((self.color[0]-1, 255, 0))
                    await asyncio.sleep(0.01)
            elif self.color == self.GREEN:
                for j in range(255):
                    self.set_all((0, 255, self.color[2]+1))
                    await asyncio.sleep(0.01)
            elif self.color == self.CYAN:
                for j in range(255):
                    self.set_all((0, self.color[1]-1, 255))
                    await asyncio.sleep(0.01)
            elif self.color == self.BLUE:
                for j in range(255):
                    self.set_all((self.color[0]+1, 0, 255))
                    await asyncio.sleep(0.01)
            elif self.color == self.MAGENTA:
                for j in range(255):
                    self.set_all((255, 0, self.color[2]-1))
                    await asyncio.sleep(0.01)
                
    def change_color(self, color: (int, int, int)) -> None:
        """
        Changes the color to the given color or simply turns the LEDs on when they are OFF.

        :param color: (int, int, int) - the wanted color
        :return: None
        """
        self.cancel_rainbow()
        if self.color == self.OFF or color == self.OFF:
            self.set_all(color)
        else:
            self.fade_to(color)
                
    def fade_to(self, color_to: (int, int, int)) -> None:
        """
        Changes the color of the LEDS to the given color by fading to them.

        :param color: (int, int, int) - the wanted color which should be faded to
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

        :param distance: int - the distance measured by the HCSR04 sensor
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
            self.change_color(self.OFF)
        