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

t_range = np.linspace(0,15,500)
g = -9.8 # m/s^2
x_0 = 50 # m
v_0 = 0 # m/s

p = 15
r = 10
x_hat = [100, 10]
x = [x_0, v_0]
t_last = 0
z_last = 0
pos = []
measure = []
estimate = []
for t in t_range:
    t_delta = t-t_last
    t_last = t
    x[0] += x[1]*t_delta
    x[1] += g*t_delta
    pos.append(x[0])

    z = np.random.normal(x[0], scale=r)
    measure.append(z)

    K = p/(p+r)
    p = (1-K)*p
    x_hat[0] = x_hat[0] + K*(z-x_hat[0])
    if t_delta != 0:
        x_hat[1] = x_hat[1] + K*(((z-z_last)/t_delta) - x_hat[1])
        print(x_hat[1])
    z_last = z
    estimate.append(x_hat[0])
    x_hat[0] += t_delta*x_hat[1]
    x_hat[1] += g*t_delta

fig, ax = plt.subplots()
ax.plot(t_range, pos)
ax.plot(t_range, measure)
ax.plot(t_range, estimate)
fig, ax = plt.subplots()
ax.plot(t_range, abs(np.array(pos)-np.array(estimate)))
plt.show()