from matplotlib import pyplot as plt
import numpy as np
import random

'''产生一行随机数组,n为列数'''
def r(n):
    t=[]
    for i in range(n):
        t.append(random.random())
    return t

'''产生随机数组m为行,n为列'''
def ar(m,n):
    t=[]
    for i in range(m):
        t.append(r(n))
    return np.array(t)

'''sigmod'''
def sig(x): 
    return 1/(1+pow(np.e,-x))

'''sigmod求导'''
def dsig(x):
    return x*(1-x)

'''向前'''
def forward(x,y):
    I=[x,y,x*y]
    hi=np.mat([I])*np.mat(w)
    h=[]
    for i in hi.tolist()[0]:
        h.append(sig(i))
    h2i=np.mat([h])*m
    h2=[]
    for i in h2i.tolist()[0]:
        h2.append(sig(i))
    o=(np.mat([h2])*np.mat(n)).tolist()[0][0]
    return (I,h,h2,o)

def back(x,y,t):
    r=forward(x,y)
    for i in range(len(w)):
        for j in range(len(w[0])):
            w[i][j]=w[i][j]-step*(r[3]-t)*n[0][0]*dsig(r[2][0])*m[j][0]*r[0][i]*dsig(r[1][j])
    for i in range(len(m)):
        for j in range(len(m[0])):
            m[i][j]=m[i][j]-step*(r[3]-t)*n[j][0]*dsig(r[2][j])*r[1][i]
    for i in range(len(n)):
        n[i][0]=n[i][0]-step*(r[3]-t)*r[2][i]

def ss(x,y):
    print(forward(x,y)[3])
    
step=0.1 #学习速率

'''初始化'''
w=ar(3,4)
m=ar(4,4)
n=ar(4,1)

l=[[3,7,1],[5,8.3,1],[2,1,1],[9,9,0],[7,9.8,0],[10,4.5,0]]

'''学习'''
for i in range(10000):
    for j in l:
        x,y,t=j
        back(x,y,t)

for i in l:
    ss(i[0],i[1])

'''输出结果图像'''
t=[]
cc=['b','r']
for i in range(50):
    for j in range(50):
        t.append((i/5,j/5,forward(i/5,j/5)[3]))

fig=plt.figure()
ax=plt.subplot(111)
for i in t[::4]:
    k=1 if i[2]>0.5 else 0
    plt.scatter(i[0],i[1],c=cc[k])
plt.show()
