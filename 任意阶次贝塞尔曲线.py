import numpy as np
import matplotlib.pyplot as plt

def bse(x,y,n):
    rex=[]
    rey=[]
    for i in range(len(x)-1):
        xt=x[i]*(100-n)/100+x[i+1]*n/100
        yt=y[i]*(100-n)/100+y[i+1]*n/100
        rex.append(xt)
        rey.append(yt)
    if len(rex)>1:
        rex,rey=bse(rex,rey,n)
    return (rex,rey)

def start(x,y):
    xx=[]
    yy=[]
    for i in range(101):
        a,b=bse(x,y,i)
        xx.append(a)
        yy.append(b)
    return xx,yy

def draw(x,y):
    xx,yy=start(x,y)
    fig=plt.Figure()
    ax=plt.subplot()
    ax.scatter(xx,yy)
    ax.scatter(x,y,c='r')
    plt.show()

x=[2,3,5,6,7,5]
y=[2,3,4,6,8,7]
draw(x,y)
