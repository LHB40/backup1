from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def zz(x,y):
    return (x-10)**2+(y-10)**2+x*y
    
x=np.arange(-20,20,0.25)
y=np.arange(-20,20,0.25)
x,y=np.meshgrid(x,y)
z=zz(x,y)

x1=[]
y1=[]
z1=[]
xt=-20
yt=-15
zt=zz(xt,yt)
x1.append(xt)
y1.append(yt)
z1.append(zt)
while 1:
    xtt=xt-0.5*(xt-10)
    ytt=yt-0.5*(yt-10)
    dx=xt-xtt
    dy=yt-ytt
    xt=xtt
    yt=ytt
    zt=zz(xt,yt)
    x1.append(xt)
    y1.append(yt)
    z1.append(zt)
    if abs(dx)<0.0001 and abs(dy)<0.0001:
        break

fig=plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.plot_surface(x, y, z,cmap='rainbow')
ax.plot(x1,y1,z1)
plt.show()
