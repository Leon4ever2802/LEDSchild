# -----------------------------------------------------------------------------
# Based on             :   Jonas Witte, Leon Reusch, Jannis Dickel
# Edited by            :   Leon Reusch
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
                
    def change_color(self, color: (int, int, int)) -> None:
        if(self.color == self.OFF):
            self.set_all(color)
        
        newPos = self.COLOR_LST.index(color)
        oldPos = self.COLOR_LST.index(self.color)
        posChange = newPos - oldPos
        
        if posChange > 0:
            for i in range(oldPos+1, newPos+1, 1):
                self.fade_to(self.COLOR_LST[i])
        elif posChange < 0:
            for i in range(oldPos-1, newPos-1, -1):
                self.fade_to(self.COLOR_LST[i])
                
    def fade_to(self, color_to: (int, int, int)) -> None:
        if(color_to[0] > self.color[0]):
            for i in range(5, 256, 5):
                self.set_all((i, self.color[1], self.color[2]))
        
        elif(color_to[0] < self.color[0]):
            for i in range(5, 256, 5):
                self.set_all((255-i, self.color[1], self.color[2]))
                
        elif(color_to[1] > self.color[1]):
            for i in range(5, 256, 5):
                self.set_all((self.color[0], i, self.color[2]))
                
        elif(color_to[1] < self.color[1]):
            for i in range(5, 256, 5):
                self.set_all((self.color[0], 255-i, self.color[2]))
                
        elif(color_to[2] > self.color[2]):
            for i in range(5, 256, 5):
                self.set_all((self.color[0], self.color[1], i))
                
        elif(color_to[2] < self.color[2]):
            for i in range(5, 256, 5):
                self.set_all((self.color[0], self.color[1], 255-i))

    def switch_distance(self, distance: int) -> None:
        """
        Switches all the colors depending on the measured distance of a sensor
        
        :param distance: a distance measured by a sensor (optimal: HCSR04-sensor)
        :return: None
        """
        if(distance < 4):
            self.set_all(self.RED)
            
        elif(distance > 4 and distance < 7):
            self.set_all((255, 0, int ((distance % 3) * 85)))
            
        elif(distance > 7 and distance < 10):
            self.set_all((int( 255-((distance % 3) * 85)), 0, 255))
            
        elif(distance > 10 and distance < 11):
            self.set_all(self.BLUE)
            
        elif(distance > 11 and distance < 14):
            self.set_all((0, int ((distance % 3) * 85), 255))
            
        elif(distance > 14 and distance < 17):
            self.set_all((0, 255, int (255-((distance % 3) * 85))))
            
        elif(distance > 17 and distance < 18):
            self.set_all(self.GREEN)
            
        elif(distance > 18 and distance < 21):
            self.set_all((int ((distance % 3) * 85), 255, 0))
            
        elif(distance > 23 and distance < 26):
            self.set_all(self.WHITE)
            
        elif(distance > 26 and distance < 30):
            self.set_all(self.OFF)
            
        else:
            return
        
    def change(self, distance: int) -> None:
        if distance < 5:
            self.change_color(self.RED)
        elif 5 < distance < 9:
            self.change_color(self.YELLOW)
        elif 9 < distance < 13:
            self.change_color(self.GREEN)
        elif 13 < distance < 17:
            self.change_color(self.CYAN)
        elif 17 < distance < 21:
            self.change_color(self.BLUE)
        elif 21 < distance < 25:
            self.change_color(self.MAGENTA)
        elif 25 < distance < 30:
            self.set_all(self.OFF)
        