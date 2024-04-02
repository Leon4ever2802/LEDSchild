# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------
from asyncio import Task
import rester
from lib.leds import Leds
from lib.HCSR04 import HCSR04


class Server(rester.Rester):
    """
    A server class used to control the Raspberry Pi Pico W via HTTP.
    """

    def __init__(self, host: str, port: int, led: Leds, loop, sensor_task: Task, sensor: HCSR04):
        """
        Initializes a Server-object based on the Rester 'API'.
        
        :param host: the IPv4 address on which the server should run
        :param port: the port number for the server
        :param led: Leds-object so it can be controlled
        :param loop: event_loop handling the async of all tasks
        :param sensor_task: current sensor task inside the loop
        :param sensor: HCSR04-object so we can create a task with the measuring methode inside
        """
        super().__init__(self, host, port)
        self.led = led
        self.loop = loop
        self.sensor_task = sensor_task
        self.sensor = sensor
        self.rainbow_task = None

    def check_exceptions(self, color: (int, int, int)) -> bool:
        """
        Checks for exceptions that can be maybe when passing a value.

        :param color: the given color tuple to check for correctness
        :return: is given color ok?
        """
        try:
            if not len(color) == 3:
                if len(color) == 4 and color[0] == 666 and color[1] == 666 and color[2] == 666 and color[3] > 0:
                    return True
                else:
                    raise Exception()

            for col in color:
                if not 0 <= col <= 255:
                    raise Exception()
            return True
        except:
            return False

    def get_changecolor(self, color: str) -> str:
        """
        Changes the color of the LED-Schild to the given color inside the URL.
        
        :param color: the color given inside the URL as a parameter
        :return: HTTP.status
        """
        set_color = tuple(map(int, color.split(";")))
        if not self.check_exceptions(set_color):
            return self.BAD_REQUEST

        self.led.change_color(set_color)

        return self.OK

    def get_sensor(self) -> str:
        """
        Blocks/Reactivates the HCSR04-sensor.
        
        :return: HTTP.status
        """
        if self.sensor_task is not None:
            self.sensor_task.cancel()
            self.sensor_task = None
        else:
            self.sensor_task = self.loop.create_task(self.sensor.change_by_distance())
        return self.OK

    def get_rainbow(self) -> str:
        """
        Makes the LED-Schild run through the color spectrum.
        
        :return: HTTP.status
        """
        try:
            self.rainbow_task.cancel()
        except:
            pass

        self.rainbow_task = self.loop.create_task(self.led.rainbow())
        self.led.set_rainbow_task(self.rainbow_task)
        return self.OK

    def get_turnoffon(self) -> str:
        """
        Deactivates the HCSR04 sensor and turns the Leds to OFF.
        If both are deactivated, sensor will be started and LED set to RED.
        
        :return: HTTP.status
        """
        try:
            self.sensor_task.cancel()
            self.sensor_task = None
        except:
            if self.led.color == self.led.OFF:
                self.sensor_task = self.loop.create_task(self.sensor.change_by_distance())
                self.led.change_color(self.led.RED)
                return self.OK
            pass
        self.led.change_color(self.led.OFF)
        return self.OK

    def get_(self) -> (str, str):
        """
        Sends the index.html to the client.
        
        :return: (HTTP.status, html-code)
        """
        with open("assets/answer.html") as index:
            index_html = index.read()
            index.close()
        return self.OK, index_html
