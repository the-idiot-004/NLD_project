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

y0 = [0,1,1]
dt = 0.005
T = 300
nt = int(T/dt)
t = np.linspace(0,T,nt)
Y = np.zeros((nt,3))
Y[0] = y0
yin = y0

for i in range(1,nt):
    yin  = rk4singlestep(lorentz,dt,t[i-1],yin)
    Y[i]= yin
transient_cut = 30000
Y_plot = Y[transient_cut:]
t_plot = t[transient_cut:]

fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(111,projection = '3d',label= 'x0=(0,1,1)')

ax.plot(Y_plot[:,0],Y_plot[:,1],Y_plot[:,2],'blue',lw =0.6, label=f'Initial: x0={y0[0]}, y0={y0[1]}, z0={y0[2]}')

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.savefig('lorenz_attractor.png', dpi=300)
plt.show()

