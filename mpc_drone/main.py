#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from dynamics.droneDynamics import droneDynamics
from solver.rungeKutta import rungeKutta4_Order
from visualizer.visualizer import MatplotlibVisualizer

###############Initial Conditions###################
simulation_time = 100
initial_state = np.array([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0])
initial_control_input = np.array([ 0.0, 0.0, 0.1, 9.81])
####################################################

drone = droneDynamics()
states = initial_state
control_input = initial_control_input
viz = MatplotlibVisualizer()
   

for i in range(simulation_time):
    states = rungeKutta4_Order(drone.getA(states),drone.getB(),drone.getC(states),states,control_input,1)
    position = states[9:12]
    viz.appendPosition(position)
    print(states)
plt.show()

