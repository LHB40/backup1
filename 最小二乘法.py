import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

x=np.arange(0,100)
y=x.copy()
x,y=np.meshgrid(x,y)
z=x**2+2*y**2-16*x*y-6*y+10+np.sin(x)*np.cos(y)*10
x1=[]
y1=[]
z1=[]
for i in x:
    for m in i:
        x1.append(m)
x=np.array(x1)

for i in y:
    for m in i:
        y1.append(m)
y=np.array(y1)

for i in z:
    for m in i:
        z1.append(m)
z=np.array(z1)

def aa(p,x,y,z):
    a,b,c,d,e=p
    return z-(a*x**2+b*y**2+c*x*y+d*y+e)

p=(0,0,0,0,0)

r=leastsq(aa,p,(x,y,z))
print(r)
