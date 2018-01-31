
class Controller(object):
    def __init__(self):
        pass
    
    def before_tick(self, incubator, **kwargs):
        pass
    
    def after_tick(self, incubator, **kwargs):
        pass

class DumbController(Controller):
    
    def __init__(self, target_temp, tolerance=0.2):
        super(DumbController, self).__init__()
        self.target_temp = target_temp
        self.tolerance = tolerance
    
    def before_tick(self, incubator, **kwargs):
        if incubator.temp < (self.target_temp - self.tolerance):
            incubator.set_duty_cycle(1)
            
    
    def after_tick(self, incubator, **kwargs):
        if incubator.temp > (self.target_temp + self.tolerance):
            incubator.set_duty_cycle(0)

class SmartPController(Controller):
    def __init__(self, target_temp, p=0.809):
        super(SmartPController, self).__init__()
        self.target_temp = target_temp
        self.p = p
        
    def before_tick(self, incubator, **kwargs):
        error = self.target_temp - incubator.temp
        new_duty_cycle = max(incubator.stable_duty_cycle(self.target_temp), min(1, self.p * error))
        incubator.set_duty_cycle(new_duty_cycle)

class PIDController(Controller):
    def __init__(self, target_temp, p=0.809, i=0.5, d=0.1):
        super(PIDController, self).__init__()
        self.target_temp = target_temp
        self.p = p
        self.i = i
        self.d = d
        self.accumulated_error = 0
        self.last_error = 0
        
        self.rolling_error = []
        
    def before_tick(self, incubator, tictime, **kwargs):
        error = self.target_temp - incubator.temp
        self.accumulated_error += error * tictime
        
        p_term = self.p * error
        i_term = self.i * self.accumulated_error
        d_term = self.d * ((error - self.last_error) / tictime)
        
        self.last_error = error
        
        new_duty_cycle = max(0, min(1, p_term + i_term + d_term))
        incubator.set_duty_cycle(new_duty_cycle)
        
    def after_tick(self, incubator, **kwargs):
        error = self.target_temp - incubator.temp
        self.rolling_error = self.rolling_error[-2048:]
        self.rolling_error.append(abs(error))
        
    @property
    def avg_error(self):
        if(len(self.rolling_error) > 0):
            return sum(self.rolling_error) / float(len(self.rolling_error))
        return 0