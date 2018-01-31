from ubidots import ApiClient
from secrets import master_incubator_token
import pprint as pp
import traceback
import time

class Renderer(object):
    def __init__(self):
        self.count = 0
        
    def render(self, incubator):
        self.count += 1
    
    def finish(self, incubator):
        pass


class TerminalRenderer(Renderer):
    
    def render(self, incubator, controller):
        super(TerminalRenderer, self).render(incubator)
        if (self.count % 1666) == 0:
            print("%s -- +- %s" % (incubator.temp, controller.avg_error))

class UbidotsRenderer(Renderer):
    def __init__(self):
        super(UbidotsRenderer, self).__init__()
        
        self.api = ApiClient(token=master_incubator_token)
        
        self.incubator_endpoint = self.api.get_datasource('5a224554c03f9721f59934ff')
        self.variables = self.incubator_endpoint.get_variables()
        
        self.temperature_1 = self._get_variable('temperature-1')
        self.temperature_2 = self._get_variable('temperature-2')
        self.humidity_1 = self._get_variable('humidity-1')
        self.humidity_2 = self._get_variable('humidity-2')
        self.heater_1 = self._get_variable('heater-1')
        self.heater_2 = self._get_variable('heater-2')
        self.uptime = self._get_variable('uptime')
        self.error = self._get_variable('error')
        
        self.backlogged_data = []

    def _get_time(self):
        return int(time.time() * 1000)

    def _get_variable(self, label):
    
        for variable in self.variables:
            if str(variable.label) == label:
                print("Found variable %s: %s" % (variable.label, variable.id))
                return variable
        raise Exception("Could not find variable %s!" % label)
        
        
    def render(self, incubator, controller):
        timestamp = self._get_time()
    
        data = [{'variable': self.temperature_1.id, 'value': incubator.temp_1, timestamp:timestamp},
                {'variable': self.temperature_2.id, 'value': incubator.temp_2, timestamp:timestamp},
                {'variable': self.humidity_1.id, 'value': incubator.hum_1, timestamp:timestamp},
                {'variable': self.humidity_2.id, 'value': incubator.hum_2, timestamp:timestamp},
                {'variable': self.heater_1.id, 'value': incubator.duty_cycle, timestamp:timestamp},
                {'variable': self.heater_2.id, 'value': incubator.duty_cycle, timestamp:timestamp},
                {'variable': self.uptime.id, 'value': incubator.uptime, timestamp:timestamp},
                {'variable': self.error.id, 'value': controller.avg_error, timestamp:timestamp}]
        
        try:
            self.api.save_collection(data)
        except:
            for i in data:
                self.backlogged_data.append(i)
            traceback.print_exc()
        
        if (incubator.uptime == 0):
            pp.pprint(self.backlogged_data)