#!/usr/bin/env python3
import numpy as np
from dynamics.droneDynamics import droneDynamics
from solver.rungeKutta import rk4
from visualizer.frameviz import FrameVisualization
from controller.controller import PID

###############Initial Conditions###################
simulation_time = 500
initial_state = np.array([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
initial_control_input = np.array([ 0.0, 0.0, 0.0, 9.81])
####################################################
sim = FrameVisualization([0,5],[0,5],[0,-5])

drone = droneDynamics()
states = initial_state
control_input = initial_control_input
##################Cascaded Altitude Controller################################
velControl_attitude = PID(1,0,0.5,4,-4,5)
posControl_attitude = PID(1,0,0.5,4,-4)
##############################################################################

sim.addFrame("Drone",states[9:12], sim.getRotZ(states[2]) @ sim.getRotY(states[1]) @ sim.getRotX(states[0])) 
sim.addFrame("DroneZRotating",states[9:12], sim.getRotZ(states[2]) @ sim.getRotY(states[1]) @ sim.getRotX(states[0]),0.2)   
while True:

    vel = posControl_attitude.update(-3 - states[11],0.03)
    control_input[3] = 9.81 - velControl_attitude.update(vel - states[8],0.03)

    states = rk4(drone.getA(states),drone.getB(),drone.getC(states),states,control_input,0.03, 5)
    sim.updateFrame("Drone",states[9:12], sim.getRotZ(states[2]) @ sim.getRotY(states[1]) @ sim.getRotX(states[0]))
    sim.updateFrame("DroneZRotating",states[9:12],sim.getRotZ(states[2]))
    sim.displayAllFrames(0.03)