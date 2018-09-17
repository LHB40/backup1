import numpy as np
import matplotlib.pyplot as plt
import math

values1=[]
values2=[]
values3=[]
count=0

def ave(v):
    l=len(v)
    if l>1:
        average=sum(v)/l
        sigma=0
        tmp=0
        for i in range(l):
            tmp=math.pow(v[i]-average,2)
            sigma=sigma+tmp
        sigma=tmp/(l-1)
        return sigma
    else:
        return v[0]

plt.figure(1)
ax=plt.subplot(111)
plt.ion()

while 1:
    value1=np.random.randn()
    value2=np.random.randn()
    value3=value1+value2
    values1.append(value1)
    values2.append(value2)
    values3.append(value3)
    r1=ave(values1)
    r2=ave(values2)
    r3=ave(values3)
    r4=r1+r2
    plt.scatter(count,r3,c='r')
    plt.scatter(count,r4,c='b')
    count+=1
    plt.pause(0.1)
