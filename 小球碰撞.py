import tkinter as tk
from threading import Thread as th
import time
import math

class win():
    def __init__(self,n):
        self.w=tk.Tk()
        self.fr=tk.Frame(self.w)
        self.fr.pack()
        self.ca=tk.Canvas(self.fr,width=200,height=200)
        self.ca.pack()
        self.t=[]
        self.n=n
        self.r=20
    def add(self):
        for i in range(self.n):
            a=ball(self.ca,i*25+10,i*25+25,4*(i+3)/7,2*(i-3)/7,self.n,self.r)
            self.t.append(a)
    def cls(self):
        self.ca.delete('all')
    def cal(self):
        while 1:
            self.cls()
            for i in self.t:
                i.move()
                i.draw()
            self.t[-1].comwall()
            for i in range(self.n-1):
                self.t[i].comwall()
                for j in range(i+1,self.n):
                    self.t[i].comball(self.t[j],j)
            time.sleep(0.02)
    def make(self):
        time.sleep(2)
        self.t[0].vx=6
        self.t[0].vy=3
    def start(self):
        t=th(target=self.cal)
        t.setDaemon(True)
        t.start()
        #t=th(target=self.make)
        #t.setDaemon(True)
        #t.start()
    def loop(self):
        self.w.mainloop()

class ball():
    def __init__(self,ca,x,y,vx,vy,n,r):
        self.x=x
        self.y=y
        self.r=r
        self.vx=vx
        self.vy=vy
        self.ca=ca
        self.state=[0 for i in range(n)]
    def draw(self):
        self.ca.create_oval(self.x-self.r/2,self.y-self.r/2,self.x+self.r/2,self.y+self.r/2,fill='red')
    def move(self):
        self.x+=self.vx
        self.y+=self.vy
    def comball(self,other,n):
        if math.pow((self.x-other.x),2)+math.pow((self.y-other.y),2)<math.pow(self.r,2) and self.state[n]==0:
            self.state[n]=1
            vx1=self.vx
            vx2=other.vx
            vy1=self.vy
            vy2=other.vy
            #数学模型可能有错误 ↓  
            self.vx=(vx1*math.pow(other.y-self.y,2)+vx2*math.pow(other.x-self.x,2)+(vy2-vy1)*(other.x-self.x)*(other.y-self.y))/(math.pow(other.x-self.x,2)+math.pow(other.y-self.y,2))
            self.vy=(vy1*math.pow(other.x-self.x,2)+vy2*math.pow(other.y-self.y,2)+(vx2-vx1)*(other.x-self.x)*(other.y-self.y))/(math.pow(other.x-self.x,2)+math.pow(other.y-self.y,2))
            other.vx=(vx1*math.pow(other.x-self.x,2)+vx2*math.pow(other.y-self.y,2)-(vy2-vy1)*(other.x-self.x)*(other.y-self.y))/(math.pow(other.x-self.x,2)+math.pow(other.y-self.y,2))
            other.vx=(vy1*math.pow(other.y-self.y,2)+vy2*math.pow(other.x-self.x,2)-(vx2-vx1)*(other.x-self.x)*(other.y-self.y))/(math.pow(other.x-self.x,2)+math.pow(other.y-self.y,2))
        if math.pow((self.x-other.x),2)+math.pow((self.y-other.y),2)>=math.pow(20,2):
            self.state[n]=0 
    def comwall(self):
        if self.x<=self.r/2 or self.x>=200-self.r/2:
            self.vx=-self.vx
        if self.y<=self.r/2 or self.y>=200-self.r/2:
            self.vy=-self.vy

if __name__=='__main__':
    w=win(6)
    w.add()
    w.start()
    w.loop()
