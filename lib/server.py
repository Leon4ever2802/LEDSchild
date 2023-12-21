# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------
import rester

class Server(rester.Rester):
    
    def __init__(self, host: str, port: int, led):
        super().__init__(self, host, port)
        self.led = led
    
    def check_exceptions(self, color: (int, int, int)) -> bool:
        """
        Checks for exceptions that can be maybe when passing a value
        
        :param color: the given color tuple to check for correctness
        :return: tuple (int, int, int[, int]) - given color
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
    
    def get_changecolor(self, color):
        """
        """
        set_color = tuple(map(int, color.split(";")))
        print(set_color)
        if not self.check_exceptions(set_color):
            return self.bad_request
        
        self.led.fade_to(set_color)
        
        return self.good_request
        
    def get_(self):
        in_index = open("lib/answer.html")
        index = in_index.read()
        in_index.close()
        return (self.good_request, index)
        
        