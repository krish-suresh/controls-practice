import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import sin, cos, pi
from matplotlib.animation import FuncAnimation
import scipy.integrate as integrate
# State: [x, x_dot, theta, theta_dot]
CART_W = 0.05
CART_H = 0.05
CART_Y = 0.15
L = 0.2
m = 0.4 # Pendulum Mass
M = 15 # Cart Mass
dt = 0.01
t_stop = 5
u = 0
g = -9.8
d = 0.1
def double_pen_non_linear(x, t):
    D = m*L*L*(M+m*(1-cos(x[2]**2)))
    dx = np.zeros_like(x)
    dx[0] = x[1]
    dx[1] = (1/D)*(-(m**2) * (L**2) *g*cos(x[2])*sin(x[2]) + m*(L**2)*(m*L*(x[3]**2)*sin(x[2]) - d*x[1])) + m*L*L*(1/D)*u
    dx[2] = x[3]
    dx[3] = (1/D)*((m+M)*m*g*L*sin(x[2]) - m*L*cos(x[2])*(m*L*x[3]**2*sin(x[2]) - d*x[1])) - m*L*cos(x[2])*(1/D)*u
    return dx

# Set Up plots
t = np.arange(0, t_stop, dt)
state = integrate.odeint(double_pen_non_linear, [0.5,0,2*pi/3,0], t)
fig, ax = plt.subplots()
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
line,  = ax.plot([],[], lw=2)
cart, = ax.plot([],[], marker='o', color='r', ls='')
prev_patch = None
print(state)
def draw_pendulum(i):
    line.set_data([state[i][0], state[i][0]-L*sin(state[i][2])],[CART_Y, CART_Y-L*cos(state[i][2])])
    cart.set_data(state[i][0], CART_Y)
    # prev_patch = cart
    # cart = patches.Rectangle((state[i][0]-CART_W/2, CART_Y-(CART_H/2)), CART_W, CART_H)
    # prev_patch.remove()
    # ax.add_patch(cart)
    return line, cart,
# ax.axis('equal')
ani = FuncAnimation(fig, draw_pendulum, len(state), interval=dt*1000, blit=True)
plt.show()