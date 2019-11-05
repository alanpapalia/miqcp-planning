# VTOL Parameter File
import numpy as np
from math import sqrt

# Physical parameters known to controller
mc = 1          # Mass of copter (kg)
Jc = 0.0042     # Inertia of copter (kg m^2)
mr = 0.25       # Mass of right rotor (kg)
ml = 0.25       # Mass of left rotor (kg)
d = 0.65         # Distance from copter c.o.g. to rotor (m)
mu = 0.1        # Drag coefficient (kg/s)
g = 9.81        # Gravity (m/s^2)

# Animation parameters
L = 6           # Ground length (m)
cbw = 0.3       # Copter body width (m)
caw = 0.05      # Copter arm width (m)
rw = 0.6        # Copter rotor width (m)
rh = 0.15       # Copter rotor height (m)

# Initial conditions
zc0 = 3.0       # Copter horizontal initial position (m)
h0 = 1.0        # Copter initial height (m)
theta0 = 0.0    # Copter initial angle (rad)
zcdot0 = 0.0    # Copter initial velocity (m/s)
hdot0 = 0.0     # Copter height initial velocity (m/s)
thetadot0 = 0.0 # Copter angle initial velocity (rad/s)

# Simulation parameters
t0 = 0.0        # Start time of simulation
tf = 10         # End time of simulation
Ts = 0.01       # Sample time for simulation
t_plot = 0.1   # Simulation update rate
t_win = 20      # Plot time window
beta = 0.05     # Dirty derivative parameter

# Equilibrium parameters
Fe = g * (mc + ml + mr)

# Wind
F_wind = 0.1
