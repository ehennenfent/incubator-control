from ubidots import ApiClient
from secrets import master_incubator_token
import traceback
import time

class Renderer():
    def __init__(self):
        self.count = 0
        
    def render(self, incubator):
        self.count += 1
    
    def finish(self, incubator):
        pass


class TerminalRenderer(Renderer):
    
    def render(self, incubator):
        super().render(incubator)
        if (self.count % 1666) == 0:
            print(incubator.temp)

class UbidotsRenderer(Renderer):
    def __init__(self):
        super().__init__()
        
        self.api = ApiClient(token=master_incubator_token)
        
        self.incubator_endpoint = self.api.get_datasource('5a224554c03f9721f59934ff')
        self.variables = incubator_endpoint.get_variables()
        
        self.temperature_1 = self._get_variable('temperature-1')
        self.temperature_2 = self._get_variable('temperature-2')
        self.humidity_1 = self._get_variable('humidity-1')
        self.humidity_2 = self._get_variable('humidity-2')
        self.heater_1 = self._get_variable('heater-1')
        self.heater_2 = self._get_variable('heater-2')
        self.uptime = self._get_variable('uptime')

    def _get_time(self):
        return int(time.time() * 1000)

    def _get_variable(self, label):
    
        for variable in self.variables:
            if str(variable.label) == label:
                print("Found variable %s: %s" % (variable.label, variable.id))
                return variable
        raise Exception("Could not find variable %s!" % label)
        
        
    def render(self, incubator):
        timestamp = self._get_time()
    
        try:
            self.api.save_collection([
                {'variable': self.temperature_1.id, 'value': incubator.temp_1, timestamp:timestamp},
                {'variable': self.temperature_2.id, 'value': incubator.temp_2, timestamp:timestamp},
                {'variable': self.humidity_1.id, 'value': incubator.hum_1, timestamp:timestamp},
                {'variable': self.humidity_2.id, 'value': incubator.hum_2, timestamp:timestamp},
                {'variable': self.heater_1.id, 'value': incubator.duty_cycle, timestamp:timestamp},
                {'variable': self.heater_2.id, 'value': incubator.duty_cycle, timestamp:timestamp},
                {'variable': self.uptime.id, 'value': incubator.uptime, timestamp:timestamp}])
        except:
            print("Error saving data to ubidots")
            traceback.print_exc()
        