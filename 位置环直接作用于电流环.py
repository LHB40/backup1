import numpy as np
import matplotlib.pyplot as plt

class pi():
    def __init__(self,ka,kb,r,inertia,v):
        self.c=40000
        self.x=[i*v for i in range(self.c)]
        self.target=[i for i in range(int(self.c/2))]
        for i in range(self.c-int(self.c/2)):
            self.target.append(self.target[int(self.c/2)-1])
        self.position=[0 for i in self.x]
        self.speed=0
        self.current_integrate=0
        self.ka=ka
        self.kb=kb
        self.inertia=inertia
        self.current=0
        self.r=r

    def GetCurrent(self,tar,pos,current,ka,kb,current_integrate):
        err=tar-pos
        p_value=ka*err
        current_integrate+=(p_value*kb)
        return (p_value+current_integrate,current_integrate)

    def GetSpeed(self,speed,current,inertia):
        if speed>0:
            speed+=((current-self.r)/inertia)
        else:
            speed+=((current+self.r)/inertia)
        return speed

    def GetPosition(self,n,position):
        position[n]=position[n-1]+self.speed

    def cal(self):
        for i in range(self.c-1):
            if i%100==0:
                self.current,self.current_integrate=self.GetCurrent(self.target[i+1],self.position[i],self.current,self.ka,self.kb,self.current_integrate)
            self.speed=self.GetSpeed(self.speed,self.current,self.inertia)
            self.GetPosition(i+1,self.position)
        print(self.target[-1]-self.position[-1])

#无积分 低增益
aa=pi(0.1,0,100,10000,20)
aa.cal()
#无积分 高增益
aa1=pi(1,0,100,10000,20)
aa1.cal()
#无积分 适当增益
aa2=pi(0.9,0,100,10000,20)
aa2.cal()
#有积分 适当增益
aa3=pi(0.9,0.04,100,10000,20)
aa3.cal()
#有积分 适当增益 负载增大
aa4=pi(0.9,0.04,5000,500000,20)
aa4.cal()
#有积分 适当增益 负载减小
aa5=pi(0.9,0.04,80,8000,20)
aa5.cal()

fig=plt.Figure()
ax=plt.subplot(321)
ax.plot(aa.x,aa.position,color="red")
ax.plot(aa.x,aa.target,color="blue")

ax=plt.subplot(322)
ax.plot(aa1.x,aa1.position,color="red")
ax.plot(aa1.x,aa1.target,color="blue")

ax=plt.subplot(323)
ax.plot(aa2.x,aa2.position,color="red")
ax.plot(aa2.x,aa2.target,color="blue")

ax=plt.subplot(324)
ax.plot(aa3.x,aa3.position,color="red")
ax.plot(aa3.x,aa3.target,color="blue")

ax=plt.subplot(325)
ax.plot(aa4.x,aa4.position,color="red")
ax.plot(aa4.x,aa4.target,color="blue")

ax=plt.subplot(326)
ax.plot(aa5.x,aa5.position,color="red")
ax.plot(aa5.x,aa5.target,color="blue")

plt.show()
