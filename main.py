from simulator import Sim
from incubator import Incubator
from renderers import TerminalRenderer
from controllers import PIDController

import time

NUM_TICS = 200000 # 120 minutes

def simulate(starting_temp, ambient_temp, controller, renderer, t=.036):
    sim = Sim(starting_temp, ambient_temp)
    
    for i in range(NUM_TICS):
        renderer.render(sim)
        controller.before_tick(sim, tictime=t)
        sim.tick(tictime=t)
        controller.after_tick(sim, tictime=t)

controller = PIDController(37.0)

renderer = TerminalRenderer()
simulate(22.0, 22.0, controller, renderer)

def incubate(starting_temp, ambient_temp, controller, renderer):
    incubator = Incubator(ambient_temp)
    incubator = Sim(starting_temp, ambient_temp)
    
    last_time = time.time()
    while(True):
        current_time = time.time()
        t = current_time - last_time
        renderer.render(incubator)
        controller.before_tick(incubator, tictime=t)
        incubator.tick(tictime=t)
        controller.after_tick(incubator, tictime=t)
        last_time = current_time
        
# incubate(22.0, 22.0, controller, renderer)