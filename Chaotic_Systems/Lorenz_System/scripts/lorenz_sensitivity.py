import numpy as np
from matplotlib import pyplot as plt

def rk4singlestep(f,dt,t0,y0):
    k1 = f(t0,y0)
    k2 = f(t0 + dt/2 ,y0 + (dt/2)*k1)
    k3 = f(t0 + dt/2 ,y0 + (dt/2)*k2)
    k4 = f(t0 + dt , y0 + dt*k3)
    yout = y0 + (dt/6)*(k1+2*k2+2*k3+k4)
    return yout
    
sigma = 10
rho = 28
beta = 8/3

def lorentz(t,y):
    dy = [
        sigma*(y[1]-y[0]) ,
        y[0]*(rho - y[2]) - y[1] ,
        y[0]*y[1]-beta*y[2]
    ]
    return np.array(dy)

y0_1 = [1, 1, 1]
y0_2 = [1, 1, 1 + 1e-8]

dt = 0.005
T = 200
transient = 500
nt = int(T / dt)
t_plot = np.linspace(0, T, nt)

Y1 = np.zeros((nt, 3))
Y1[0] = y0_1
yin1 = y0_1.copy()

for i in range(1, nt):
    yin1 = rk4singlestep(lorentz, dt, t_plot[i-1], yin1)
    Y1[i] = yin1

Y2 = np.zeros((nt, 3))
Y2[0] = y0_2
yin2 = y0_2.copy()

for i in range(1, nt):
    yin2 = rk4singlestep(lorentz, dt, t_plot[i-1], yin2)
    Y2[i] = yin2

Y1_plot = Y1[transient:]
Y2_plot = Y2[transient:]    

plt.figure(figsize=(14, 7))
plt.plot(t_plot[transient:], Y1_plot[:, 2], label=f'Initial: x0={y0_1[0]}, y0={y0_1[1]}, z0={y0_1[2]}', color='b', lw=1)
plt.plot(t_plot[transient:], Y2_plot[:, 2], label=f'Initial: x0={y0_2[0]}, y0={y0_2[1]}, z0={y0_2[2]:.8f}', color='r', lw=1, linestyle='--')

plt.xlabel('t', fontsize=14)
plt.ylabel('$z$', fontsize=14)
plt.title('z,t', fontsize=16)
plt.legend(fontsize=12, loc='upper right')
plt.grid(True, which='both', linestyle=':', linewidth=0.7, alpha=0.8)
plt.xlim(0, 80)
plt.tight_layout()
plt.savefig('./z_vs_t.png')
plt.show()
