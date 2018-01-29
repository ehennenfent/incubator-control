import time

class Incubator():
    
    def __init__(self, ambient_temp):
        self.temp = 22.0 # TODO read starting temp
        self.ambient_temp = ambient_temp
        self.duty_cycle = 0
        self._tictime = time.time()

    def tick(self, tictime=0):
        # Newton's law of cooling:
        # https://www.ugrad.math.ubc.ca/coursedoc/math100/notes/diffeqs.cool.html
        current_time = time.time()
        if tictime != 0:
            dt = tictime
        else:
            dt = current_time - self._tictime # delta time

        #TODO Incorporate incubator controls and temperature smoothing

    def set_duty_cycle(self, new_duty_cycle):
        if new_duty_cycle > 1 or new_duty_cycle < 0:
            raise ValueError("Duty cycle must be between 0 and 1")
        self.duty_cycle = new_duty_cycle
        
    def stable_duty_cycle(self, target_temp):
        return abs(-.00257 * (target_temp - self.ambient_temp)) / (.00208 * (58.5 - target_temp))