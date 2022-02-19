import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import sin, cos, pi
from matplotlib.animation import FuncAnimation
import scipy.integrate as integrate
import control
# State: [x, x_dot, theta, theta_dot]
CART_W = 0.05
CART_H = 0.05
CART_Y = 0.15
L = 0.1
m = 1 # Pendulum Mass
M = 5 # Cart Mass
dt = 0.01
t_stop = 5
g = -9.8
d = 0.1
s=1
A = np.array([[0,1,0,0],
    [0,-d/M,-m*g/M,0],
    [0,0,0,1],
    [0,-s*d/(M*L),-s*(m+M)*g/(M*L),0]])

B = np.array([[0],[1/M],[0],[s*1/(M*L)]])
# print(np.linalg.matrix_rank(control.ctrb(A, B)))
p = np.array([-4.3,-4.4,-4.5,-4.6])
K = control.place(A,B,p)
Q = np.array([[1,0,0,0],
              [0,1,0,0],
              [0,0,10,0],
              [0,0,0,100]])
R = .0001

K = control.lqr(A,B,Q,R)[0]
def double_pen_non_linear(x, t):
    D = m*L*L*(M+m*(1-cos(x[2]**2)))
    dx = np.zeros_like(x)
    u = -np.matmul(K,(x-np.array([0.5,0,pi,0])))
    dx[0] = x[1]
    dx[1] = (1/D)*(-(m**2) * (L**2) *g*cos(x[2])*sin(x[2]) + m*(L**2)*(m*L*(x[3]**2)*sin(x[2]) - d*x[1])) + m*L*L*(1/D)*u
    dx[2] = x[3]
    dx[3] = (1/D)*((m+M)*m*g*L*sin(x[2]) - m*L*cos(x[2])*(m*L*x[3]**2*sin(x[2]) - d*x[1])) - m*L*cos(x[2])*(1/D)*u
    return dx

# Set Up plots
t = np.arange(0, t_stop, dt)
state = integrate.odeint(double_pen_non_linear, [0.25,0,pi-0.3,0], t)
fig, ax = plt.subplots()
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
line,  = ax.plot([],[], lw=2)
cart, = ax.plot([],[], marker='o', color='r', ls='')

def draw_pendulum(i):
    line.set_data([state[i][0], state[i][0]-L*sin(state[i][2])],[CART_Y, CART_Y-L*cos(state[i][2])])
    cart.set_data(state[i][0], CART_Y)
    return line, cart,
# ax.axis('equal')
ani = FuncAnimation(fig, draw_pendulum, len(state), interval=dt*1000, blit=True)
plt.show()