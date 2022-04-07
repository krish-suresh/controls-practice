from math import pow
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

measured = np.array([[-393.66,-375.93,-351.04,-328.96,-299.35,-273.36,-245.89,-222.58,-198.03,-174.17,-146.32,-123.72,-103.47,-78.23,-52.63,-23.34,25.96,49.72,76.94,95.38,119.83,144.01,161.84,180.56,201.42,222.62,239.4,252.51,266.26,271.75,277.4,294.12,301.23,291.8,299.89],
                     [300.4,301.78,295.1,305.19,301.06,302.05,300,303.57,296.33,297.65,297.41,299.61,299.6,302.39,295.04,300.09,294.72,298.61,294.64,284.88,272.82,264.93,251.46,241.27,222.98,203.73,184.1,166.12,138.71,119.71,100.41,79.76,50.62,32.99,2.14]])

t_delta = 1
sigma = 6

F = np.array([[1, t_delta, 0.5*t_delta*t_delta, 0, 0,0],
              [0,1,t_delta,0,0,0],
              [0,0,1,0,0,0],
              [0,0,0,1,t_delta, 0.5*t_delta*t_delta],
              [0,0,0,0,1,t_delta],
              [0,0,0,0,0,1]])
Q = np.array([[pow(t_delta, 4)/4, pow(t_delta, 2)/2, pow(t_delta, 2)/2, 0, 0,0],
              [pow(t_delta, 2)/2,pow(t_delta, 2),t_delta,0,0,0],
              [pow(t_delta, 2)/2,t_delta,1,0,0,0],
              [0,0,0,pow(t_delta, 4)/4, pow(t_delta, 2)/2, pow(t_delta, 2)/2],
              [0,0,0,pow(t_delta, 2)/2,pow(t_delta, 2),t_delta],
              [0,0,0,pow(t_delta, 2)/2,t_delta,1]])

R = np.array([[pow(sigma, 2),0],
              [0,pow(sigma, 2)]])

H = np.array([[1,0,0,0,0,0],[0,0,0,1,0,0]])

x_hat = np.zeros((6,1))

P = np.eye(6,6)*500

# print(F)
# print(Q)
# print(R)
# print(P)
estimate = []
for i in range(35):
    x_hat = np.matmul(F,x_hat)
    print(x_hat)
    P = np.matmul(F, np.matmul(P, F.T)) + Q

    z = measured[:, i].reshape(2,1)

    K = np.matmul(np.matmul(P, H.T), np.linalg.inv(np.matmul(H, np.matmul(P, H.T))+R))
    x_hat = x_hat + np.matmul(K, (z-np.matmul(H,x_hat)))
    print(np.matmul(H,x_hat))
    estimate.append(np.matmul(H,x_hat))
    I = np.eye(6,6)
    P = np.matmul((I - np.matmul(K, H)), np.matmul(P, (I-np.matmul(K,H)).T)) + np.matmul(K,np.matmul(R,K.T))
estimate = np.array(estimate).reshape(35,2).T
print(estimate)
fig, ax = plt.subplots()
ax.plot(measured[0,:], measured[1,:])
ax.plot(estimate[0,:], estimate[1,:])

plt.show()