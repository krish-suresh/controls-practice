# Kalman filter applied to a 1 dim system of a ball dropped from a building

# x = x_0 + vt + at^2 /2
# v = v_0 + at
# a = g

# p = 1 estimate uncertainty
# r = 0.1 measurement uncertainty
# q = 0 process noise

# obs z, obs uncertainty r

# calculate K = p/(p+r)
# estimate state 
# update p = (1-K)*p

# estimate state = x + K(z-x)

# predict state 

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

t_range = np.linspace(0,10,500)
g = -9.8 # m/s^2
x_0 = 50 # m
v_0 = 0 # m/s

x = [x_0, v_0]
t_last = 0
pos = []
for t in t_range:
    t_delta = t-t_last
    t_last = t
    x[0] += x[1]*t_delta
    x[1] += g*t_delta
    pos.append(x[0])

fig, ax = plt.subplots()
ax.plot(t_range, pos)
plt.show()