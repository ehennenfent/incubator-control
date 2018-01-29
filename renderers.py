
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
        print("Haven't written a logging system for ubidots yet :/")
        exit(1)