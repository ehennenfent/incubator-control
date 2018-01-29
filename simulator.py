import time

class Sim():
    
    def __init__(self, starting_temp, ambient_temp):
        self.temp = starting_temp
        self.ambient_temp = ambient_temp
        self.duty_cycle = 0
        self._tictime = time.time()
        
        self._k_cool = -.00257 # Calculated from actual incubator cooling behavior
        self._k_heat = .00208
        # Heating equals cooling at ~38.5 degrees in a ~22 degree room
        # Use this to solve for approximate element temp
        # TODO confirm this with IR thermometer
        self._element_temp = 58.5
    
    def tick(self, tictime=0):
        # Newton's law of cooling:
        # https://www.ugrad.math.ubc.ca/coursedoc/math100/notes/diffeqs.cool.html
        current_time = time.time()
        if tictime != 0:
            dt = tictime
        else:
            dt = current_time - self._tictime # delta time
        dT_over_dt = self._k_cool * (self.temp - self.ambient_temp)
        dT = dT_over_dt * dt # delta temperature
        
        dT_over_dt = self._k_heat * self.duty_cycle * (self._element_temp - self.temp)
        dT += (dT_over_dt * dt)
        
        self.temp += dT
        self._tictime = current_time

    def set_duty_cycle(self, new_duty_cycle):
        if new_duty_cycle > 1 or new_duty_cycle < 0:
            raise ValueError("Duty cycle must be between 0 and 1")
        self.duty_cycle = new_duty_cycle
        
    def stable_duty_cycle(self, target_temp):
        return abs(self._k_cool * (target_temp - self.ambient_temp)) / (self._k_heat * (self._element_temp - target_temp))