from simulator import Sim
# from incubator import Incubator
from renderers import TerminalRenderer
from controllers import PIDController

import time

NUM_TICS = 200000 # 120 minutes
TARGET_TEMP = 37.0
AMBIENT_TEMP = 22.0

def simulate(starting_temp, ambient_temp, controller, renderer, t=.036):
    sim = Sim(starting_temp, ambient_temp)
    
    for i in range(NUM_TICS):
        renderer.render(sim, controller)
        controller.before_tick(sim, tictime=t)
        sim.tick(tictime=t)
        controller.after_tick(sim, tictime=t)
        
    sim.cleanup()

controller = PIDController(TARGET_TEMP)

renderer = TerminalRenderer()
simulate(AMBIENT_TEMP, AMBIENT_TEMP, controller, renderer)


def incubate(starting_temp, ambient_temp, controller, renderer):
    incubator = Incubator(ambient_temp)

    last_time = time.time()
    while(True):
        try:
            current_time = time.time()
            t = current_time - last_time
            renderer.render(incubator, controller)
            controller.before_tick(incubator, tictime=t)
            incubator.tick(tictime=t)
            controller.after_tick(incubator, tictime=t)
            last_time = current_time
        except:
            incubator.cleanup()
            renderer.render(incubator, controller)
            raise
        
# incubate(AMBIENT_TEMP, AMBIENT_TEMP, controller, renderer)