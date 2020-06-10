import random as rd

minimum=999999  #初始化minimum为一个很大的值 保证任何结果都小于该值
result =""  #全局最小路径结果

pathLen=[[0,38,42,27,41,24],[38,0,8,21,13,22],[42,8,0,26,10,29],[27,21,26,0,18,5],[41,13,10,18,0,25],[24,22,29,5,25,0]]

class path():
    def __init__(self,p1,p2,n=5): #类型初始化,p1为交叉概率,p2为变异概率,n为城市数 本例为5（北京先后到5个城市）
        self.path=[i for i in range(n)]
        self.p1=p1
        self.p2=p2
        self.n=n
    def init(self): #用于第一代的基因生成
        for i in range(self.n):
            self.path[i]=rd.randint(0,self.n)
        
    def exchange(self): #交叉
        if rd.randint(1,100)>(100-self.p1):   #有概率交叉
            while 1:
                position1=rd.randint(0,self.n-1)   #随机生成交叉位置
                position2=rd.randint(0,self.n-1)
                if position1 != position2:  #判断交叉位置非同一位置
                    self.path[position1],self.path[position2]=self.path[position2],self.path[position1]
                    break
                else:
                    continue
    def change(self):
        if rd.randint(1,100)>(100-self.p2):     #有概率变异
            self.path[rd.randint(0,self.n-1)]=rd.randint(0,self.n)
    def calculate(self):    #计算路径总长度
        count=pathLen[1][self.path[0]]   #北京至第一个城市的路程
        for i in range(self.n-1):
            count+=pathLen[self.path[i]][self.path[i+1]]   #中途各个城市间的路程
        count+=pathLen[self.path[-1]][1]  #最后一个城市到北京的路程
        return count
    def parity(self):   #校验是否为每个城市去一次且不包含北京
        count=0
        path=self.path.copy()
        path.sort()
        for i in range(len(path)-1):
            if path[i]==path[i+1]:
                count+=1
            if path[i]==1:
                count+=1
        if count==0:
            return 1
        else:
            return 0

    def nxt(self,other): #产生子代
        p=path(self.p1,self.p2)
        for i in range(self.n):
            if rd.randint(1,100)>50:
                p.path[i]=self.path[i]
            else:
                p.path[i]=other.path[i]
        return p
        

def generate(n,p1,p2):  #生成种群 n为规模 p1为交叉概率 p2为变异概率
    t=[]
    for i in range(n):
        father=path(p1,p2)
        father.init()
        t.append(father)
    return t


def allChange(t):    #进行繁殖、变异、交换、淘汰
    global minimum
    global result
    l=len(t)
    print("本轮父代个数为:",l)
    if l>100:   #如果父代个数大于100则开始父代淘汰机制
        path=[]
        for i in t:
            path.append(i.calculate())   #计算各个个体的路径长度
        path.sort()  #路径长度排序
        tt=[]
        j=0
        while len(tt)<100:
            for i in t:
                if i.calculate()==path[j]:
                    tt.append(i)
            j+=1
        t=tt
    l=len(t)
    for i in range(l):   
        for j in range(l-1-i):
            child=t[i].nxt(t[j]) #两两交配产生子代
            child.exchange()     #子代交换
            child.change()      #子代变异
            t.append(child)          #向种群添加子代
    count=0
    for i in range(len(t)):  #去除不符合的成员
        if t[i-count].parity()==0: #杀死不符合要求的子代 （每个城市去一次且不包含北京）
            del(t[i-count])
            count+=1
    print("本轮产生子代后总数:",len(t))
    result1=t[-1].path
    mini=t[-1].calculate()
    for i in range(len(t)-1):   #获得各个个体的路程长度
        tt=t[i].calculate()     
        if mini>tt:             #比较是否是新的最小路径
            mini=tt
            result1=t[i].path
    print("本轮最小路径长度:",mini)
    print("本轮最小路径结果:",result1)
    if mini<minimum:
        minimum=mini
        result=result1
            



zq=generate(30,10,10) #generate(30,10,10)表示 初始种群30，交换概率10%，变异概率10%
for i in range(6):  #range(n) 标识迭代n代
    allChange(zq)
print("最后最小路径长度为:",minimum)
print("最后最小路径为:",result)

